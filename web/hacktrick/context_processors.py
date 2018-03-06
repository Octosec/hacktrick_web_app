from .models import Setting


def get_settings(request):
    settings = Setting.objects.first()
    project_settings = {}
    if settings:
        project_settings = {
            "training_selection": settings.training_selection,
            "participant_selection": settings.participant_selection,
            #"participant_accept": settings.participant_accept
        }

    return {
        'project_settings': project_settings
    }