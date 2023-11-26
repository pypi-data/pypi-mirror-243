import datetime
import enum

import httpx


class APNSResponse:
    def __init__(self, httpx_response: httpx.Response):
        self.httpx_response = httpx_response

        headers = self.httpx_response.headers
        request_headers = self.httpx_response.request.headers

        timestamp = request_headers.get('apns-unix-time', None)

        self.status_code = self.httpx_response.status_code
        self.apns_id = headers.get('apns-id', None)
        self.apns_unique_id = headers.get('apns-unique-id', None)
        self.timestamp = Time(int(timestamp) * 1000) if timestamp else None

    @property
    def is_success(self) -> bool:
        return self.httpx_response.is_success


class Time:
    def __init__(self, timestamp):
        self.timestamp = timestamp

    @property
    def time(self):
        return datetime.datetime.fromtimestamp(self.timestamp / 1000)


class Reason(enum.Enum):
    bad_collapse_id = "BadCollapseId"
    bad_device_token = "BadDeviceToken"
    bad_expiration_date = "BadExpirationDate"
    bad_message_id = "BadMessageId"
    bad_priority = "BadPriority"
    bad_topic = "BadTopic"
    device_token_not_for_topic = "DeviceTokenNotForTopic"
    duplicate_headers = "DuplicateHeaders"
    idle_timeout = "IdleTimeout"
    invalid_push_type = "InvalidPushType"
    missing_device_token = "MissingDeviceToken"
    missing_topic = "MissingTopic"
    payload_empty = "PayloadEmpty"
    topic_disallowed = "TopicDisallowed"
    bad_certificate = "BadCertificate"
    bad_certificate_environment = "BadCertificateEnvironment"
    expired_provider_token = "ExpiredProviderToken"
    forbidden = "Forbidden"
    invalid_provider_token = "InvalidProviderToken"
    missing_provider_token = "MissingProviderToken"
    bad_path = "BadPath"
    method_not_allowed = "MethodNotAllowed"
    unregistered = "Unregistered"
    payload_too_large = "PayloadTooLarge"
    too_many_provider_token_updates = "TooManyProviderTokenUpdates"
    too_many_requests = "TooManyRequests"
    internal_server_error = "InternalServerError"
    service_unavailable = "ServiceUnavailable"
    shutdown = "Shutdown"
