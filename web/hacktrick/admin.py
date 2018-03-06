from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import (
    Sponsor,
    Contributor,
    FAQ,
    BugMiner,
    GameOfPwners,
    DemoRoom,
    CsAward,
    ConferenceSlot,
    Speaker,
    Training,
    TrainingDocument,
    Ticket,
    TicketComment,
    Setting,
    Speak,
    UserTraining,
    Mail
)


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'order', 'website']
    list_filter = ['category']
    search_fields = ['name']
    ordering = ['order']


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'title', 'mission', 'status', 'twitter',
                    'linkedin']
    search_fields = ['full_name', 'title']
    list_filter = ['status']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'order']
    search_fields = ['question']

@admin.register(BugMiner)
class BugMinerAdmin(admin.ModelAdmin):
    list_display = ['header', 'text_area']
    search_fields = ['header']

@admin.register(GameOfPwners)
class GameOfPwnersAdmin(admin.ModelAdmin):
    list_display = ['header', 'text_area']
    search_fields = ['header']

@admin.register(DemoRoom)
class DemoRoomAdmin(admin.ModelAdmin):
    list_display = ['header', 'text_area']
    search_fields = ['header']

@admin.register(CsAward)
class CsAwardAdmin(admin.ModelAdmin):
    list_display = ['header', 'text_area']
    search_fields = ['header']

@admin.register(ConferenceSlot)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ['date']


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'title', 'institution', 'facebook', 'twitter',
                    'linkedin', 'is_visible']
    search_fields = ['full_name', 'title', 'institution']


@admin.register(Speak)
class SpeakAdmin(admin.ModelAdmin):
    list_display = ['title', 'hall', 'starting_time', 'ending_time', 'slot',
                    'speaker']
    search_fields = ['title', 'hall', 'speaker__full_name']
    list_filter = ['speaker', 'slot']


class TrainingInline(admin.StackedInline):
    model = TrainingDocument
    can_delete = True
    extra = 2


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['title', 'capacity', 'date']
    list_filter = ['instructor']
    search_fields = ['title', 'instructor__user__first_name']
    inlines = [TrainingInline]
    filter_horizontal = ['instructor']


@admin.register(TrainingDocument)
class TrainingDocument(admin.ModelAdmin):
    list_display = ['name', 'document_url', 'training']
    search_fields = ['name']
    list_filter = ['training']


class TicketInline(admin.StackedInline):
    model = TicketComment
    can_delete = True
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'ticket_status', 'date', 'user']
    search_fields = ['user__first_name', 'user__last_name']
    list_filter = ['user']
    inlines = [TicketInline]


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'ticket', 'date', 'user']
    list_filter = ['ticket', 'user']
    search_fields = ['user__first_name', 'user__last_name', 'ticket__title',
                     'comment']
    raw_id_fields = ['ticket']
    readonly_fields = ['user']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['city',
                    'place_fullname',
                    'expected_participant',
                    'expected_speaker',
                    'place',
                    'date',
                    'starting_date',
                    'address']


@admin.register(UserTraining)
class UserTrainingAdmin(admin.ModelAdmin):
    list_display = [
        'get_first_selection_title',
        'accepted_training',
        'get_username',
    ]
    search_fields = ['user__first_name', 'user__last_name']

@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ['type', 'title']
