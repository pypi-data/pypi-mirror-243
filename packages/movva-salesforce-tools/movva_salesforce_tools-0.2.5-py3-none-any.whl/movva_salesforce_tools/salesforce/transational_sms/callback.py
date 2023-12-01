import requests
from google.cloud import firestore


def get_rapidpro_id_by_marketingcloud_key(marketingcloud_key):
    db = firestore.Client()
    # [START firestore_get_rapidpro_id_by_marketingcloud_key]
    doc_ref = db.collection(u'rapidpro_marketingcloud').document(marketingcloud_key)

    doc = doc_ref.get()
    data = None
    if doc.exists:
        data = doc.to_dict()
        print(f'Document data: {data}')
    else:
        print(u'No such document!')
    # [END firestore_get_rapidpro_id_by_marketingcloud_key]

    return data['rapidpro_id'] if data is not None else None


def get_url(event_category_type, info):
    base_url = 'https://rapidpro.nudgebots.com/c/ex/38371db4-0c31-4ee6-a461-63ba87587081'
    category_type_to_url = {
        'TransactionalSendEvents.SmsSent': 'sent',
        'TransactionalSendEvents.SmsNotSent': 'failed',
        'TransactionalSendEvents.SmsBounced': 'failed',
        'TransactionalSendEvents.SmsDelivered': 'delivered',
    }

    if event_category_type in category_type_to_url:
        return f'{base_url}/{category_type_to_url[event_category_type]}'

    if event_category_type == 'TransactionalSendEvents.SmsTransient':
        if info['statusCode'] in ('3000', '3001', '3002', ):
            # 3000: Enroute | Message is en route to carrier. Waiting on carrier confirmation.
            # 3001: SentToCarrier | Message sent to carrier. Waiting to be accepted by carrier.
            # 3002: AcceptedByCarrier | Message accepted by carrier. Waiting for delivery confirmation.
            return f'{base_url}/sent'

        elif info['statusCode'] in ('4000', ):
            # 4000: Delivered | Message delivered to mobile device.
            return f'{base_url}/delivered'

        else:
            # 1000: QueuedToSfmcSendService | Message queued to the internal send service.
            # 1500: QueueFailureToSfmcSendService | Message failed to queue to the internal send service. Retry your send.
            # 1501: ValidationError | Status indicates an internal validation error. Retry your send.
            # 2000: DeliveredToAggregator | Message delivered to aggregator. Status is updated when delivery confirmation comes from carrier or mobile device. For shared codes, this status is the final one.
            # 2500: FailedToAggregator | Message not delivered to aggregator. Retry your send.
            # 2501: UnknownToAggregator | Unknown aggregator error.
            # 2502: FailedToAggregatorDueToInvalidDestinationAddress | Invalid Destination Address.
            # 2600: ThrottledToAggregator | Message not accepted by aggregator due to capacity issues. Salesforce exhausted the retry process.
            # 2601: SocketExceptionToAggregator | Socket connection error to aggregator. Can retry. If this status is logged, we exhausted our retries.
            # 3400: Unknown | Unknown error.
            # 4500: Undeliverable | Message not delivered to mobile device.
            # 4501: Expired | Message expired. Message exhausted the carrier retry process. Mobile device is out of carrier range.
            # 4502: Deleted | Message deleted by the carrier.
            # 4503: Rejected | Message rejected. Carrier detected a loop or assumed that message is spam. This status can indicate an administrative or financial problem between the operator and the end users.
            # 4504: FailedDueToUnknownSubscriber | Unknown Subscriber.
            # 4505: FailedDueToInvalidDestinationAddress | Invalid Destination Address.

            return f'{base_url}/failed'

    return None


def process_status_update(status_update):
    event_category_type = status_update['eventCategoryType']
    info = status_update['info']
    message_key = info['messageKey']
    # TransactionalSendEvents.SmsSent
    # TransactionalSendEvents.SmsDelivered

    # 1. Get rapidpro_id by MC message key
    rapidpro_id = get_rapidpro_id_by_marketingcloud_key(message_key)
    if rapidpro_id is None:
        print(
            f'Failed to find rapidpro_id for message_key = {message_key}, info = {info}')

        return

    # 2. Get mapped status from MC to RapidPro
    url = get_url(event_category_type, info)
    if url is None:
        print(
            f'Failed to find url for event_category_type = {event_category_type}, info = {info}')

        return

    # 3. Send status update to RapidPro
    send_status_payload = {
        "url": url,
        "data": {
            "id": rapidpro_id
        }
    }

    return requests.post(
        timeout=60,
        **send_status_payload)


def main(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)

    if 'verificationKey' in request_json:
        print(request_json)
        return request_json, 200

    responses = []

    for status_update in request_json:
        request_to_rapidpro = process_status_update(status_update)
        if request_to_rapidpro is None:
            continue

        responses.append(request_to_rapidpro)

    return {
        "responses": [response.json() for response in responses],
        "status_code": [response.status_code for response in responses],
        "error_count": sum([1 for response in responses
                            if response.status_code != 200]),
    }
