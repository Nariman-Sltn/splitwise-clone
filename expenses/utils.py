from .models import ActivityLog

def log_activity(group, user, message):
    ActivityLog.objects.create(
        group=group,
        user=user,
        message=message
    )