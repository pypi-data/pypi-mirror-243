
import json
from datetime import datetime, timedelta
import requests


class MarketingCloudAPI:
    """MarketingCloud API to send SMS messages."""

    def __init__(
        self, subdomain: str,
        client_id: str, client_secret: str, sms_msg_id: str,
        call_key: str, client_number: str
    ):
        """
        Args:
            subdomain (str): Salesforce marketing cloud subdomain.
            client_id (str): client_id Identification at Salesforce marketing
                cloud.
            client_secret (str): Salesforce marketing cloud client secret.
            sms_msg_id (str): ?.
        Return:
            MarketingCloudAPI object.
        """

        self._subdomain = subdomain
        self._client_id = client_id
        self._client_secret = client_secret
        self._sms_msg_id = sms_msg_id
        self._call_key = call_key
        self._client_number = client_number
        self._access_token = None
        self._auth_response = None

    def generate_token(self):
        """
        Generate a new token of Salesforce.

        Args:
            No Args.
        Kwargs:
            No Kwargs.
        Return:
            None
        """
        url = (
            'https://{subdomain}.auth.marketingcloudapis.com/v2/'
            'token').format(subdomain=self._subdomain)
        try:
            response = requests.post(
                url=url, json={
                    "grant_type": "client_credentials",
                    "client_id": self._client_id,
                    "client_secret": self._client_secret})
            response.raise_for_status()
            response_json = response.json()
            self.last_token_refresh = datetime.now()
            self.token_expires_at = (
                self.last_token_refresh + timedelta(
                    seconds=response_json["expires_in"]))
            self._access_token = response_json['access_token']
            print("Token generated successfully!")
        except Exception as e:
            raise e

    def get_auth_header(self):
        """
        Refresh token if not valid.

        Args:
            No args.
        Kwargs:
            No Kwargs
        """
        # If token not set create one
        if self._access_token is None:
            self.generate_token()
        elif self.token_expires_at < datetime.now():
            self.generate_token()

        request_header = {
            "Content-Type": "application/json",
            "Authorization": 'Bearer {access_token}'.format(
                access_token=self._access_token)}
        return request_header

    def get_message_status(self, token_id: str):
        """
        Get delivery status of the message.

        Args:
            external_id [str]: Message external id.
        Kwargs:
            No Kwargs.
        Return:
            None
        """
        service_url = (
            "https://{subdomain}.rest.marketingcloudapis.com/"
            "sms/v1/messageContact/{call_key}/"
            "deliveries/{token_id}"
        ).format(
            subdomain=self._subdomain,
            call_key=self._call_key,
            token_id=token_id
        )

        auth_header = self.get_auth_header()
        response = requests.get(
            service_url,
            headers=auth_header
        )
        response.raise_for_status()

        return response.json()

    def send_message(self, rapidpro_request: dict, auth_header: dict):

        base_url = 'https://{subdomain}.rest.marketingcloudapis.com'.format(
            subdomain=self._subdomain
        )
        url = f'{base_url}/sms/v1/messageContact/{self._call_key}/send'

        message = f"{rapidpro_request['text']} %%[SetSmsConversationNextKeyword({self._client_number}, AttributeValue(\"MOBILE_NUMBER\"), \"MOVVA_NUDGE_RESPOSTA\")]%%"  # noqa

        send_sms_payload = {
            "url": url,
            "headers": auth_header,
            "data": json.dumps({
                "mobileNumbers": [
                    rapidpro_request['to_no_plus']
                ],
                "Override": True,
                "messageText": message
            })
        }

        print(f"Payload========================{send_sms_payload['data']}")

        response = requests.post(
            timeout=60,
            **send_sms_payload
        )

        return response

    def check_error_keys_mc_response(self, mc_response: json):
        if 'errorCode' or 'errorMessage' in mc_response:
            return True
        return False

    def update_status_failed_message_in_rapidpro(
        self, rapidpro_request: json
    ):

        url = 'https://rapidpro.nudgebots.com/c/ex/{channel}/failed?id={message_id}'.format(
            channel=rapidpro_request['channel'],
            message_id=self._sms_msg_id
        )

        response = requests.post(url)

        print("Message status updated: Failed")

        return response

        return None

    def update_status_sent_message_in_rapidpro(
        self, rapidpro_request: json
    ):
        url = 'https://rapidpro.nudgebots.com/c/ex/{channel}/sent?id={message_id}'.format(
            channel=rapidpro_request['channel'],
            message_id=self._sms_msg_id
        )

        response = requests.post(url)

        print("Message status updated: Sent")

        return response

    def update_status_delivered_message_in_rapidpro(
        self, rapidpro_request: json
    ):
        url = 'https://rapidpro.nudgebots.com/c/ex/{channel}/delivered?id={message_id}'.format(
            channel=rapidpro_request['channel'],
            message_id=self._sms_msg_id
        )

        response = requests.post(url)

        print("Message status updated: Delivered")

        return response
