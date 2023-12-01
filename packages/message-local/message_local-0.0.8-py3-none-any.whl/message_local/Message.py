"imports"
from abc import ABC, abstractmethod
from enum import Enum

from circles_local_database_python.generic_crud import GenericCRUD
from item_local.item import Item

AWS_SMS_MESSAGE_PROVIDER_ID = 1
SMS_MESSAGE_CHANNEL_ID = 2
WHATSAPP_CHANNEL_ID = 11
INFORU_MESSAGE_PROVIDER_ID = 2


class Importance(Enum):
    "Enum class"
    LOW = 10
    MEDIUM = 20
    HIGH = 30

# TODO Please add MessagesLocal Class in a separate file
# TODO Please add get_channel() and get_profider() methods so make decision which channel
# (Email, WhatsApp, SMS- Default at this point in time ...) and to decide which provider
# (AWS SNS, InforU- Default at this point in thime, ...) to use in each case.
# TODO Please integrate those methods in Message Class


class Message(Item, ABC):
    "Message Class"
    def __init__(self, body: str, importance: Importance, subject: str = None) -> None:
        # TODO We should add all fields from message schema in the database
        # (i.e. message_id, scheduled_sent_timestamp, message_sent_status : MessageSentStatus  ...)
        self.body = body
        self.importance = importance
        self.subject = subject

    # TODO Create a new Class of Recipient
    @abstractmethod
    def send(self, recipients: list, cc: list = None, bcc: list = None) -> None:
        "send method"
        message_channel = self._get_message_channel_id
        provider_id = self._get_message_provider_id(message_channel)
        # TODO Call API-Management Direct (see API Management tests direct.py)
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def was_read(self) -> bool:
        "read method"
        raise NotImplementedError("Subclasses must implement this method.")

    def get_importance(self) -> Importance:
        "get method"
        return self.importance

    @abstractmethod
    def _can_send(self) -> bool:
        # TODO call API Management Indirect before (see API Management tests indirect.py)
        """Implement this with API management """
        """https://github.com/circles-zone/api-management-local-python-package"""
        raise NotImplementedError(
            "Implement this with API management"
            "https://github.com/circles-zone/api-management-local-python-package")

    @abstractmethod
    def _after_send_attempt(self) -> None:
        # TODO Call API Management Indiret after (see API Management tests indirect.py)
        """Update the DB if sent successfully, or with the problem details"""
        raise NotImplementedError(
            "Update the DB if sent successfully, or with the problem details")

    def _get_message_channel_id(self) -> int:
        return SMS_MESSAGE_CHANNEL_ID

    def _get_message_provider_id(self, message_channel_id: int) -> int:
        "return message provider"
        if message_channel_id == SMS_MESSAGE_CHANNEL_ID:
            return SMS_MESSAGE_CHANNEL_ID
        elif message_channel_id == AWS_SMS_MESSAGE_PROVIDER_ID:
            return AWS_SMS_MESSAGE_PROVIDER_ID
        elif message_channel_id == WHATSAPP_CHANNEL_ID:
            return INFORU_MESSAGE_PROVIDER_ID
