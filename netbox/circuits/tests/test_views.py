import datetime

from django.test import override_settings
from django.urls import reverse

from circuits.choices import *
from circuits.models import *
from core.models import ObjectType
from dcim.models import Cable, Interface, Site
from ipam.models import ASN, RIR
from netbox.choices import ImportFormatChoices
from users.models import ObjectPermission
from utilities.testing import ViewTestCases, create_tags, create_test_device


class ProviderTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = Provider

    @classmethod
    def setUpTestData(cls):

        rir = RIR.objects.create(name='RFC 6996', is_private=True)
        asns = [
            ASN(asn=65000 + i, rir=rir) for i in range(8)
        ]
        ASN.objects.bulk_create(asns)

        providers = (
            Provider(name='Provider 1', slug='provider-1'),
            Provider(name='Provider 2', slug='provider-2'),
            Provider(name='Provider 3', slug='provider-3'),
        )
        Provider.objects.bulk_create(providers)
        providers[0].asns.set([asns[0], asns[1]])
        providers[1].asns.set([asns[2], asns[3]])
        providers[2].asns.set([asns[4], asns[5]])

        tags = create_tags('Alpha', 'Bravo', 'Charlie')

        cls.form_data = {
            'name': 'Provider X',
            'slug': 'provider-x',
            'asns': [asns[6].pk, asns[7].pk],
            'comments': 'Another provider',
            'tags': [t.pk for t in tags],
        }

        cls.csv_data = (
            "name,slug",
            "Provider 4,provider-4",
            "Provider 5,provider-5",
            "Provider 6,provider-6",
        )

        cls.csv_update_data = (
            "id,name,comments",
            f"{providers[0].pk},Provider 7,New comment7",
            f"{providers[1].pk},Provider 8,New comment8",
            f"{providers[2].pk},Provider 9,New comment9",
        )

        cls.bulk_edit_data = {
            'comments': 'New comments',
        }


class CircuitTypeTestCase(ViewTestCases.OrganizationalObjectViewTestCase):
    model = CircuitType

    @classmethod
    def setUpTestData(cls):

        circuit_types = (
            CircuitType(name='Circuit Type 1', slug='circuit-type-1'),
            CircuitType(name='Circuit Type 2', slug='circuit-type-2'),
            CircuitType(name='Circuit Type 3', slug='circuit-type-3'),
        )

        CircuitType.objects.bulk_create(circuit_types)

        tags = create_tags('Alpha', 'Bravo', 'Charlie')

        cls.form_data = {
            'name': 'Circuit Type X',
            'slug': 'circuit-type-x',
            'description': 'A new circuit type',
            'tags': [t.pk for t in tags],
        }

        cls.csv_data = (
            "name,slug",
            "Circuit Type 4,circuit-type-4",
            "Circuit Type 5,circuit-type-5",
            "Circuit Type 6,circuit-type-6",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{circuit_types[0].pk},Circuit Type 7,New description7",
            f"{circuit_types[1].pk},Circuit Type 8,New description8",
            f"{circuit_types[2].pk},Circuit Type 9,New description9",
        )

        cls.bulk_edit_data = {
            'description': 'Foo',
        }


class CircuitTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = Circuit

    def setUp(self):
        super().setUp()

        self.add_permissions(
            'circuits.add_circuittermination',
        )

    @classmethod
    def setUpTestData(cls):
        Site.objects.create(name='Site 1', slug='site-1')

        providers = (
            Provider(name='Provider 1', slug='provider-1'),
            Provider(name='Provider 2', slug='provider-2'),
        )
        Provider.objects.bulk_create(providers)

        provider_accounts = (
            ProviderAccount(name='Provider Account 1', provider=providers[0], account='1234'),
            ProviderAccount(name='Provider Account 2', provider=providers[1], account='2345'),
        )
        ProviderAccount.objects.bulk_create(provider_accounts)

        circuittypes = (
            CircuitType(name='Circuit Type 1', slug='circuit-type-1'),
            CircuitType(name='Circuit Type 2', slug='circuit-type-2'),
        )
        CircuitType.objects.bulk_create(circuittypes)

        circuits = (
            Circuit(cid='Circuit 1', provider=providers[0], provider_account=provider_accounts[0], type=circuittypes[0]),
            Circuit(cid='Circuit 2', provider=providers[0], provider_account=provider_accounts[0], type=circuittypes[0]),
            Circuit(cid='Circuit 3', provider=providers[0], provider_account=provider_accounts[0], type=circuittypes[0]),
        )

        Circuit.objects.bulk_create(circuits)

        tags = create_tags('Alpha', 'Bravo', 'Charlie')

        cls.form_data = {
            'cid': 'Circuit X',
            'provider': providers[1].pk,
            'provider_account': provider_accounts[1].pk,
            'type': circuittypes[1].pk,
            'status': CircuitStatusChoices.STATUS_DECOMMISSIONED,
            'tenant': None,
            'install_date': datetime.date(2020, 1, 1),
            'termination_date': datetime.date(2021, 1, 1),
            'commit_rate': 1000,
            'description': 'A new circuit',
            'comments': 'Some comments',
            'tags': [t.pk for t in tags],
        }

        cls.csv_data = (
            "cid,provider,provider_account,type,status",
            "Circuit 4,Provider 1,Provider Account 1,Circuit Type 1,active",
            "Circuit 5,Provider 1,Provider Account 1,Circuit Type 1,active",
            "Circuit 6,Provider 1,Provider Account 1,Circuit Type 1,active",
        )

        cls.csv_update_data = (
            "id,cid,description,status",
            f"{circuits[0].pk},Circuit 7,New description7,{CircuitStatusChoices.STATUS_DECOMMISSIONED}",
            f"{circuits[1].pk},Circuit 8,New description8,{CircuitStatusChoices.STATUS_DECOMMISSIONED}",
            f"{circuits[2].pk},Circuit 9,New description9,{CircuitStatusChoices.STATUS_DECOMMISSIONED}",
        )

        cls.bulk_edit_data = {
            'provider': providers[1].pk,
            'provider_account': provider_accounts[1].pk,
            'type': circuittypes[1].pk,
            'status': CircuitStatusChoices.STATUS_DECOMMISSIONED,
            'tenant': None,
            'commit_rate': 2000,
            'description': 'New description',
            'comments': 'New comments',
        }

    @override_settings(EXEMPT_VIEW_PERMISSIONS=['*'], EXEMPT_EXCLUDE_MODELS=[])
    def test_bulk_import_objects_with_terminations(self):
        json_data = """
            [
              {
                "cid": "Circuit 7",
                "provider": "Provider 1",
                "type": "Circuit Type 1",
                "status": "active",
                "description": "Testing Import",
                "terminations": [
                  {
                    "term_side": "A",
                    "site": "Site 1"
                  },
                  {
                    "term_side": "Z",
                    "site": "Site 1"
                  }
                ]
              }
            ]
        """
        initial_count = self._get_queryset().count()
        data = {
            'data': json_data,
            'format': ImportFormatChoices.JSON,
        }

        # Assign model-level permission
        obj_perm = ObjectPermission(
            name='Test permission',
            actions=['add']
        )
        obj_perm.save()
        obj_perm.users.add(self.user)
        obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

        # Try GET with model-level permission
        self.assertHttpStatus(self.client.get(self._get_url('import')), 200)

        # Test POST with permission
        self.assertHttpStatus(self.client.post(self._get_url('import'), data), 302)
        self.assertEqual(self._get_queryset().count(), initial_count + 1)


class ProviderAccountTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = ProviderAccount

    @classmethod
    def setUpTestData(cls):

        providers = (
            Provider(name='Provider 1', slug='provider-1'),
            Provider(name='Provider 2', slug='provider-2'),
        )
        Provider.objects.bulk_create(providers)

        provider_accounts = (
            ProviderAccount(name='Provider Account 1', provider=providers[0], account='1234'),
            ProviderAccount(name='Provider Account 2', provider=providers[0], account='2345'),
            ProviderAccount(name='Provider Account 3', provider=providers[0], account='3456'),
        )
        ProviderAccount.objects.bulk_create(provider_accounts)

        tags = create_tags('Alpha', 'Bravo', 'Charlie')

        cls.form_data = {
            'name': 'Provider Account X',
            'provider': providers[1].pk,
            'account': 'XXXX',
            'description': 'A new provider network',
            'comments': 'Longer description goes here',
            'tags': [t.pk for t in tags],
        }

        cls.csv_data = (
            "name,provider,account,description",
            "Provider Account 4,Provider 1,4567,Foo",
            "Provider Account 5,Provider 1,5678,Bar",
            "Provider Account 6,Provider 1,6789,Baz",
        )

        cls.csv_update_data = (
            "id,name,account,description",
            f"{provider_accounts[0].pk},Provider Network 7,7890,New description7",
            f"{provider_accounts[1].pk},Provider Network 8,8901,New description8",
            f"{provider_accounts[2].pk},Provider Network 9,9012,New description9",
        )

        cls.bulk_edit_data = {
            'provider': providers[1].pk,
            'description': 'New description',
            'comments': 'New comments',
        }


class ProviderNetworkTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = ProviderNetwork

    @classmethod
    def setUpTestData(cls):

        providers = (
            Provider(name='Provider 1', slug='provider-1'),
            Provider(name='Provider 2', slug='provider-2'),
        )
        Provider.objects.bulk_create(providers)

        provider_networks = (
            ProviderNetwork(name='Provider Network 1', provider=providers[0]),
            ProviderNetwork(name='Provider Network 2', provider=providers[0]),
            ProviderNetwork(name='Provider Network 3', provider=providers[0]),
        )

        ProviderNetwork.objects.bulk_create(provider_networks)

        tags = create_tags('Alpha', 'Bravo', 'Charlie')

        cls.form_data = {
            'name': 'Provider Network X',
            'provider': providers[1].pk,
            'description': 'A new provider network',
            'comments': 'Longer description goes here',
            'tags': [t.pk for t in tags],
        }

        cls.csv_data = (
            "name,provider,description",
            "Provider Network 4,Provider 1,Foo",
            "Provider Network 5,Provider 1,Bar",
            "Provider Network 6,Provider 1,Baz",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{provider_networks[0].pk},Provider Network 7,New description7",
            f"{provider_networks[1].pk},Provider Network 8,New description8",
            f"{provider_networks[2].pk},Provider Network 9,New description9",
        )

        cls.bulk_edit_data = {
            'provider': providers[1].pk,
            'description': 'New description',
            'comments': 'New comments',
        }


class CircuitTerminationTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = CircuitTermination

    @classmethod
    def setUpTestData(cls):

        sites = (
            Site(name='Site 1', slug='site-1'),
            Site(name='Site 2', slug='site-2'),
            Site(name='Site 3', slug='site-3'),
        )
        Site.objects.bulk_create(sites)
        provider = Provider.objects.create(name='Provider 1', slug='provider-1')
        circuittype = CircuitType.objects.create(name='Circuit Type 1', slug='circuit-type-1')

        circuits = (
            Circuit(cid='Circuit 1', provider=provider, type=circuittype),
            Circuit(cid='Circuit 2', provider=provider, type=circuittype),
            Circuit(cid='Circuit 3', provider=provider, type=circuittype),
        )
        Circuit.objects.bulk_create(circuits)

        circuit_terminations = (
            CircuitTermination(circuit=circuits[0], term_side='A', site=sites[0]),
            CircuitTermination(circuit=circuits[0], term_side='Z', site=sites[1]),
            CircuitTermination(circuit=circuits[1], term_side='A', site=sites[0]),
            CircuitTermination(circuit=circuits[1], term_side='Z', site=sites[1]),
        )
        CircuitTermination.objects.bulk_create(circuit_terminations)

        cls.form_data = {
            'circuit': circuits[2].pk,
            'term_side': 'A',
            'site': sites[2].pk,
            'description': 'New description',
        }

        cls.csv_data = (
            "circuit,term_side,site,description",
            "Circuit 3,A,Site 1,Foo",
            "Circuit 3,Z,Site 1,Bar",
        )

        cls.csv_update_data = (
            "id,port_speed,description",
            f"{circuit_terminations[0].pk},100,New description7",
            f"{circuit_terminations[1].pk},200,New description8",
            f"{circuit_terminations[2].pk},300,New description9",
        )

        cls.bulk_edit_data = {
            'port_speed': 400,
            'description': 'New description',
        }

    @override_settings(EXEMPT_VIEW_PERMISSIONS=['*'])
    def test_trace(self):
        device = create_test_device('Device 1')

        circuittermination = CircuitTermination.objects.first()
        interface = Interface.objects.create(
            device=device,
            name='Interface 1'
        )
        Cable(a_terminations=[circuittermination], b_terminations=[interface]).save()

        response = self.client.get(reverse('circuits:circuittermination_trace', kwargs={'pk': circuittermination.pk}))
        self.assertHttpStatus(response, 200)


class CircuitGroupTestCase(ViewTestCases.OrganizationalObjectViewTestCase):
    model = CircuitGroup

    @classmethod
    def setUpTestData(cls):

        circuit_groups = (
            CircuitGroup(name='Circuit Group 1', slug='circuit-group-1'),
            CircuitGroup(name='Circuit Group 2', slug='circuit-group-2'),
            CircuitGroup(name='Circuit Group 3', slug='circuit-group-3'),
        )
        CircuitGroup.objects.bulk_create(circuit_groups)

        tags = create_tags('Alpha', 'Bravo', 'Charlie')

        cls.form_data = {
            'name': 'Circuit Group X',
            'slug': 'circuit-group-x',
            'description': 'A new Circuit Group',
            'tags': [t.pk for t in tags],
        }

        cls.csv_data = (
            "name,slug",
            "Circuit Group 4,circuit-group-4",
            "Circuit Group 5,circuit-group-5",
            "Circuit Group 6,circuit-group-6",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{circuit_groups[0].pk},Circuit Group 7,New description7",
            f"{circuit_groups[1].pk},Circuit Group 8,New description8",
            f"{circuit_groups[2].pk},Circuit Group 9,New description9",
        )

        cls.bulk_edit_data = {
            'description': 'Foo',
        }


class CircuitGroupAssignmentTestCase(
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase
):
    model = CircuitGroupAssignment

    @classmethod
    def setUpTestData(cls):

        circuit_groups = (
            CircuitGroup(name='Circuit Group 1', slug='circuit-group-1'),
            CircuitGroup(name='Circuit Group 2', slug='circuit-group-2'),
            CircuitGroup(name='Circuit Group 3', slug='circuit-group-3'),
            CircuitGroup(name='Circuit Group 4', slug='circuit-group-4'),
        )
        CircuitGroup.objects.bulk_create(circuit_groups)

        provider = Provider.objects.create(name='Provider 1', slug='provider-1')
        circuittype = CircuitType.objects.create(name='Circuit Type 1', slug='circuit-type-1')

        circuits = (
            Circuit(cid='Circuit 1', provider=provider, type=circuittype),
            Circuit(cid='Circuit 2', provider=provider, type=circuittype),
            Circuit(cid='Circuit 3', provider=provider, type=circuittype),
            Circuit(cid='Circuit 4', provider=provider, type=circuittype),
        )
        Circuit.objects.bulk_create(circuits)

        assignments = (
            CircuitGroupAssignment(
                group=circuit_groups[0],
                circuit=circuits[0],
                priority=CircuitPriorityChoices.PRIORITY_PRIMARY
            ),
            CircuitGroupAssignment(
                group=circuit_groups[1],
                circuit=circuits[1],
                priority=CircuitPriorityChoices.PRIORITY_SECONDARY
            ),
            CircuitGroupAssignment(
                group=circuit_groups[2],
                circuit=circuits[2],
                priority=CircuitPriorityChoices.PRIORITY_TERTIARY
            ),
        )
        CircuitGroupAssignment.objects.bulk_create(assignments)

        tags = create_tags('Alpha', 'Bravo', 'Charlie')

        cls.form_data = {
            'group': circuit_groups[3].pk,
            'circuit': circuits[3].pk,
            'priority': CircuitPriorityChoices.PRIORITY_INACTIVE,
            'tags': [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            'priority': CircuitPriorityChoices.PRIORITY_INACTIVE,
        }
