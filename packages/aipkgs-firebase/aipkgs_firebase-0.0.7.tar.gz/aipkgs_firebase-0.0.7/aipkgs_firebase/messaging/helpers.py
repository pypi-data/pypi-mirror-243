import datetime
from firebase_admin import messaging
import aipkgs_firebase.messaging.core as cmcore
from aipkgs_firebase.messaging.enums import AndroidPriorityEnum


def send_to_token(token: str, data: dict):
    message = cmcore.create_message(token=token, data=data)
    cmcore.send_message(message=message)


def send_to_topic(topic: str, data: dict):
    message = cmcore.create_message(topic=topic, data=data)
    cmcore.send_message(message)


def send_to_condition(condition: str, notification: messaging.Notification):
    message = cmcore.create_message(notification=notification, condition=condition)
    cmcore.send_message(message=message)


def send_dry_run(token: str, data: dict):
    message = cmcore.create_message(token=token, data=data)
    cmcore.send_message(message, dry_run=True)


def send_multicast(data: dict, tokens: list):
    message = cmcore.create_multicast_message(data=data, tokens=tokens)
    response = messaging.send_multicast(message)


def send_multicast_and_handle_errors(data: dict, tokens: list):
    message = cmcore.create_multicast_message(data=data, tokens=tokens)
    response = messaging.send_multicast(message)
    if response.failure_count > 0:
        responses = response.responses
        failed_tokens = []
        for idx, resp in enumerate(responses):
            if not resp.success:
                # The order of responses corresponds to the order of the registration tokens.
                failed_tokens.append(tokens[idx])
        print('List of tokens that caused failures: {0}'.format(failed_tokens))


def create_unity_message(title: str = None, body: str = None, badge: int = None, icon: str = None, web_icon: str = None, ios_priority: int = None, android_priority: AndroidPriorityEnum = None, color: str = None, ttl_seconds: int = None, token: str = None, topic: str = None):

    notification = cmcore.create_notification(title=title, body=body)

    android_config = cmcore.create_android_configuration(title=title, body=body, icon=icon, color=color, ttl_seconds=ttl_seconds, priority=android_priority)

    ios_apns_config = cmcore.create_ios_apns_config(title=title, body=body, priority=ios_priority, badge=badge)

    web_push_config = cmcore.create_web_push_config(title=title, body=body, icon=web_icon)

    message = cmcore.create_message(token=token, notification=notification, android_config=android_config, apns_config=ios_apns_config, web_push=web_push_config, topic=topic)

    return message

