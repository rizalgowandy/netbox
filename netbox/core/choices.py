from django.utils.translation import gettext_lazy as _

from utilities.choices import ChoiceSet


#
# Data sources
#

class DataSourceStatusChoices(ChoiceSet):
    NEW = 'new'
    QUEUED = 'queued'
    SYNCING = 'syncing'
    COMPLETED = 'completed'
    FAILED = 'failed'

    CHOICES = (
        (NEW, _('New'), 'blue'),
        (QUEUED, _('Queued'), 'orange'),
        (SYNCING, _('Syncing'), 'cyan'),
        (COMPLETED, _('Completed'), 'green'),
        (FAILED, _('Failed'), 'red'),
    )


#
# Managed files
#

class ManagedFileRootPathChoices(ChoiceSet):
    SCRIPTS = 'scripts'  # settings.SCRIPTS_ROOT
    REPORTS = 'reports'  # settings.REPORTS_ROOT

    CHOICES = (
        (SCRIPTS, _('Scripts')),
        (REPORTS, _('Reports')),
    )


#
# Jobs
#

class JobStatusChoices(ChoiceSet):

    STATUS_PENDING = 'pending'
    STATUS_SCHEDULED = 'scheduled'
    STATUS_RUNNING = 'running'
    STATUS_COMPLETED = 'completed'
    STATUS_ERRORED = 'errored'
    STATUS_FAILED = 'failed'

    CHOICES = (
        (STATUS_PENDING, _('Pending'), 'cyan'),
        (STATUS_SCHEDULED, _('Scheduled'), 'gray'),
        (STATUS_RUNNING, _('Running'), 'blue'),
        (STATUS_COMPLETED, _('Completed'), 'green'),
        (STATUS_ERRORED, _('Errored'), 'red'),
        (STATUS_FAILED, _('Failed'), 'red'),
    )

    ENQUEUED_STATE_CHOICES = (
        STATUS_PENDING,
        STATUS_SCHEDULED,
        STATUS_RUNNING,
    )

    TERMINAL_STATE_CHOICES = (
        STATUS_COMPLETED,
        STATUS_ERRORED,
        STATUS_FAILED,
    )


#
# ObjectChanges
#

class ObjectChangeActionChoices(ChoiceSet):

    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'

    CHOICES = (
        (ACTION_CREATE, _('Created'), 'green'),
        (ACTION_UPDATE, _('Updated'), 'blue'),
        (ACTION_DELETE, _('Deleted'), 'red'),
    )
