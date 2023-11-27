import datetime

from firebase_admin import messaging

# region create message
from aipkgs_firebase.messaging.enums import AndroidPriorityEnum


def create_message(token: str = None, notification: messaging.Notification = None,
                   android_config: messaging.AndroidConfig = None, apns_config: messaging.APNSConfig = None,
                   web_push: messaging.WebpushConfig = None, topic: str = None, data: dict = None,
                   condition: str = None):
    message = messaging.Message()
    if token:
        message.token = token
    if notification:
        message.notification = notification
    if android_config:
        message.android = android_config
    if apns_config:
        message.apns = apns_config
    if web_push:
        message.webpush = web_push
    if topic:
        message.topic = topic
    if data:
        message.data = data
    if condition:
        message.condition = condition
    return message


def create_multicast_message(tokens: list = None, notification: messaging.Notification = None,
                             android_config: messaging.AndroidConfig = None, apns_config: messaging.APNSConfig = None,
                             web_push: messaging.WebpushConfig = None, topic: str = None, data: dict = None):
    message = messaging.MulticastMessage()
    if tokens:
        message.tokens = tokens
    if notification:
        message.notification = notification
    if android_config:
        message.android = android_config
    if apns_config:
        message.apns = apns_config
    if web_push:
        message.webpush = web_push
    if topic:
        message.topic = topic
    if data:
        message.data = data
    return message


# endregion


# region notification
def create_notification(title: str = None, body: str = None):
    notification = messaging.Notification()
    if title:
        notification.title = title
    if body:
        notification.body = body
    return notification


# endregion


# region ios
def create_ios_apns_config(title: str = None, body: str = None, priority: int = None, badge: int = None):
    # aps alert
    aps_alert = messaging.ApsAlert(
        title=title,
        body=body,
    )
    if title:
        aps_alert.title = title
    if body:
        aps_alert.body = body

    # aps
    aps = messaging.Aps()
    if aps_alert:
        aps.alert = aps_alert
    if badge:
        aps.badge = badge

    # apns payload
    payload = messaging.APNSPayload()
    if aps:
        payload.aps = aps

    # apns config
    apns_config = messaging.APNSConfig()
    if payload:
        apns_config.payload = payload

    headers: dict = {}
    if priority:
        headers['apns-priority'] = f'{priority}'
    apns_config.headers = headers

    return apns_config


# endregion


# region android
def create_android_configuration(title: str = None, body: str = None, icon: str = None, color: str = None,
                                 ttl_seconds: int = None, priority: AndroidPriorityEnum = None):
    notification = messaging.AndroidNotification()
    if title:
        notification.title = title
    if body:
        notification.body = body
    if icon:
        notification.icon = icon
    if color:
        notification.color = color

    android_config = messaging.AndroidConfig()
    notification.ttl = datetime.timedelta(seconds=ttl_seconds or 3600),
    notification.priority = priority.value if priority else AndroidPriorityEnum.normal.value
    if notification:
        android_config.notification = notification

    return android_config


# endregion


# region web notification
def create_web_push_config(title: str = None, body: str = None, icon: str = None):
    notification = messaging.WebpushNotification()
    if title:
        notification.title = title
    if body:
        notification.body = body
    if icon:
        notification.icon = icon

    config = messaging.WebpushConfig()
    if notification:
        config.notification = notification

    return config


# eng region


# region send messages
def send_all_message(messages: [messaging.Message], dry_run: bool = None):
    response = messaging.send_all(messages=messages, dry_run=dry_run or False)
    print('{0} messages were sent successfully'.format(response.success_count))


def send_message(message: messaging.Message, dry_run: bool = None):
    response = messaging.send(message=message, dry_run=dry_run or False)
    print('Successfully sent message:', response)


def send_multicast_message(message: messaging.MulticastMessage, dry_run: bool = None):
    response = messaging.send_multicast(multicast_message=message, dry_run=dry_run or False)
    print('{0} messages were sent successfully'.format(response.success_count))


# endregion


# region topic
def subscribe_to_topic(topic: str, tokens: list):
    response = messaging.subscribe_to_topic(tokens, topic)
    print(response.success_count, 'tokens were subscribed successfully')


def unsubscribe_from_topic(topic: str, tokens: list):
    response = messaging.unsubscribe_from_topic(tokens, topic)
    print(response.success_count, 'tokens were unsubscribed successfully')
# endregion
