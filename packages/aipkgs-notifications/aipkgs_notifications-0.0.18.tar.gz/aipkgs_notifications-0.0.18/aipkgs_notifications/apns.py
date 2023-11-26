import json
import time
import uuid
import httpx
import jwt
import aipkgs_notifications.singleton as singleton
import aipkgs_notifications.utils as utils
import aipkgs_notifications.response as ai_response
import aipkgs_notifications.payload as ai_payload
import aipkgs_notifications.enums as enums


APNS_HOST_URL_SANDBOX = "https://api.sandbox.push.apple.com"
APNS_HOST_URL_PROD = "https://api.push.apple.com"


class Config:
    def __init__(self, verbose: bool = None):
        self.verbose = verbose or False


@singleton.Singleton
class APNS:
    def __init__(self, key_id: str = '', team_id: str = '', bundle_id: str = '', is_prod: bool = None, p8_key_path: str = '', pem_file_path: str = '', apns_priority: int = None,
                 apns_expiration: int = None):
        self.config = Config()

        self.ALGORITHM = 'ES256'
        self.KEY_ID = key_id
        self.TEAM_ID = team_id
        self.BUNDLE_ID = bundle_id
        self.IS_PROD = is_prod
        self.AUTH_P8_KEY = p8_key_path
        self.AUTH_PEM_KEY = pem_file_path
        self.AUTH_TOKEN = None
        self.APNS_PRIORITY = str(apns_priority) or '10'
        self.APNS_EXPIRATION = str(apns_expiration) or '0'

        if self.IS_PROD:
            self.APNS_HOST_URL = APNS_HOST_URL_PROD
        else:
            self.APNS_HOST_URL = APNS_HOST_URL_SANDBOX

        # assert self.KEY_ID, "KEY_ID is null or empty"
        # assert self.TEAM_ID, "TEAM_ID is null or empty"
        # assert self.BUNDLE_ID, "BUNDLE_ID is null or empty"
        # assert self.AUTH_P8_KEY or self.AUTH_PEM_KEY, "AUTH_P8_KEY or AUTH_PEM_KEY is null or empty"

    @property
    def authentication_method(self) -> enums.AuthenticationMethod:
        if self.AUTH_P8_KEY:
            return enums.AuthenticationMethod.P8
        elif self.AUTH_PEM_KEY:
            return enums.AuthenticationMethod.PEM
        else:
            return None

    def __initialize_apns(self, key_id='', team_id='', bundle_id='', is_prod: bool = None, p8_key_path='', pem_file_path='', apns_priority: int = None,
                          apns_expiration: int = None):
        self.__init__(key_id=key_id, p8_key_path=p8_key_path, pem_file_path=pem_file_path, team_id=team_id, bundle_id=bundle_id, is_prod=is_prod, apns_priority=apns_priority,
                      apns_expiration=apns_expiration)

    def initialize_apns(self, key_id='', team_id='', bundle_id='', is_prod: bool = None, p8_key_path='', pem_file_path='', apns_priority: int = None, apns_expiration: int = None):
        self.__initialize_apns(key_id=key_id, team_id=team_id, bundle_id=bundle_id, is_prod=is_prod, p8_key_path=p8_key_path, pem_file_path=pem_file_path,
                               apns_priority=apns_priority,
                               apns_expiration=apns_expiration)

    def __generate_auth_token(self, expires: int = None) -> str:
        if self.AUTH_TOKEN:
            if expires:
                token_expired = True
                now = time.time()
                decoded_token = jwt.decode(self.AUTH_TOKEN, verify=False)
                if (decoded_token['exp'] - now) > 60:  # check if 60 seconds is left, consider it expired
                    token_expired = True
                elif decoded_token['exp'] > time.time():
                    token_expired = False
                if decoded_token['exp'] < time.time():
                    token_expired = True

                if token_expired is False:
                    return self.AUTH_TOKEN

        with open(self.AUTH_P8_KEY, 'r') as file:
            private_key = file.read()

        headers = {
            'kid': self.KEY_ID,
        }

        now = time.time()
        token_payload = {
            'iss': self.TEAM_ID,
            'iat': int(time.time()),
        }
        if expires:
            expires = now + (60 * expires)  # minutes
            token_payload['exp'] = int(expires)

        token = jwt.encode(
            token_payload,
            private_key,
            algorithm=self.ALGORITHM,
            headers=headers
        )

        self.AUTH_TOKEN = token

        return token

    def push(self, device_token: str, payload: ai_payload.Payload, push_type: enums.PushType = None, collapse_id: str = None) -> ai_response.APNSResponse:
        if self.authentication_method is None:
            raise Exception("Authentication method is not defined")

        FULL_URL = f"{self.APNS_HOST_URL}/3/device/{device_token}"

        auth_token = None
        if self.authentication_method == enums.AuthenticationMethod.P8:
            auth_token = self.__generate_auth_token(expires=None)

        bundle_id = self.BUNDLE_ID
        if push_type == enums.PushType.push_to_talk:
            bundle_id = f"{bundle_id}.voip-ptt"

        # headers
        headers = {
            "apns-id": str(uuid.uuid4()),
            "apns-push-type": push_type.value if push_type else enums.PushType.alert.value,
            "apns-expiration": self.APNS_EXPIRATION,
            "apns-priority": self.APNS_PRIORITY,
            "apns-topic": bundle_id,
            "apns-collapse-id": collapse_id,
            "apns-unix-time": str(int(time.time())),
        }
        if auth_token:
            headers["authorization"] = f"bearer {auth_token}"

        headers = utils.remove_nulls(headers)

        # print
        if self.config.verbose:
            print('---------------- sending push notification ----------------')
            print(f"headers: {json.dumps(headers, indent=4)}")
            print(f"data: {json.dumps(payload.to_dict(), indent=4)}")

        # send request
        response = None
        if self.authentication_method == enums.AuthenticationMethod.P8:
            client = httpx.Client(http2=True)
            response = client.post(
                FULL_URL,
                headers=headers,
                json=payload.to_dict(),
            )
        elif self.authentication_method == enums.AuthenticationMethod.PEM:
            client = httpx.Client(http2=True, cert=self.AUTH_PEM_KEY)
            response = client.post(
                FULL_URL,
                headers=headers,
                json=payload.to_dict(),
            )

        apns_response = ai_response.APNSResponse(httpx_response=response)

        if self.config.verbose:
            print(f"is_sent: {apns_response.is_sent()}")
            print(f"status_code: {apns_response.status_code}")
            print(f"apns_id: {apns_response.apns_id}")
            print(f"apns_unique_id:  {apns_response.apns_unique_id}")
            print(f"timestamp: {apns_response.timestamp.time if apns_response.timestamp else None}")

        return apns_response


def config() -> Config:
    return APNS.shared.config


def initialize_apns(key_id='', team_id='', bundle_id='', is_prod: bool = None, p8_key_path='', pem_file_path='', apns_priority: int = None, apns_expiration: int = None):
    APNS.shared.initialize_apns(key_id=key_id, team_id=team_id, bundle_id=bundle_id, is_prod=is_prod, p8_key_path=p8_key_path, pem_file_path=pem_file_path,
                                apns_priority=apns_priority, apns_expiration=apns_expiration)
    return APNS.shared


def push_raw(device_token: str, payload: ai_payload.Payload, push_type: enums.PushType = None, collapse_id: str = None) -> ai_response.APNSResponse:
    return APNS.shared.push(device_token=device_token, payload=payload, push_type=push_type, collapse_id=collapse_id)


def push(device_token: str, title: str, body: str = None, data: dict = None, badge: int = None, push_type: enums.PushType = None, collapse_id: str = None) -> ai_response.APNSResponse:
    alert_payload = ai_payload.AlertPayload(title=title, body=body)
    payload = ai_payload.Payload(alert=alert_payload, badge=badge, data=data)

    return push_raw(device_token=device_token, payload=payload, collapse_id=collapse_id)
