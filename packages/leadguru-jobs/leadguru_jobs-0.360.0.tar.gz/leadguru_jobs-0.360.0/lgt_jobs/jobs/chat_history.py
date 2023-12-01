import datetime
from abc import ABC
from typing import Optional, List
from lgt.common.python.lgt_logging import log
from lgt.common.python.slack_client.web_client import SlackWebClient, SlackMessageConvertService
from lgt_data.model import SlackHistoryMessageModel, UserModel, UserContact
from lgt_data.mongo_repository import UserMongoRepository, DedicatedBotRepository, UserContactsRepository
from pydantic import BaseModel
from ..runner import BackgroundJobRunner
from ..env import portal_url
from ..basejobs import BaseBackgroundJob, BaseBackgroundJobData
from ..smtp import SendMailJobData, SendMailJob

"""
Load slack chat history
"""


class LoadChatHistoryJobData(BaseBackgroundJobData, BaseModel):
    user_id: str
    template_path: str = 'lgt_jobs/templates/new_message_mail_template.html'


class LoadChatHistoryJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return LoadChatHistoryJobData

    def exec(self, data: LoadChatHistoryJobData):
        """download chat history"""
        user = UserMongoRepository().get(data.user_id)
        contacts = UserContactsRepository().find(user.id, with_chat_only=True, spam=False)
        if not contacts:
            return

        log.info(f"[LoadChatHistoryJob]: processing {len(contacts)} contacts for user: {user.email}")
        last_message = None
        last_message_contact = None
        for contact in contacts:
            message = LoadChatHistoryJob._update_history(user=user, contact=contact)

            if not message:
                continue

            if not last_message:
                last_message = message
                last_message_contact = contact

            if message.created_at > last_message.created_at and message.user == contact.sender_id:
                last_message = message
                last_message_contact = contact

        has_to_be_notified = (not user.new_message_notified_at or
                              (last_message and last_message.created_at > user.new_message_notified_at))

        if last_message and has_to_be_notified and last_message.user == last_message_contact.sender_id:
            LoadChatHistoryJob._notify_about_new_messages(user, last_message_contact, data.template_path)
            UserMongoRepository().set(data.user_id, new_message_notified_at=datetime.datetime.utcnow())

    @staticmethod
    def _merge_chat_histories(contact: UserContact, messages: List[SlackHistoryMessageModel]):
        for message in contact.chat_history:
            if not [True for msg in messages if msg.ts == message.ts]:  # Uniq messages
                messages.append(message)
        messages.reverse()
        return messages

    @staticmethod
    def _update_history(user: UserModel, contact: UserContact) -> Optional[SlackHistoryMessageModel]:
        bot = DedicatedBotRepository().get_one(user_id=user.id, source_id=contact.source_id, only_valid=True)
        if not bot:
            return None

        slack_client = SlackWebClient(bot.token, bot.cookies)
        try:
            history = slack_client.chat_history(contact.chat_id)
        except Exception as ex:
            log.error(f'[LoadChatHistoryJob]: Failed to load chat for the contact: {contact.id}. ERROR: {str(ex)}')
            return

        if not history['ok']:
            log.error(f'Failed to load chat for the contact: {contact.id}. ERROR: {history.get("error", "")}')
            return

        messages = [SlackMessageConvertService.from_slack_response(user.email, "slack_files", bot.token, m) for m in
                    history.get('messages', [])]
        messages = LoadChatHistoryJob._merge_chat_histories(contact, messages)
        chat_history = [message.to_dic() for message in messages]
        if not chat_history:
            return None

        UserContactsRepository().update(user.id, contact.sender_id, chat_history=chat_history)
        return messages[-1] if bot.associated_user != contact.sender_id else None

    @staticmethod
    def _notify_about_new_messages(user: UserModel, contact: UserContact, template_path: str):
        with open(template_path, mode='r') as template_file:
            html = template_file.read()
            html = html.replace("{sender}", contact.name if hasattr(contact, 'name') else contact.real_name)
            html = html.replace("{view_message_link}", f'{portal_url}/')

            message_data = {
                "html": html,
                "subject": 'New message(s) on LEADGURU',
                "recipient": user.email,
                "sender": None
            }

        BackgroundJobRunner.submit(SendMailJob, SendMailJobData(**message_data))
