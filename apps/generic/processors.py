__author__ = 'mark'
from models import FormName, ExtraFormContent
from django.template import Library, Node, TemplateSyntaxError

"""
Attempting to add a template tag that works via {% display_pre_text_segment formname field %}
add a load statement: {%  load display_pre_text_segment %} before the template tag call
needs to be enabled in context processors section of settings.

Currently fails with __init__ requires 4 arguments received 2.
I can't see how it is getting initialized
"""


register = Library()

class display_pre_text_segment(Node):


    def __init__(self, pp, formname,field_name):
        self.pp = pp
        self.formname   = formname
        self.field_name = field_name

    def render(self, context):
        result = ExtraFormContent.objects.get(form_name=formname,field_name=field_name)

        context['display_text_segment'] = result.field_pre_text
        return ''


    def display_pre_field_text(parser, token):
        bits = token.contents.split()

        #print bits[1]
        #print bits[2]

        if len(bits) != 3:
            raise TemplateSyntaxError, "display_pre_field_text tag takes exactly two arguments"
        return display_pre_text_segment("pre", bits[1], bits[2])

    display_pre_field_text = register.tag(display_pre_field_text)


