from django import template

register = template.Library()


@register.simple_tag
def my_tag(data, data_list, indexes):
    indexes.append(data_list.index(data))
    return data_list.index(data)


@register.simple_tag
def getIndex(value, array):
    return array.index(value)