from django.http import JsonResponse

__all__ = ('JSONResponseMixin',)


class JSONResponseMixin(object):
    """A mixin that can be used to render a JSON response."""

    def render_to_json_response(self, context, **response_kwargs):
        """Return a JSON response, transforming 'context' for the payload."""
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """Return an object to be serialized as JSON by json.dumps()."""
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context
