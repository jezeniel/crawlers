from datetime import datetime

from django.contrib import admin

from crawlers.models import Cinema, Movie


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    actions = ['fetch_schedule']

    def fetch_schedule(self, request, queryset):
        for obj in queryset:
            obj.fetch()


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'cinema', 'room', 'genre', 'price', 'view_schedule', 'created_at'
    )

    def view_schedule(self, obj):
        if not obj.schedule:
            return None
        schedule = obj.schedule.split(', ')
        return [
            datetime.strptime(s, '%Y-%m-%d %I:%M %p').strftime('%I:%M %p')
            for s in schedule
        ]

    view_schedule.short_description = "Schedule"
