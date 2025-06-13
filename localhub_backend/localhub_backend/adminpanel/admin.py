from django.contrib import admin
from .models import Analytics, SupportTicket
from moderation.models import Report, ModerationLog

@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'active_users', 'revenue', 'new_listings', 'sessions')
    list_filter = ('date',)
    search_fields = ('date',)

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'resolved_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'issue')
    actions = ['mark_in_progress', 'mark_resolved']

    @admin.action(description='Mark selected tickets as In Progress')
    def mark_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f"{updated} ticket(s) marked as In Progress.")

    @admin.action(description='Mark selected tickets as Resolved')
    def mark_resolved(self, request, queryset):
        updated = queryset.update(status='resolved')
        self.message_user(request, f"{updated} ticket(s) marked as Resolved.")

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'reported_by', 'reported_user', 'reason', 'created_at')
    list_filter = ('reason', 'created_at')
    search_fields = ('reported_by__username', 'reported_user__username')
    actions = ['approve_report', 'ban_user', 'delete_content']

    @admin.action(description='Approve selected reports')
    def approve_report(self, request, queryset):
        for report in queryset:
            ModerationLog.objects.create(
                moderator=request.user,
                action_taken='approved',
                report=report,
                comments='Report approved.'
            )
        self.message_user(request, f"{queryset.count()} report(s) approved.")

    @admin.action(description='Ban reported users')
    def ban_user(self, request, queryset):
        for report in queryset:
            if report.reported_user:
                report.reported_user.is_active = False
                report.reported_user.save()
                ModerationLog.objects.create(
                    moderator=request.user,
                    action_taken='banned',
                    report=report,
                    comments='User banned.'
                )
        self.message_user(request, f"{queryset.count()} user(s) banned.")

    @admin.action(description='Delete reported content')
    def delete_content(self, request, queryset):
        for report in queryset:
            content = report.content_object
            if content:
                content.delete()
                ModerationLog.objects.create(
                    moderator=request.user,
                    action_taken='content_deleted',
                    report=report,
                    comments='Content deleted.'
                )
        self.message_user(request, f"{queryset.count()} content item(s) deleted.")

@admin.register(ModerationLog)
class ModerationLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'moderator', 'action_taken', 'report', 'timestamp')
    list_filter = ('action_taken', 'timestamp')
    search_fields = ('moderator__username', 'report__id')
