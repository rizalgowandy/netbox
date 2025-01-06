from django.urls import include, path

from utilities.urls import get_model_urls
from . import views

app_name = 'circuits'
urlpatterns = [

    # Providers
    path('providers/', views.ProviderListView.as_view(), name='provider_list'),
    path('providers/add/', views.ProviderEditView.as_view(), name='provider_add'),
    path('providers/import/', views.ProviderBulkImportView.as_view(), name='provider_import'),
    path('providers/edit/', views.ProviderBulkEditView.as_view(), name='provider_bulk_edit'),
    path('providers/delete/', views.ProviderBulkDeleteView.as_view(), name='provider_bulk_delete'),
    path('providers/<int:pk>/', include(get_model_urls('circuits', 'provider'))),

    # Provider accounts
    path('provider-accounts/', views.ProviderAccountListView.as_view(), name='provideraccount_list'),
    path('provider-accounts/add/', views.ProviderAccountEditView.as_view(), name='provideraccount_add'),
    path('provider-accounts/import/', views.ProviderAccountBulkImportView.as_view(), name='provideraccount_import'),
    path('provider-accounts/edit/', views.ProviderAccountBulkEditView.as_view(), name='provideraccount_bulk_edit'),
    path('provider-accounts/delete/', views.ProviderAccountBulkDeleteView.as_view(), name='provideraccount_bulk_delete'),
    path('provider-accounts/<int:pk>/', include(get_model_urls('circuits', 'provideraccount'))),

    # Provider networks
    path('provider-networks/', views.ProviderNetworkListView.as_view(), name='providernetwork_list'),
    path('provider-networks/add/', views.ProviderNetworkEditView.as_view(), name='providernetwork_add'),
    path('provider-networks/import/', views.ProviderNetworkBulkImportView.as_view(), name='providernetwork_import'),
    path('provider-networks/edit/', views.ProviderNetworkBulkEditView.as_view(), name='providernetwork_bulk_edit'),
    path('provider-networks/delete/', views.ProviderNetworkBulkDeleteView.as_view(), name='providernetwork_bulk_delete'),
    path('provider-networks/<int:pk>/', include(get_model_urls('circuits', 'providernetwork'))),

    # Circuit types
    path('circuit-types/', views.CircuitTypeListView.as_view(), name='circuittype_list'),
    path('circuit-types/add/', views.CircuitTypeEditView.as_view(), name='circuittype_add'),
    path('circuit-types/import/', views.CircuitTypeBulkImportView.as_view(), name='circuittype_import'),
    path('circuit-types/edit/', views.CircuitTypeBulkEditView.as_view(), name='circuittype_bulk_edit'),
    path('circuit-types/delete/', views.CircuitTypeBulkDeleteView.as_view(), name='circuittype_bulk_delete'),
    path('circuit-types/<int:pk>/', include(get_model_urls('circuits', 'circuittype'))),

    # Circuits
    path('circuits/', views.CircuitListView.as_view(), name='circuit_list'),
    path('circuits/add/', views.CircuitEditView.as_view(), name='circuit_add'),
    path('circuits/import/', views.CircuitBulkImportView.as_view(), name='circuit_import'),
    path('circuits/edit/', views.CircuitBulkEditView.as_view(), name='circuit_bulk_edit'),
    path('circuits/delete/', views.CircuitBulkDeleteView.as_view(), name='circuit_bulk_delete'),
    path('circuits/<int:pk>/terminations/swap/', views.CircuitSwapTerminations.as_view(), name='circuit_terminations_swap'),
    path('circuits/<int:pk>/', include(get_model_urls('circuits', 'circuit'))),

    # Circuit terminations
    path('circuit-terminations/', views.CircuitTerminationListView.as_view(), name='circuittermination_list'),
    path('circuit-terminations/add/', views.CircuitTerminationEditView.as_view(), name='circuittermination_add'),
    path('circuit-terminations/import/', views.CircuitTerminationBulkImportView.as_view(), name='circuittermination_import'),
    path('circuit-terminations/edit/', views.CircuitTerminationBulkEditView.as_view(), name='circuittermination_bulk_edit'),
    path('circuit-terminations/delete/', views.CircuitTerminationBulkDeleteView.as_view(), name='circuittermination_bulk_delete'),
    path('circuit-terminations/<int:pk>/', include(get_model_urls('circuits', 'circuittermination'))),

    # Circuit Groups
    path('circuit-groups/', views.CircuitGroupListView.as_view(), name='circuitgroup_list'),
    path('circuit-groups/add/', views.CircuitGroupEditView.as_view(), name='circuitgroup_add'),
    path('circuit-groups/import/', views.CircuitGroupBulkImportView.as_view(), name='circuitgroup_import'),
    path('circuit-groups/edit/', views.CircuitGroupBulkEditView.as_view(), name='circuitgroup_bulk_edit'),
    path('circuit-groups/delete/', views.CircuitGroupBulkDeleteView.as_view(), name='circuitgroup_bulk_delete'),
    path('circuit-groups/<int:pk>/', include(get_model_urls('circuits', 'circuitgroup'))),

    # Circuit Group Assignments
    path('circuit-group-assignments/', views.CircuitGroupAssignmentListView.as_view(), name='circuitgroupassignment_list'),
    path('circuit-group-assignments/add/', views.CircuitGroupAssignmentEditView.as_view(), name='circuitgroupassignment_add'),
    path('circuit-group-assignments/import/', views.CircuitGroupAssignmentBulkImportView.as_view(), name='circuitgroupassignment_import'),
    path('circuit-group-assignments/edit/', views.CircuitGroupAssignmentBulkEditView.as_view(), name='circuitgroupassignment_bulk_edit'),
    path('circuit-group-assignments/delete/', views.CircuitGroupAssignmentBulkDeleteView.as_view(), name='circuitgroupassignment_bulk_delete'),
    path('circuit-group-assignments/<int:pk>/', include(get_model_urls('circuits', 'circuitgroupassignment'))),
]
