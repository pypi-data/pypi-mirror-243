from unittest import expectedFailure
from django.conf import settings
from django.shortcuts import render
from django_guard import errors as e


class GuardMiddleware(object):
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def get_threshold(self):
        try:
            gt = settings.GUARD_THRESHOLD
        except AttributeError:
            raise e.SettingsException('GUARD_THRESHOLD is not set')

        self.memory_threshold = gt.get('memory', 80)

    def __call__(self, request):
        self.get_threshold()
        import psutil
        server_usage = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
        if server_usage > self.memory_threshold:
            return render(
                request,
                'django_guard/503.html',
                context={"msg": f"The memory usage is {server_usage:.2f}%, and threshold is {self.memory_threshold}%."},
                status=503,
            )
        else:
            return self.get_response(request)
