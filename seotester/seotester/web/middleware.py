from django.http import Http404


class OnlyAdminMiddleware:
    """
    Raises an Http404 error for any page request from a banned IP.  IP addresses
    may be added to the list of banned IPs via the Django admin.

    The banned users do not actually receive the 404 error--instead they get
    an "Internal Server Error", effectively eliminating any access to the site.
    """

    def process_request(self, request):
        if "/admin/" not in request.path and not request.user.is_staff:
            raise Http404("Must be admin user!")

