from django.contrib import admin

from .models import (
    Sponsor,
    Contributor,
    CFP,
    FAQ,
    ConferenceSlot,
    Speaker,
    Training,
    TrainingDocument,
    Ticket,
    TicketComment,
    Setting
)


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'order']


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'title', 'mission']


@admin.register(CFP)
class CFPAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'url', 'order']


@admin.register(ConferenceSlot)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ['date', 'starting_time', 'ending_time']


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'image', 'corporate']


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['title', 'capacity', 'reserve_quota']


@admin.register(TrainingDocument)
class TrainingDocument(admin.ModelAdmin):
    list_display = ['name', 'document', 'is_public']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['status', 'date']


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'date', ]


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['place', 'starting_date', 'ending_date', 'address']
