from django import template


register = template.Library()


@register.filter('join_prefetched')
def join_prefetched(prefetched_item_set_all):
    """returns a string made up of the name attribute for each item supplied in all prefetched items set"""
    name_list = sorted(
        [item.name for item in prefetched_item_set_all],
        key=lambda item: item,
    )
    return ', '.join(name_list)



