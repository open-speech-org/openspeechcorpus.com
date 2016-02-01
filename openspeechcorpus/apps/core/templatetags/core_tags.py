from django import template
from openspeechcorpus.apps.core import utils as core_utils
register = template.Library()

@register.filter(name="audio_length")
def audio_length(length):
    return core_utils.human_readable_length(length)
