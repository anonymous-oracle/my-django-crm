from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


# making sure that only the organisers have access to the views
class OrganiserAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organiser:
            # return self.handle_no_permission()
            return redirect("leads:home")
        return super().dispatch(request, *args, **kwargs)