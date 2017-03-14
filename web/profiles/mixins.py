from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.contrib import messages

from hacktrick.models import Setting

class InfoRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.institution or not request.user.phone_number \
                or not request.user.first_name or not request.user.last_name:
            return redirect(reverse_lazy('profiles:profile'))
        return super(InfoRequiredMixin, self).dispatch(request, *args, **kwargs)


class SuperuserOrModeratorRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type not in [0, 1]:
            return redirect(reverse_lazy('hacktrick:index'))
        return super(SuperuserOrModeratorRequiredMixin, self).dispatch(request, *args, **kwargs)


class InstructorRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.user_type == 2:
            return redirect(reverse_lazy('hacktrick:index'))
        return super(InstructorRequiredMixin, self).dispatch(request, *args, **kwargs)


class ParticipantRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.user_type == 3:
            return redirect(reverse_lazy('hacktrick:index'))
        return super(ParticipantRequiredMixin, self).dispatch(request, *args, **kwargs)


class TrainingSelectionRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            setting = Setting.objects.first()
            if setting==None or setting.training_selection == False:
                messages.add_message(self.request, messages.ERROR, 'Eğitim seçimi henüz açılmamıştır.')
                return redirect(reverse_lazy('profiles:profile'))
        except:
            pass
        return super(TrainingSelectionRequiredMixin, self).dispatch(request, *args, **kwargs)


class ParticipantSelectionRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            setting = Setting.objects.first()
            if setting==None or setting.participant_selection == False:
                messages.add_message(self.request, messages.ERROR, 'Katılımcı seçimi henüz açılmamıştır.')
                return redirect(reverse_lazy('profiles:profile'))
        except:
            pass
        return super(ParticipantSelectionRequiredMixin, self).dispatch(request, *args, **kwargs)


class ParticipantTrainingAcceptRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            setting = Setting.objects.first()
            if setting==None or setting.participant_accept == False:
                messages.add_message(self.request, messages.ERROR, 'Eğitim onay henüz açılmamıştır.')
                return redirect(reverse_lazy('profiles:profile'))
        except:
            pass
        return super(ParticipantTrainingAcceptRequiredMixin, self).dispatch(request, *args, **kwargs)
