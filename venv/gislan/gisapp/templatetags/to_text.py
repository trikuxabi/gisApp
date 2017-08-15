from django import template

register = template.Library()

@register.filter
def to_text(f):
	testua = f.read()
	return testua.decode('utf8')