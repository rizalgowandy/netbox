import json
import platform

from django import __version__ as DJANGO_VERSION
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.cache import cache
from django.db import connection, ProgrammingError
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import View
from django_rq.queues import get_connection, get_queue_by_index, get_redis_connection
from django_rq.settings import QUEUES_MAP, QUEUES_LIST
from django_rq.utils import get_jobs, get_statistics, stop_jobs
from rq import requeue_job
from rq.exceptions import NoSuchJobError
from rq.job import Job as RQ_Job, JobStatus as RQJobStatus
from rq.registry import (
    DeferredJobRegistry, FailedJobRegistry, FinishedJobRegistry, ScheduledJobRegistry, StartedJobRegistry,
)
from rq.worker import Worker
from rq.worker_registration import clean_worker_registry

from netbox.config import get_config, PARAMS
from netbox.views import generic
from netbox.views.generic.base import BaseObjectView
from netbox.views.generic.mixins import TableMixin
from utilities.data import shallow_compare_dict
from utilities.forms import ConfirmationForm
from utilities.htmx import htmx_partial
from utilities.json import ConfigJSONEncoder
from utilities.query import count_related
from utilities.views import ContentTypePermissionRequiredMixin, GetRelatedModelsMixin, register_model_view
from . import filtersets, forms, tables
from .choices import DataSourceStatusChoices
from .jobs import SyncDataSourceJob
from .models import *
from .plugins import get_catalog_plugins, get_local_plugins
from .tables import CatalogPluginTable, PluginVersionTable


#
# Data sources
#

class DataSourceListView(generic.ObjectListView):
    queryset = DataSource.objects.annotate(
        file_count=count_related(DataFile, 'source')
    )
    filterset = filtersets.DataSourceFilterSet
    filterset_form = forms.DataSourceFilterForm
    table = tables.DataSourceTable


@register_model_view(DataSource)
class DataSourceView(GetRelatedModelsMixin, generic.ObjectView):
    queryset = DataSource.objects.all()

    def get_extra_context(self, request, instance):
        return {
            'related_models': self.get_related_models(request, instance),
        }


@register_model_view(DataSource, 'sync')
class DataSourceSyncView(BaseObjectView):
    queryset = DataSource.objects.all()

    def get_required_permission(self):
        return 'core.sync_datasource'

    def get(self, request, pk):
        # Redirect GET requests to the object view
        datasource = get_object_or_404(self.queryset, pk=pk)
        return redirect(datasource.get_absolute_url())

    def post(self, request, pk):
        datasource = get_object_or_404(self.queryset, pk=pk)

        # Enqueue the sync job & update the DataSource's status
        job = SyncDataSourceJob.enqueue(instance=datasource, user=request.user)
        datasource.status = DataSourceStatusChoices.QUEUED
        DataSource.objects.filter(pk=datasource.pk).update(status=datasource.status)

        messages.success(
            request,
            _("Queued job #{id} to sync {datasource}").format(id=job.pk, datasource=datasource)
        )
        return redirect(datasource.get_absolute_url())


@register_model_view(DataSource, 'edit')
class DataSourceEditView(generic.ObjectEditView):
    queryset = DataSource.objects.all()
    form = forms.DataSourceForm


@register_model_view(DataSource, 'delete')
class DataSourceDeleteView(generic.ObjectDeleteView):
    queryset = DataSource.objects.all()


class DataSourceBulkImportView(generic.BulkImportView):
    queryset = DataSource.objects.all()
    model_form = forms.DataSourceImportForm


class DataSourceBulkEditView(generic.BulkEditView):
    queryset = DataSource.objects.annotate(
        count_files=count_related(DataFile, 'source')
    )
    filterset = filtersets.DataSourceFilterSet
    table = tables.DataSourceTable
    form = forms.DataSourceBulkEditForm


class DataSourceBulkDeleteView(generic.BulkDeleteView):
    queryset = DataSource.objects.annotate(
        count_files=count_related(DataFile, 'source')
    )
    filterset = filtersets.DataSourceFilterSet
    table = tables.DataSourceTable


#
# Data files
#

class DataFileListView(generic.ObjectListView):
    queryset = DataFile.objects.defer('data')
    filterset = filtersets.DataFileFilterSet
    filterset_form = forms.DataFileFilterForm
    table = tables.DataFileTable
    actions = {
        'bulk_delete': {'delete'},
    }


@register_model_view(DataFile)
class DataFileView(generic.ObjectView):
    queryset = DataFile.objects.all()


@register_model_view(DataFile, 'delete')
class DataFileDeleteView(generic.ObjectDeleteView):
    queryset = DataFile.objects.all()


class DataFileBulkDeleteView(generic.BulkDeleteView):
    queryset = DataFile.objects.defer('data')
    filterset = filtersets.DataFileFilterSet
    table = tables.DataFileTable


#
# Jobs
#

class JobListView(generic.ObjectListView):
    queryset = Job.objects.all()
    filterset = filtersets.JobFilterSet
    filterset_form = forms.JobFilterForm
    table = tables.JobTable
    actions = {
        'export': {'view'},
        'bulk_delete': {'delete'},
    }


class JobView(generic.ObjectView):
    queryset = Job.objects.all()


class JobDeleteView(generic.ObjectDeleteView):
    queryset = Job.objects.all()


class JobBulkDeleteView(generic.BulkDeleteView):
    queryset = Job.objects.all()
    filterset = filtersets.JobFilterSet
    table = tables.JobTable


#
# Change logging
#

class ObjectChangeListView(generic.ObjectListView):
    queryset = ObjectChange.objects.valid_models()
    filterset = filtersets.ObjectChangeFilterSet
    filterset_form = forms.ObjectChangeFilterForm
    table = tables.ObjectChangeTable
    template_name = 'core/objectchange_list.html'
    actions = {
        'export': {'view'},
    }


@register_model_view(ObjectChange)
class ObjectChangeView(generic.ObjectView):
    queryset = ObjectChange.objects.valid_models()

    def get_extra_context(self, request, instance):
        related_changes = ObjectChange.objects.valid_models().restrict(request.user, 'view').filter(
            request_id=instance.request_id
        ).exclude(
            pk=instance.pk
        )
        related_changes_table = tables.ObjectChangeTable(
            data=related_changes[:50],
            orderable=False
        )

        objectchanges = ObjectChange.objects.valid_models().restrict(request.user, 'view').filter(
            changed_object_type=instance.changed_object_type,
            changed_object_id=instance.changed_object_id,
        )

        next_change = objectchanges.filter(time__gt=instance.time).order_by('time').first()
        prev_change = objectchanges.filter(time__lt=instance.time).order_by('-time').first()

        if not instance.prechange_data and instance.action in ['update', 'delete'] and prev_change:
            non_atomic_change = True
            prechange_data = prev_change.postchange_data_clean
        else:
            non_atomic_change = False
            prechange_data = instance.prechange_data_clean

        if prechange_data and instance.postchange_data:
            diff_added = shallow_compare_dict(
                prechange_data or dict(),
                instance.postchange_data_clean or dict(),
                exclude=['last_updated'],
            )
            diff_removed = {
                x: prechange_data.get(x) for x in diff_added
            } if prechange_data else {}
        else:
            diff_added = None
            diff_removed = None

        return {
            'diff_added': diff_added,
            'diff_removed': diff_removed,
            'next_change': next_change,
            'prev_change': prev_change,
            'related_changes_table': related_changes_table,
            'related_changes_count': related_changes.count(),
            'non_atomic_change': non_atomic_change
        }


#
# Config Revisions
#

class ConfigRevisionListView(generic.ObjectListView):
    queryset = ConfigRevision.objects.all()
    filterset = filtersets.ConfigRevisionFilterSet
    filterset_form = forms.ConfigRevisionFilterForm
    table = tables.ConfigRevisionTable


@register_model_view(ConfigRevision)
class ConfigRevisionView(generic.ObjectView):
    queryset = ConfigRevision.objects.all()


class ConfigRevisionEditView(generic.ObjectEditView):
    queryset = ConfigRevision.objects.all()
    form = forms.ConfigRevisionForm


@register_model_view(ConfigRevision, 'delete')
class ConfigRevisionDeleteView(generic.ObjectDeleteView):
    queryset = ConfigRevision.objects.all()


class ConfigRevisionBulkDeleteView(generic.BulkDeleteView):
    queryset = ConfigRevision.objects.all()
    filterset = filtersets.ConfigRevisionFilterSet
    table = tables.ConfigRevisionTable


class ConfigRevisionRestoreView(ContentTypePermissionRequiredMixin, View):

    def get_required_permission(self):
        return 'core.configrevision_edit'

    def get(self, request, pk):
        candidate_config = get_object_or_404(ConfigRevision, pk=pk)

        # Get the current ConfigRevision
        config_version = get_config().version
        current_config = ConfigRevision.objects.filter(pk=config_version).first()

        params = []
        for param in PARAMS:
            params.append((
                param.name,
                current_config.data.get(param.name, None) if current_config else None,
                candidate_config.data.get(param.name, None)
            ))

        return render(request, 'core/configrevision_restore.html', {
            'object': candidate_config,
            'params': params,
        })

    def post(self, request, pk):
        if not request.user.has_perm('core.configrevision_edit'):
            return HttpResponseForbidden()

        candidate_config = get_object_or_404(ConfigRevision, pk=pk)
        candidate_config.activate()
        messages.success(request, _("Restored configuration revision #{id}").format(id=pk))

        return redirect(candidate_config.get_absolute_url())


#
# Background Tasks (RQ)
#

class BaseRQView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_staff


class BackgroundQueueListView(TableMixin, BaseRQView):
    table = tables.BackgroundQueueTable

    def get(self, request):
        data = get_statistics(run_maintenance_tasks=True)["queues"]
        table = self.get_table(data, request, bulk_actions=False)

        return render(request, 'core/rq_queue_list.html', {
            'table': table,
        })


class BackgroundTaskListView(TableMixin, BaseRQView):
    table = tables.BackgroundTaskTable

    def get_table_data(self, request, queue, status):
        jobs = []

        # Call get_jobs() to returned queued tasks
        if status == RQJobStatus.QUEUED:
            return queue.get_jobs()

        # For other statuses, determine the registry to list (or raise a 404 for invalid statuses)
        try:
            registry_cls = {
                RQJobStatus.STARTED: StartedJobRegistry,
                RQJobStatus.DEFERRED: DeferredJobRegistry,
                RQJobStatus.FINISHED: FinishedJobRegistry,
                RQJobStatus.FAILED: FailedJobRegistry,
                RQJobStatus.SCHEDULED: ScheduledJobRegistry,
            }[status]
        except KeyError:
            raise Http404
        registry = registry_cls(queue.name, queue.connection)

        job_ids = registry.get_job_ids()
        if status != RQJobStatus.DEFERRED:
            jobs = get_jobs(queue, job_ids, registry)
        else:
            # Deferred jobs require special handling
            for job_id in job_ids:
                try:
                    jobs.append(RQ_Job.fetch(job_id, connection=queue.connection, serializer=queue.serializer))
                except NoSuchJobError:
                    pass

        if jobs and status == RQJobStatus.SCHEDULED:
            for job in jobs:
                job.scheduled_at = registry.get_scheduled_time(job)

        return jobs

    def get(self, request, queue_index, status):
        queue = get_queue_by_index(queue_index)
        data = self.get_table_data(request, queue, status)
        table = self.get_table(data, request, False)

        # If this is an HTMX request, return only the rendered table HTML
        if htmx_partial(request):
            return render(request, 'htmx/table.html', {
                'table': table,
            })

        return render(request, 'core/rq_task_list.html', {
            'table': table,
            'queue': queue,
            'status': status,
        })


class BackgroundTaskView(BaseRQView):

    def get(self, request, job_id):
        # all the RQ queues should use the same connection
        config = QUEUES_LIST[0]
        try:
            job = RQ_Job.fetch(job_id, connection=get_redis_connection(config['connection_config']),)
        except NoSuchJobError:
            raise Http404(_("Job {job_id} not found").format(job_id=job_id))

        queue_index = QUEUES_MAP[job.origin]
        queue = get_queue_by_index(queue_index)

        try:
            exc_info = job._exc_info
        except AttributeError:
            exc_info = None

        return render(request, 'core/rq_task.html', {
            'queue': queue,
            'job': job,
            'queue_index': queue_index,
            'dependency_id': job._dependency_id,
            'exc_info': exc_info,
        })


class BackgroundTaskDeleteView(BaseRQView):

    def get(self, request, job_id):
        if not request.htmx:
            return redirect(reverse('core:background_queue_list'))

        form = ConfirmationForm(initial=request.GET)

        return render(request, 'htmx/delete_form.html', {
            'object_type': 'background task',
            'object': job_id,
            'form': form,
            'form_url': reverse('core:background_task_delete', kwargs={'job_id': job_id})
        })

    def post(self, request, job_id):
        form = ConfirmationForm(request.POST)

        if form.is_valid():
            # all the RQ queues should use the same connection
            config = QUEUES_LIST[0]
            try:
                job = RQ_Job.fetch(job_id, connection=get_redis_connection(config['connection_config']),)
            except NoSuchJobError:
                raise Http404(_("Job {job_id} not found").format(job_id=job_id))

            queue_index = QUEUES_MAP[job.origin]
            queue = get_queue_by_index(queue_index)

            # Remove job id from queue and delete the actual job
            queue.connection.lrem(queue.key, 0, job.id)
            job.delete()
            messages.success(request, _('Job {id} has been deleted.').format(id=job_id))
        else:
            messages.error(request, _('Error deleting job {id}: {error}').format(id=job_id, error=form.errors[0]))

        return redirect(reverse('core:background_queue_list'))


class BackgroundTaskRequeueView(BaseRQView):

    def get(self, request, job_id):
        # all the RQ queues should use the same connection
        config = QUEUES_LIST[0]
        try:
            job = RQ_Job.fetch(job_id, connection=get_redis_connection(config['connection_config']),)
        except NoSuchJobError:
            raise Http404(_("Job {id} not found.").format(id=job_id))

        queue_index = QUEUES_MAP[job.origin]
        queue = get_queue_by_index(queue_index)

        requeue_job(job_id, connection=queue.connection, serializer=queue.serializer)
        messages.success(request, _('Job {id} has been re-enqueued.').format(id=job_id))
        return redirect(reverse('core:background_task', args=[job_id]))


class BackgroundTaskEnqueueView(BaseRQView):

    def get(self, request, job_id):
        # all the RQ queues should use the same connection
        config = QUEUES_LIST[0]
        try:
            job = RQ_Job.fetch(job_id, connection=get_redis_connection(config['connection_config']),)
        except NoSuchJobError:
            raise Http404(_("Job {id} not found.").format(id=job_id))

        queue_index = QUEUES_MAP[job.origin]
        queue = get_queue_by_index(queue_index)

        try:
            # _enqueue_job is new in RQ 1.14, this is used to enqueue
            # job regardless of its dependencies
            queue._enqueue_job(job)
        except AttributeError:
            queue.enqueue_job(job)

        # Remove job from correct registry if needed
        if job.get_status() == RQJobStatus.DEFERRED:
            registry = DeferredJobRegistry(queue.name, queue.connection)
            registry.remove(job)
        elif job.get_status() == RQJobStatus.FINISHED:
            registry = FinishedJobRegistry(queue.name, queue.connection)
            registry.remove(job)
        elif job.get_status() == RQJobStatus.SCHEDULED:
            registry = ScheduledJobRegistry(queue.name, queue.connection)
            registry.remove(job)

        messages.success(request, _('Job {id} has been enqueued.').format(id=job_id))
        return redirect(reverse('core:background_task', args=[job_id]))


class BackgroundTaskStopView(BaseRQView):

    def get(self, request, job_id):
        # all the RQ queues should use the same connection
        config = QUEUES_LIST[0]
        try:
            job = RQ_Job.fetch(job_id, connection=get_redis_connection(config['connection_config']),)
        except NoSuchJobError:
            raise Http404(_("Job {job_id} not found").format(job_id=job_id))

        queue_index = QUEUES_MAP[job.origin]
        queue = get_queue_by_index(queue_index)

        stopped_jobs = stop_jobs(queue, job_id)[0]
        if len(stopped_jobs) == 1:
            messages.success(request, _('Job {id} has been stopped.').format(id=job_id))
        else:
            messages.error(request, _('Failed to stop job {id}').format(id=job_id))

        return redirect(reverse('core:background_task', args=[job_id]))


class WorkerListView(TableMixin, BaseRQView):
    table = tables.WorkerTable

    def get_table_data(self, request, queue):
        clean_worker_registry(queue)
        all_workers = Worker.all(queue.connection)
        workers = [worker for worker in all_workers if queue.name in worker.queue_names()]
        return workers

    def get(self, request, queue_index):
        queue = get_queue_by_index(queue_index)
        data = self.get_table_data(request, queue)

        table = self.get_table(data, request, False)

        # If this is an HTMX request, return only the rendered table HTML
        if htmx_partial(request):
            if not request.htmx.target:
                table.embedded = True
                # Hide selection checkboxes
                if 'pk' in table.base_columns:
                    table.columns.hide('pk')
            return render(request, 'htmx/table.html', {
                'table': table,
                'queue': queue,
            })

        return render(request, 'core/rq_worker_list.html', {
            'table': table,
            'queue': queue,
        })


class WorkerView(BaseRQView):

    def get(self, request, key):
        # all the RQ queues should use the same connection
        config = QUEUES_LIST[0]
        worker = Worker.find_by_key('rq:worker:' + key, connection=get_redis_connection(config['connection_config']))
        # Convert microseconds to milliseconds
        worker.total_working_time = worker.total_working_time / 1000

        return render(request, 'core/rq_worker.html', {
            'worker': worker,
            'job': worker.get_current_job(),
            'total_working_time': worker.total_working_time * 1000,
        })


#
# System
#

class SystemView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request):

        # System stats
        psql_version = db_name = db_size = None
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version()")
                psql_version = cursor.fetchone()[0]
                psql_version = psql_version.split('(')[0].strip()
                cursor.execute("SELECT current_database()")
                db_name = cursor.fetchone()[0]
                cursor.execute(f"SELECT pg_size_pretty(pg_database_size('{db_name}'))")
                db_size = cursor.fetchone()[0]
        except (ProgrammingError, IndexError):
            pass
        stats = {
            'netbox_release': settings.RELEASE,
            'django_version': DJANGO_VERSION,
            'python_version': platform.python_version(),
            'postgresql_version': psql_version,
            'database_name': db_name,
            'database_size': db_size,
            'rq_worker_count': Worker.count(get_connection('default')),
        }

        # Configuration
        config = get_config()

        # Raw data export
        if 'export' in request.GET:
            stats['netbox_release'] = stats['netbox_release'].asdict()
            params = [param.name for param in PARAMS]
            data = {
                **stats,
                'plugins': settings.PLUGINS,
                'config': {
                    k: getattr(config, k) for k in sorted(params)
                },
            }
            response = HttpResponse(json.dumps(data, cls=ConfigJSONEncoder, indent=4), content_type='text/json')
            response['Content-Disposition'] = 'attachment; filename="netbox.json"'
            return response

        # Serialize any CustomValidator classes
        if hasattr(config, 'CUSTOM_VALIDATORS') and config.CUSTOM_VALIDATORS:
            config.CUSTOM_VALIDATORS = json.dumps(config.CUSTOM_VALIDATORS, cls=ConfigJSONEncoder, indent=4)

        return render(request, 'core/system.html', {
            'stats': stats,
            'config': config,
        })


#
# Plugins
#

class BasePluginView(UserPassesTestMixin, View):
    CACHE_KEY_CATALOG_ERROR = 'plugins-catalog-error'

    def test_func(self):
        return self.request.user.is_staff

    def get_cached_plugins(self, request):
        catalog_plugins = {}
        catalog_plugins_error = cache.get(self.CACHE_KEY_CATALOG_ERROR, default=False)
        if not catalog_plugins_error:
            catalog_plugins = get_catalog_plugins()
            if not catalog_plugins:
                # Cache for 5 minutes to avoid spamming connection
                cache.set(self.CACHE_KEY_CATALOG_ERROR, True, 300)
                messages.warning(request, _("Plugins catalog could not be loaded"))

        return get_local_plugins(catalog_plugins)


class PluginListView(BasePluginView):

    def get(self, request):
        q = request.GET.get('q', None)

        plugins = self.get_cached_plugins(request).values()
        if q:
            plugins = [obj for obj in plugins if q.casefold() in obj.title_short.casefold()]

        table = CatalogPluginTable(plugins, user=request.user)
        table.configure(request)

        # If this is an HTMX request, return only the rendered table HTML
        if htmx_partial(request):
            return render(request, 'htmx/table.html', {
                'table': table,
            })

        return render(request, 'core/plugin_list.html', {
            'table': table,
        })


class PluginView(BasePluginView):

    def get(self, request, name):

        plugins = self.get_cached_plugins(request)
        if name not in plugins:
            raise Http404(_("Plugin {name} not found").format(name=name))
        plugin = plugins[name]

        table = PluginVersionTable(plugin.release_recent_history, user=request.user)
        table.configure(request)

        return render(request, 'core/plugin.html', {
            'plugin': plugin,
            'table': table,
        })
