from .models import Employee, Nationality, Certification, Degree
from django.contrib import admin
from django.utils.html import format_html


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action', 'object_repr', 'object_id', 'timestamp', 'actor', 'get_changes_display']
    list_filter = ['action', 'timestamp', 'actor']
    search_fields = ['actor__username', 'changes']

    def get_changes_display(self, obj):
        changes = obj.changes
        if changes:
            return format_html('<pre>{}</pre>', changes)
        return "-"

    get_changes_display.short_description = 'Changes'


admin.site.register(Employee)
admin.site.register(Nationality)
admin.site.register(Certification)
admin.site.register(Degree)

