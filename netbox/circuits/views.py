from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from dcim.views import PathTraceView
from netbox.views import generic
from tenancy.views import ObjectContactsView
from utilities.forms import ConfirmationForm
from utilities.query import count_related
from utilities.views import GetRelatedModelsMixin, register_model_view
from . import filtersets, forms, tables
from .models import *


#
# Providers
#

class ProviderListView(generic.ObjectListView):
    queryset = Provider.objects.annotate(
        count_circuits=count_related(Circuit, 'provider')
    )
    filterset = filtersets.ProviderFilterSet
    filterset_form = forms.ProviderFilterForm
    table = tables.ProviderTable


@register_model_view(Provider)
class ProviderView(GetRelatedModelsMixin, generic.ObjectView):
    queryset = Provider.objects.all()

    def get_extra_context(self, request, instance):
        return {
            'related_models': self.get_related_models(request, instance),
        }


@register_model_view(Provider, 'edit')
class ProviderEditView(generic.ObjectEditView):
    queryset = Provider.objects.all()
    form = forms.ProviderForm


@register_model_view(Provider, 'delete')
class ProviderDeleteView(generic.ObjectDeleteView):
    queryset = Provider.objects.all()


class ProviderBulkImportView(generic.BulkImportView):
    queryset = Provider.objects.all()
    model_form = forms.ProviderImportForm


class ProviderBulkEditView(generic.BulkEditView):
    queryset = Provider.objects.annotate(
        count_circuits=count_related(Circuit, 'provider')
    )
    filterset = filtersets.ProviderFilterSet
    table = tables.ProviderTable
    form = forms.ProviderBulkEditForm


class ProviderBulkDeleteView(generic.BulkDeleteView):
    queryset = Provider.objects.annotate(
        count_circuits=count_related(Circuit, 'provider')
    )
    filterset = filtersets.ProviderFilterSet
    table = tables.ProviderTable


@register_model_view(Provider, 'contacts')
class ProviderContactsView(ObjectContactsView):
    queryset = Provider.objects.all()


#
# ProviderAccounts
#

class ProviderAccountListView(generic.ObjectListView):
    queryset = ProviderAccount.objects.annotate(
        count_circuits=count_related(Circuit, 'provider_account')
    )
    filterset = filtersets.ProviderAccountFilterSet
    filterset_form = forms.ProviderAccountFilterForm
    table = tables.ProviderAccountTable


@register_model_view(ProviderAccount)
class ProviderAccountView(GetRelatedModelsMixin, generic.ObjectView):
    queryset = ProviderAccount.objects.all()

    def get_extra_context(self, request, instance):
        return {
            'related_models': self.get_related_models(request, instance),
        }


@register_model_view(ProviderAccount, 'edit')
class ProviderAccountEditView(generic.ObjectEditView):
    queryset = ProviderAccount.objects.all()
    form = forms.ProviderAccountForm


@register_model_view(ProviderAccount, 'delete')
class ProviderAccountDeleteView(generic.ObjectDeleteView):
    queryset = ProviderAccount.objects.all()


class ProviderAccountBulkImportView(generic.BulkImportView):
    queryset = ProviderAccount.objects.all()
    model_form = forms.ProviderAccountImportForm
    table = tables.ProviderAccountTable


class ProviderAccountBulkEditView(generic.BulkEditView):
    queryset = ProviderAccount.objects.annotate(
        count_circuits=count_related(Circuit, 'provider_account')
    )
    filterset = filtersets.ProviderAccountFilterSet
    table = tables.ProviderAccountTable
    form = forms.ProviderAccountBulkEditForm


class ProviderAccountBulkDeleteView(generic.BulkDeleteView):
    queryset = ProviderAccount.objects.annotate(
        count_circuits=count_related(Circuit, 'provider_account')
    )
    filterset = filtersets.ProviderAccountFilterSet
    table = tables.ProviderAccountTable


@register_model_view(ProviderAccount, 'contacts')
class ProviderAccountContactsView(ObjectContactsView):
    queryset = ProviderAccount.objects.all()


#
# Provider networks
#

class ProviderNetworkListView(generic.ObjectListView):
    queryset = ProviderNetwork.objects.all()
    filterset = filtersets.ProviderNetworkFilterSet
    filterset_form = forms.ProviderNetworkFilterForm
    table = tables.ProviderNetworkTable


@register_model_view(ProviderNetwork)
class ProviderNetworkView(GetRelatedModelsMixin, generic.ObjectView):
    queryset = ProviderNetwork.objects.all()

    def get_extra_context(self, request, instance):
        return {
            'related_models': self.get_related_models(
                request,
                instance,
                extra=(
                    (
                        Circuit.objects.restrict(request.user, 'view').filter(terminations__provider_network=instance),
                        'provider_network_id',
                    ),
                ),
            ),
        }


@register_model_view(ProviderNetwork, 'edit')
class ProviderNetworkEditView(generic.ObjectEditView):
    queryset = ProviderNetwork.objects.all()
    form = forms.ProviderNetworkForm


@register_model_view(ProviderNetwork, 'delete')
class ProviderNetworkDeleteView(generic.ObjectDeleteView):
    queryset = ProviderNetwork.objects.all()


class ProviderNetworkBulkImportView(generic.BulkImportView):
    queryset = ProviderNetwork.objects.all()
    model_form = forms.ProviderNetworkImportForm


class ProviderNetworkBulkEditView(generic.BulkEditView):
    queryset = ProviderNetwork.objects.all()
    filterset = filtersets.ProviderNetworkFilterSet
    table = tables.ProviderNetworkTable
    form = forms.ProviderNetworkBulkEditForm


class ProviderNetworkBulkDeleteView(generic.BulkDeleteView):
    queryset = ProviderNetwork.objects.all()
    filterset = filtersets.ProviderNetworkFilterSet
    table = tables.ProviderNetworkTable


#
# Circuit Types
#

class CircuitTypeListView(generic.ObjectListView):
    queryset = CircuitType.objects.annotate(
        circuit_count=count_related(Circuit, 'type')
    )
    filterset = filtersets.CircuitTypeFilterSet
    filterset_form = forms.CircuitTypeFilterForm
    table = tables.CircuitTypeTable


@register_model_view(CircuitType)
class CircuitTypeView(GetRelatedModelsMixin, generic.ObjectView):
    queryset = CircuitType.objects.all()

    def get_extra_context(self, request, instance):
        return {
            'related_models': self.get_related_models(request, instance),
        }


@register_model_view(CircuitType, 'edit')
class CircuitTypeEditView(generic.ObjectEditView):
    queryset = CircuitType.objects.all()
    form = forms.CircuitTypeForm


@register_model_view(CircuitType, 'delete')
class CircuitTypeDeleteView(generic.ObjectDeleteView):
    queryset = CircuitType.objects.all()


class CircuitTypeBulkImportView(generic.BulkImportView):
    queryset = CircuitType.objects.all()
    model_form = forms.CircuitTypeImportForm


class CircuitTypeBulkEditView(generic.BulkEditView):
    queryset = CircuitType.objects.annotate(
        circuit_count=count_related(Circuit, 'type')
    )
    filterset = filtersets.CircuitTypeFilterSet
    table = tables.CircuitTypeTable
    form = forms.CircuitTypeBulkEditForm


class CircuitTypeBulkDeleteView(generic.BulkDeleteView):
    queryset = CircuitType.objects.annotate(
        circuit_count=count_related(Circuit, 'type')
    )
    filterset = filtersets.CircuitTypeFilterSet
    table = tables.CircuitTypeTable


#
# Circuits
#

class CircuitListView(generic.ObjectListView):
    queryset = Circuit.objects.prefetch_related(
        'tenant__group', 'termination_a__site', 'termination_z__site',
        'termination_a__provider_network', 'termination_z__provider_network',
    )
    filterset = filtersets.CircuitFilterSet
    filterset_form = forms.CircuitFilterForm
    table = tables.CircuitTable


@register_model_view(Circuit)
class CircuitView(generic.ObjectView):
    queryset = Circuit.objects.all()


@register_model_view(Circuit, 'edit')
class CircuitEditView(generic.ObjectEditView):
    queryset = Circuit.objects.all()
    form = forms.CircuitForm


@register_model_view(Circuit, 'delete')
class CircuitDeleteView(generic.ObjectDeleteView):
    queryset = Circuit.objects.all()


class CircuitBulkImportView(generic.BulkImportView):
    queryset = Circuit.objects.all()
    model_form = forms.CircuitImportForm
    additional_permissions = [
        'circuits.add_circuittermination',
    ]
    related_object_forms = {
        'terminations': forms.CircuitTerminationImportRelatedForm,
    }

    def prep_related_object_data(self, parent, data):
        data.update({'circuit': parent})
        return data


class CircuitBulkEditView(generic.BulkEditView):
    queryset = Circuit.objects.prefetch_related(
        'termination_a__site', 'termination_z__site',
        'termination_a__provider_network', 'termination_z__provider_network',
    )
    filterset = filtersets.CircuitFilterSet
    table = tables.CircuitTable
    form = forms.CircuitBulkEditForm


class CircuitBulkDeleteView(generic.BulkDeleteView):
    queryset = Circuit.objects.prefetch_related(
        'termination_a__site', 'termination_z__site',
        'termination_a__provider_network', 'termination_z__provider_network',
    )
    filterset = filtersets.CircuitFilterSet
    table = tables.CircuitTable


class CircuitSwapTerminations(generic.ObjectEditView):
    """
    Swap the A and Z terminations of a circuit.
    """
    queryset = Circuit.objects.all()

    def get(self, request, pk):
        circuit = get_object_or_404(self.queryset, pk=pk)
        form = ConfirmationForm()

        # Circuit must have at least one termination to swap
        if not circuit.termination_a and not circuit.termination_z:
            messages.error(request, _(
                "No terminations have been defined for circuit {circuit}."
            ).format(circuit=circuit))
            return redirect('circuits:circuit', pk=circuit.pk)

        return render(request, 'circuits/circuit_terminations_swap.html', {
            'circuit': circuit,
            'termination_a': circuit.termination_a,
            'termination_z': circuit.termination_z,
            'form': form,
            'panel_class': 'light',
            'button_class': 'primary',
            'return_url': circuit.get_absolute_url(),
        })

    def post(self, request, pk):
        circuit = get_object_or_404(self.queryset, pk=pk)
        form = ConfirmationForm(request.POST)

        if form.is_valid():

            termination_a = CircuitTermination.objects.filter(pk=circuit.termination_a_id).first()
            termination_z = CircuitTermination.objects.filter(pk=circuit.termination_z_id).first()

            if termination_a and termination_z:
                # Use a placeholder to avoid an IntegrityError on the (circuit, term_side) unique constraint
                with transaction.atomic():
                    termination_a.term_side = '_'
                    termination_a.save()
                    termination_z.term_side = 'A'
                    termination_z.save()
                    termination_a.term_side = 'Z'
                    termination_a.save()
                    circuit.refresh_from_db()
                    circuit.termination_a = termination_z
                    circuit.termination_z = termination_a
                    circuit.save()
            elif termination_a:
                termination_a.term_side = 'Z'
                termination_a.save()
                circuit.refresh_from_db()
                circuit.termination_a = None
                circuit.save()
            else:
                termination_z.term_side = 'A'
                termination_z.save()
                circuit.refresh_from_db()
                circuit.termination_z = None
                circuit.save()

            messages.success(request, _("Swapped terminations for circuit {circuit}.").format(circuit=circuit))
            return redirect('circuits:circuit', pk=circuit.pk)

        return render(request, 'circuits/circuit_terminations_swap.html', {
            'circuit': circuit,
            'termination_a': circuit.termination_a,
            'termination_z': circuit.termination_z,
            'form': form,
            'panel_class': 'default',
            'button_class': 'primary',
            'return_url': circuit.get_absolute_url(),
        })


@register_model_view(Circuit, 'contacts')
class CircuitContactsView(ObjectContactsView):
    queryset = Circuit.objects.all()


#
# Circuit terminations
#

class CircuitTerminationListView(generic.ObjectListView):
    queryset = CircuitTermination.objects.all()
    filterset = filtersets.CircuitTerminationFilterSet
    filterset_form = forms.CircuitTerminationFilterForm
    table = tables.CircuitTerminationTable


@register_model_view(CircuitTermination)
class CircuitTerminationView(generic.ObjectView):
    queryset = CircuitTermination.objects.all()


@register_model_view(CircuitTermination, 'edit')
class CircuitTerminationEditView(generic.ObjectEditView):
    queryset = CircuitTermination.objects.all()
    form = forms.CircuitTerminationForm


@register_model_view(CircuitTermination, 'delete')
class CircuitTerminationDeleteView(generic.ObjectDeleteView):
    queryset = CircuitTermination.objects.all()


class CircuitTerminationBulkImportView(generic.BulkImportView):
    queryset = CircuitTermination.objects.all()
    model_form = forms.CircuitTerminationImportForm


class CircuitTerminationBulkEditView(generic.BulkEditView):
    queryset = CircuitTermination.objects.all()
    filterset = filtersets.CircuitTerminationFilterSet
    table = tables.CircuitTerminationTable
    form = forms.CircuitTerminationBulkEditForm


class CircuitTerminationBulkDeleteView(generic.BulkDeleteView):
    queryset = CircuitTermination.objects.all()
    filterset = filtersets.CircuitTerminationFilterSet
    table = tables.CircuitTerminationTable


# Trace view
register_model_view(CircuitTermination, 'trace', kwargs={'model': CircuitTermination})(PathTraceView)


#
# Circuit Groups
#

class CircuitGroupListView(generic.ObjectListView):
    queryset = CircuitGroup.objects.annotate(
        circuit_group_assignment_count=count_related(CircuitGroupAssignment, 'group')
    )
    filterset = filtersets.CircuitGroupFilterSet
    filterset_form = forms.CircuitGroupFilterForm
    table = tables.CircuitGroupTable


@register_model_view(CircuitGroup)
class CircuitGroupView(GetRelatedModelsMixin, generic.ObjectView):
    queryset = CircuitGroup.objects.all()

    def get_extra_context(self, request, instance):
        return {
            'related_models': self.get_related_models(request, instance),
        }


@register_model_view(CircuitGroup, 'edit')
class CircuitGroupEditView(generic.ObjectEditView):
    queryset = CircuitGroup.objects.all()
    form = forms.CircuitGroupForm


@register_model_view(CircuitGroup, 'delete')
class CircuitGroupDeleteView(generic.ObjectDeleteView):
    queryset = CircuitGroup.objects.all()


class CircuitGroupBulkImportView(generic.BulkImportView):
    queryset = CircuitGroup.objects.all()
    model_form = forms.CircuitGroupImportForm


class CircuitGroupBulkEditView(generic.BulkEditView):
    queryset = CircuitGroup.objects.all()
    filterset = filtersets.CircuitGroupFilterSet
    table = tables.CircuitGroupTable
    form = forms.CircuitGroupBulkEditForm


class CircuitGroupBulkDeleteView(generic.BulkDeleteView):
    queryset = CircuitGroup.objects.all()
    filterset = filtersets.CircuitGroupFilterSet
    table = tables.CircuitGroupTable


#
# Circuit Groups
#

class CircuitGroupAssignmentListView(generic.ObjectListView):
    queryset = CircuitGroupAssignment.objects.all()
    filterset = filtersets.CircuitGroupAssignmentFilterSet
    filterset_form = forms.CircuitGroupAssignmentFilterForm
    table = tables.CircuitGroupAssignmentTable


@register_model_view(CircuitGroupAssignment)
class CircuitGroupAssignmentView(generic.ObjectView):
    queryset = CircuitGroupAssignment.objects.all()


@register_model_view(CircuitGroupAssignment, 'edit')
class CircuitGroupAssignmentEditView(generic.ObjectEditView):
    queryset = CircuitGroupAssignment.objects.all()
    form = forms.CircuitGroupAssignmentForm


@register_model_view(CircuitGroupAssignment, 'delete')
class CircuitGroupAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = CircuitGroupAssignment.objects.all()


class CircuitGroupAssignmentBulkImportView(generic.BulkImportView):
    queryset = CircuitGroupAssignment.objects.all()
    model_form = forms.CircuitGroupAssignmentImportForm


class CircuitGroupAssignmentBulkEditView(generic.BulkEditView):
    queryset = CircuitGroupAssignment.objects.all()
    filterset = filtersets.CircuitGroupAssignmentFilterSet
    table = tables.CircuitGroupAssignmentTable
    form = forms.CircuitGroupAssignmentBulkEditForm


class CircuitGroupAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = CircuitGroupAssignment.objects.all()
    filterset = filtersets.CircuitGroupAssignmentFilterSet
    table = tables.CircuitGroupAssignmentTable
