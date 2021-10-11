from advertiser_management.views import get_client_ip


class FetchIpAddressMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.ipAddress = get_client_ip(request)

        response = self.get_response(request)
        return response
