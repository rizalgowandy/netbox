from collections import defaultdict

from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from utilities.ordering import naturalize
from .forms.widgets import ColorSelect
from .validators import ColorValidator

__all__ = (
    'ColorField',
    'CounterCacheField',
    'NaturalOrderingField',
    'RestrictedGenericForeignKey',
)


class ColorField(models.CharField):
    default_validators = [ColorValidator]
    description = "A hexadecimal RGB color code"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 6
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorSelect
        kwargs['help_text'] = mark_safe(_('RGB color in hexadecimal. Example: ') + '<code>00ff00</code>')
        return super().formfield(**kwargs)


class NaturalOrderingField(models.CharField):
    """
    A field which stores a naturalized representation of its target field, to be used for ordering its parent model.

    :param target_field: Name of the field of the parent model to be naturalized
    :param naturalize_function: The function used to generate a naturalized value (optional)
    """
    description = "Stores a representation of its target field suitable for natural ordering"

    def __init__(self, target_field, naturalize_function=naturalize, *args, **kwargs):
        self.target_field = target_field
        self.naturalize_function = naturalize_function
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """
        Generate a naturalized value from the target field
        """
        original_value = getattr(model_instance, self.target_field)
        naturalized_value = self.naturalize_function(original_value, max_length=self.max_length)
        setattr(model_instance, self.attname, naturalized_value)

        return naturalized_value

    def deconstruct(self):
        kwargs = super().deconstruct()[3]  # Pass kwargs from CharField
        kwargs['naturalize_function'] = self.naturalize_function
        return (
            self.name,
            'utilities.fields.NaturalOrderingField',
            [self.target_field],
            kwargs,
        )


class RestrictedGenericForeignKey(GenericForeignKey):

    # Replicated largely from GenericForeignKey. Changes include:
    #  1. Capture restrict_params from RestrictedPrefetch (hack)
    #  2. If restrict_params is set, call restrict() on the queryset for
    #     the related model
    def get_prefetch_querysets(self, instances, querysets=None):
        restrict_params = {}
        custom_queryset_dict = {}

        # Compensate for the hack in RestrictedPrefetch
        if type(querysets) is dict:
            restrict_params = querysets

        elif querysets is not None:
            for queryset in querysets:
                ct_id = self.get_content_type(
                    model=queryset.query.model, using=queryset.db
                ).pk
                if ct_id in custom_queryset_dict:
                    raise ValueError(
                        "Only one queryset is allowed for each content type."
                    )
                custom_queryset_dict[ct_id] = queryset

        # For efficiency, group the instances by content type and then do one
        # query per model
        fk_dict = defaultdict(set)
        # We need one instance for each group in order to get the right db:
        instance_dict = {}
        ct_attname = self.model._meta.get_field(self.ct_field).get_attname()
        for instance in instances:
            # We avoid looking for values if either ct_id or fkey value is None
            ct_id = getattr(instance, ct_attname)
            if ct_id is not None:
                # Check if the content type actually exists
                if not self.get_content_type(id=ct_id, using=instance._state.db).model_class():
                    continue

                fk_val = getattr(instance, self.fk_field)
                if fk_val is not None:
                    fk_dict[ct_id].add(fk_val)
                    instance_dict[ct_id] = instance

        ret_val = []
        for ct_id, fkeys in fk_dict.items():
            if ct_id in custom_queryset_dict:
                # Return values from the custom queryset, if provided.
                ret_val.extend(custom_queryset_dict[ct_id].filter(pk__in=fkeys))
            else:
                instance = instance_dict[ct_id]
                ct = self.get_content_type(id=ct_id, using=instance._state.db)
                qs = ct.model_class().objects.filter(pk__in=fkeys)
                if restrict_params:
                    qs = qs.restrict(**restrict_params)
                ret_val.extend(qs)

        # For doing the join in Python, we have to match both the FK val and the
        # content type, so we use a callable that returns a (fk, class) pair.
        def gfk_key(obj):
            ct_id = getattr(obj, ct_attname)
            if ct_id is None:
                return None
            else:
                if model := self.get_content_type(
                    id=ct_id, using=obj._state.db
                ).model_class():
                    return (
                        model._meta.pk.get_prep_value(getattr(obj, self.fk_field)),
                        model,
                    )
                return None

        return (
            ret_val,
            lambda obj: (obj.pk, obj.__class__),
            gfk_key,
            True,
            self.name,
            False,
        )


class CounterCacheField(models.BigIntegerField):
    """
    Counter field to keep track of related model counts.
    """
    def __init__(self, to_model, to_field, *args, **kwargs):
        if not isinstance(to_model, str):
            raise TypeError(
                _("%s(%r) is invalid. to_model parameter to CounterCacheField must be "
                  "a string in the format 'app.model'")
                % (
                    self.__class__.__name__,
                    to_model,
                )
            )

        if not isinstance(to_field, str):
            raise TypeError(
                _("%s(%r) is invalid. to_field parameter to CounterCacheField must be "
                  "a string in the format 'field'")
                % (
                    self.__class__.__name__,
                    to_field,
                )
            )

        self.to_model_name = to_model
        self.to_field_name = to_field

        kwargs['default'] = kwargs.get('default', 0)
        kwargs['editable'] = False

        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["to_model"] = self.to_model_name
        kwargs["to_field"] = self.to_field_name
        return name, path, args, kwargs
