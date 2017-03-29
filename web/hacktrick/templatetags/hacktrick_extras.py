from django import template
from hacktrick.models import UserTraining
register = template.Library()


@register.filter(name='calculate_percent')
def calculate_training_percent(training):
    accepted_count = UserTraining.objects.filter(first_selection=training).count()
    percent = int((accepted_count * 100) / training.capacity)
    return percent
