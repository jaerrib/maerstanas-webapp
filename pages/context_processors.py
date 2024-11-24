from game_messages.models import SystemNotice


def total_notifications(request):
    if request.user.is_authenticated:
        total_system_notices = SystemNotice.objects.filter(user=request.user).count()
    else:
        total_system_notices = 0
    return {
        "total_system_notices": total_system_notices,
    }
