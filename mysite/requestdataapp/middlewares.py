from typing import Any
from django.http import HttpRequest
import time
from django.shortcuts import render


def set_useragent_on_request_middlewares(get_response):

    print('initial call')

    def middleware(request: HttpRequest):
        print('before get response')
        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)
        print('after get response')
        return response

    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print('requests count', self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print('responses count', self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print('got', self.exceptions_count, 'exceptions')


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.last_requests_time = time.time()
        self.requests_time = 0
        self.remote_ip = ''

    def __call__(self, request: HttpRequest):
        print('last requests time', self.last_requests_time)
        self.requests_time = time.time()
        print('new requests time', self.requests_time)

        time_between_requests = self.requests_time - self.last_requests_time
        print('time:', time_between_requests)

        if (self.remote_ip == request.META['REMOTE_ADDR']) and time_between_requests < 2:
            return render(request, "requestdataapp/error.html")

        response = self.get_response(request)
        self.last_requests_time = time.time()
        self.remote_ip = request.META['REMOTE_ADDR']
        print('requests ip', self.remote_ip)
        return response
