from django.shortcuts import redirect
from django.urls.base import reverse_lazy


class InfoRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.institution or not request.user.phone_number:
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
