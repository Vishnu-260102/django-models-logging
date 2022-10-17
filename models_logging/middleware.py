try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

from . import _local
from .settings import MERGE_CHANGES
from .utils import create_revision_with_changes

from user_agents import parse



class LoggingStackMiddleware(MiddlewareMixin):

    def process_request(self, request):
        _local.user = request.user
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        _local.ip_address=ip
        _local.user_agent = parse(request.META['HTTP_USER_AGENT'])

    def process_response(self, request, response):
        if MERGE_CHANGES and _local.stack_changes:
            self.create_revision(_local)
        return response
    
    def create_revision(self, _local):
        # this method for overriding and call create_revision_with_changes async maybe

        create_revision_with_changes(_local.stack_changes.values())
        _local.stack_changes = {}