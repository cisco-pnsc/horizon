from django import template

import plugins.api.razor as razor_api

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_all_tags(context):
	return razor_api.get_all_tags()
