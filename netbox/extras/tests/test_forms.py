from django.test import TestCase

from core.models import ObjectType
from dcim.forms import SiteForm
from dcim.models import Site
from extras.choices import CustomFieldTypeChoices
from extras.forms import SavedFilterForm
from extras.models import CustomField, CustomFieldChoiceSet


class CustomFieldModelFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        object_type = ObjectType.objects.get_for_model(Site)
        choice_set = CustomFieldChoiceSet.objects.create(
            name='Choice Set 1',
            extra_choices=(('a', 'A'), ('b', 'B'), ('c', 'C'))
        )

        cf_text = CustomField.objects.create(name='text', type=CustomFieldTypeChoices.TYPE_TEXT)
        cf_text.object_types.set([object_type])

        cf_longtext = CustomField.objects.create(name='longtext', type=CustomFieldTypeChoices.TYPE_LONGTEXT)
        cf_longtext.object_types.set([object_type])

        cf_integer = CustomField.objects.create(name='integer', type=CustomFieldTypeChoices.TYPE_INTEGER)
        cf_integer.object_types.set([object_type])

        cf_integer = CustomField.objects.create(name='decimal', type=CustomFieldTypeChoices.TYPE_DECIMAL)
        cf_integer.object_types.set([object_type])

        cf_boolean = CustomField.objects.create(name='boolean', type=CustomFieldTypeChoices.TYPE_BOOLEAN)
        cf_boolean.object_types.set([object_type])

        cf_date = CustomField.objects.create(name='date', type=CustomFieldTypeChoices.TYPE_DATE)
        cf_date.object_types.set([object_type])

        cf_datetime = CustomField.objects.create(name='datetime', type=CustomFieldTypeChoices.TYPE_DATETIME)
        cf_datetime.object_types.set([object_type])

        cf_url = CustomField.objects.create(name='url', type=CustomFieldTypeChoices.TYPE_URL)
        cf_url.object_types.set([object_type])

        cf_json = CustomField.objects.create(name='json', type=CustomFieldTypeChoices.TYPE_JSON)
        cf_json.object_types.set([object_type])

        cf_select = CustomField.objects.create(
            name='select',
            type=CustomFieldTypeChoices.TYPE_SELECT,
            choice_set=choice_set
        )
        cf_select.object_types.set([object_type])

        cf_multiselect = CustomField.objects.create(
            name='multiselect',
            type=CustomFieldTypeChoices.TYPE_MULTISELECT,
            choice_set=choice_set
        )
        cf_multiselect.object_types.set([object_type])

        cf_object = CustomField.objects.create(
            name='object',
            type=CustomFieldTypeChoices.TYPE_OBJECT,
            related_object_type=ObjectType.objects.get_for_model(Site)
        )
        cf_object.object_types.set([object_type])

        cf_multiobject = CustomField.objects.create(
            name='multiobject',
            type=CustomFieldTypeChoices.TYPE_MULTIOBJECT,
            related_object_type=ObjectType.objects.get_for_model(Site)
        )
        cf_multiobject.object_types.set([object_type])

    def test_empty_values(self):
        """
        Test that empty custom field values are stored as null
        """
        form = SiteForm({
            'name': 'Site 1',
            'slug': 'site-1',
            'status': 'active',
        })
        self.assertTrue(form.is_valid())
        instance = form.save()

        for field_type, _ in CustomFieldTypeChoices.CHOICES:
            self.assertIn(field_type, instance.custom_field_data)
            self.assertIsNone(instance.custom_field_data[field_type])


class SavedFilterFormTest(TestCase):

    def test_basic_submit(self):
        """
        Test form submission and validation
        """
        form = SavedFilterForm({
            'name': 'test-sf',
            'slug': 'test-sf',
            'object_types': [ObjectType.objects.get_for_model(Site).pk],
            'weight': 100,
            'parameters': {
                "status": [
                    "active"
                ]
            }
        })
        self.assertTrue(form.is_valid())
        form.save()
