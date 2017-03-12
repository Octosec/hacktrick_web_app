from django.contrib import admin

from .models import (
    Sponsor,
    Contributor,
    FAQ,
    ConferenceSlot,
    Speaker,
    Training,
    TrainingDocument,
    Ticket,
    TicketComment,
    Setting,
    Speak,
    UserTraining
)


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'order']


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'title', 'mission']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'order']


@admin.register(ConferenceSlot)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ['date']


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'image', 'title', 'institution']


@admin.register(Speak)
class SpeakAdmin(admin.ModelAdmin):
    list_display = ['title', 'starting_time', 'ending_time', 'slot']


class TrainingInline(admin.StackedInline):
    model = TrainingDocument
    can_delete = True
    extra = 2


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['title', 'capacity', 'reserve_quota']
    inlines = [TrainingInline]

@admin.register(TrainingDocument)
class TrainingDocument(admin.ModelAdmin):
    list_display = ['name', 'document_url']


class TicketInline(admin.StackedInline):
    model = TicketComment
    can_delete = True
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'ticket_status', 'date']
    inlines = [TicketInline]


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'date', ]


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['place', 'date', 'starting_date', 'address']


@admin.register(UserTraining)
class UserTrainingAdmin(admin.ModelAdmin):
    list_display = [
        'get_first_selection_title',
        'get_second_selection_title',
        'get_accepted_selection_title',
        'get_username'
    ]