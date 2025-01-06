import json
from typing import Dict, Any
from urllib.parse import quote

from django import template
from django.urls import NoReverseMatch, reverse

from core.models import ObjectType
from utilities.forms import get_selected_values, TableConfigForm
from utilities.views import get_viewname

__all__ = (
    'applied_filters',
    'as_range',
    'divide',
    'get_item',
    'get_key',
    'humanize_megabytes',
    'humanize_speed',
    'icon_from_status',
    'kg_to_pounds',
    'meters_to_feet',
    'percentage',
    'querystring',
    'startswith',
    'status_from_tag',
    'table_config_form',
    'utilization_graph',
    'validated_viewname',
    'viewname',
)

register = template.Library()


#
# Filters
#


@register.filter()
def viewname(model, action):
    """
    Return the view name for the given model and action. Does not perform any validation.
    """
    return get_viewname(model, action)


@register.filter()
def validated_viewname(model, action):
    """
    Return the view name for the given model and action if valid, or None if invalid.
    """
    viewname = get_viewname(model, action)

    # Validate the view name
    try:
        reverse(viewname)
        return viewname
    except NoReverseMatch:
        return None


@register.filter()
def humanize_speed(speed):
    """
    Humanize speeds given in Kbps. Examples:

        1544 => "1.544 Mbps"
        100000 => "100 Mbps"
        10000000 => "10 Gbps"
    """
    if not speed:
        return ''
    if speed >= 1000000000 and speed % 1000000000 == 0:
        return '{} Tbps'.format(int(speed / 1000000000))
    elif speed >= 1000000 and speed % 1000000 == 0:
        return '{} Gbps'.format(int(speed / 1000000))
    elif speed >= 1000 and speed % 1000 == 0:
        return '{} Mbps'.format(int(speed / 1000))
    elif speed >= 1000:
        return '{} Mbps'.format(float(speed) / 1000)
    else:
        return '{} Kbps'.format(speed)


@register.filter()
def humanize_megabytes(mb):
    """
    Express a number of megabytes in the most suitable unit (e.g. gigabytes, terabytes, etc.).
    """
    if not mb:
        return ""

    PB_SIZE = 1000000000
    TB_SIZE = 1000000
    GB_SIZE = 1000

    if mb >= PB_SIZE:
        return f"{mb / PB_SIZE:.2f} PB"
    if mb >= TB_SIZE:
        return f"{mb / TB_SIZE:.2f} TB"
    if mb >= GB_SIZE:
        return f"{mb / GB_SIZE:.2f} GB"
    return f"{mb} MB"


@register.filter()
def divide(x, y):
    """
    Return x/y (rounded).
    """
    if x is None or y is None:
        return None
    return round(x / y)


@register.filter()
def percentage(x, y):
    """
    Return x/y as a percentage.
    """
    if x is None or y is None:
        return None

    return round(x / y * 100, 1)


@register.filter()
def as_range(n):
    """
    Return a range of n items.
    """
    try:
        int(n)
    except TypeError:
        return list()
    return range(n)


@register.filter()
def meters_to_feet(n):
    """
    Convert a length from meters to feet.
    """
    return float(n) * 3.28084


@register.filter()
def kg_to_pounds(n):
    """
    Convert a weight from kilograms to pounds.
    """
    return float(n) * 2.204623


@register.filter("startswith")
def startswith(text: str, starts: str) -> bool:
    """
    Template implementation of `str.startswith()`.
    """
    if isinstance(text, str):
        return text.startswith(starts)
    return False


@register.filter
def get_key(value: Dict, arg: str) -> Any:
    """
    Template implementation of `dict.get()`, for accessing dict values
    by key when the key is not able to be used in a template. For
    example, `{"ui.colormode": "dark"}`.
    """
    return value.get(arg, None)


@register.filter
def get_item(value: object, attr: str) -> Any:
    """
    Template implementation of `__getitem__`, for accessing the `__getitem__` method
    of a class from a template.
    """
    return value[attr]


@register.filter
def status_from_tag(tag: str = "info") -> str:
    """
    Determine Bootstrap theme status/level from Django's Message.level_tag.
    """
    status_map = {
        'warning': 'warning',
        'success': 'success',
        'error': 'danger',
        'danger': 'danger',
        'debug': 'info',
        'info': 'info',
    }
    return status_map.get(tag.lower(), 'info')


@register.filter
def icon_from_status(status: str = "info") -> str:
    """
    Determine icon class name from Bootstrap theme status/level.
    """
    icon_map = {
        'warning': 'alert',
        'success': 'check-circle',
        'danger': 'alert',
        'info': 'information',
    }
    return icon_map.get(status.lower(), 'information')


#
# Tags
#

@register.simple_tag()
def querystring(request, **kwargs):
    """
    Append or update the page number in a querystring.
    """
    querydict = request.GET.copy()
    for k, v in kwargs.items():
        if v is not None:
            querydict[k] = str(v)
        elif k in querydict:
            querydict.pop(k)
    querystring = querydict.urlencode(safe='/')
    if querystring:
        return '?' + querystring
    else:
        return ''


@register.inclusion_tag('helpers/utilization_graph.html')
def utilization_graph(utilization, warning_threshold=75, danger_threshold=90):
    """
    Display a horizontal bar graph indicating a percentage of utilization.
    """
    if utilization == 100:
        bar_class = 'bg-secondary'
    elif danger_threshold and utilization >= danger_threshold:
        bar_class = 'bg-danger'
    elif warning_threshold and utilization >= warning_threshold:
        bar_class = 'bg-warning'
    elif warning_threshold or danger_threshold:
        bar_class = 'bg-success'
    else:
        bar_class = 'bg-gray'
    return {
        'utilization': utilization,
        'bar_class': bar_class,
    }


@register.inclusion_tag('helpers/table_config_form.html')
def table_config_form(table, table_name=None):
    return {
        'table_name': table_name or table.__class__.__name__,
        'form': TableConfigForm(table=table),
    }


@register.inclusion_tag('helpers/applied_filters.html', takes_context=True)
def applied_filters(context, model, form, query_params):
    """
    Display the active filters for a given filter form.
    """
    user = context['request'].user
    form.is_valid()  # Ensure cleaned_data has been set

    applied_filters = []
    for filter_name in form.changed_data:
        if filter_name not in form.cleaned_data:
            continue

        querydict = query_params.copy()
        if filter_name not in querydict:
            continue

        # Skip saved filters, as they're displayed alongside the quick search widget
        if filter_name == 'filter_id':
            continue

        bound_field = form.fields[filter_name].get_bound_field(form, filter_name)
        querydict.pop(filter_name)
        display_value = ', '.join([str(v) for v in get_selected_values(form, filter_name)])

        applied_filters.append({
            'name': filter_name,
            'value': form.cleaned_data[filter_name],
            'link_url': f'?{querydict.urlencode()}',
            'link_text': f'{bound_field.label}: {display_value}',
        })

    save_link = None
    if user.has_perm('extras.add_savedfilter') and 'filter_id' not in context['request'].GET:
        object_type = ObjectType.objects.get_for_model(model).pk
        parameters = json.dumps(dict(context['request'].GET.lists()))
        url = reverse('extras:savedfilter_add')
        save_link = f"{url}?object_types={object_type}&parameters={quote(parameters)}"

    return {
        'applied_filters': applied_filters,
        'save_link': save_link,
    }
