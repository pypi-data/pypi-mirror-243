import random
import time
from abc import ABC
from typing import Optional
from lgt.common.python.discord_client.discord_client import DiscordClient
from lgt.common.python.helpers import get_formatted_bot_name
from lgt.common.python.slack_client.web_client import SlackWebClient
from lgt_data.enums import SourceType
from lgt_data.model import DedicatedBotModel, Server, Channel
from lgt_data.mongo_repository import DedicatedBotRepository
from pydantic import BaseModel
from lgt_data.analytics import get_bots_aggregated_analytics
from lgt.common.python.lgt_logging import log
from lgt.common.python.enums.slack_errors import SlackErrors
from ..basejobs import BaseBackgroundJob, BaseBackgroundJobData

"""
Update bots statistics
"""


class BotStatsUpdateJobData(BaseBackgroundJobData, BaseModel):
    bot_id: Optional[str]


class BotStatsUpdateJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return BotStatsUpdateJobData

    def exec(self, data: BotStatsUpdateJobData):
        bots_rep = DedicatedBotRepository()
        bot = bots_rep.get_one(id=data.bot_id)

        if bot.source.source_type == SourceType.DISCORD:
            client = DiscordClient(bot.token)
            servers_response = client.get_servers()

            if isinstance(servers_response, dict):
                if servers_response.get('message') == '401: Unauthorized':
                    BotStatsUpdateJob.__updated_invalid_creds_flag(bot, True)
                log.warning(f"[BotStatsUpdateJob]: Servers response is not list: {servers_response}")
                return

            bot.servers = [Server.from_dic(server) for server in servers_response]
            updated_active_servers = []
            for server in bot.servers:
                time.sleep(random.randint(1, 2))
                channels = [Channel.from_dic(channel) for channel in client.get_channels(server.id)]
                server.channels = channels
                server.icon = f'https://cdn.discordapp.com/icons/{server.id}/{server.icon}.png'
                for active_server in bot.active_servers:
                    if active_server.id == server.id:
                        updated_active_servers.append(server)
                        break

            bot.active_servers = updated_active_servers
            bots_rep.add_or_update(bot)
            return

        client = SlackWebClient(bot.token, bot.cookies)
        test_auth_response = client.test_auth()
        if not test_auth_response.status_code == 200:
            log.warning(f"[BotStatsUpdateJob]: Error to auth {data.bot_id}. {test_auth_response.content}")
            return

        if not bot.invalid_creds:
            error = test_auth_response.json().get("error")
            if error == SlackErrors.INVALID_AUTH or error == SlackErrors.TWO_FACTOR_REQUIRED:
                BotStatsUpdateJob.__updated_invalid_creds_flag(bot, True)

        user = test_auth_response.json().get('user_id')
        bot.associated_user = user
        bots_rep.add_or_update(bot)
        team_info = {}
        try:
            team_info = client.get_team_info()
        except:
            log.warning(f"[BotStatsUpdateJob]: Error to get  team info of {data.bot_id}. {test_auth_response.content}")

        if team_info.get('ok'):
            bot_name = get_formatted_bot_name(team_info['team']['domain'])
            if bot.servers and bot.active_servers:
                bot.servers[0].name = bot.active_servers[0].name = bot_name
            bot.source.source_name = bot_name
            bot.slack_url = bot.registration_link = team_info['team']['url']
            bots_rep.add_or_update(bot)
        received_messages, filtered_messages = get_bots_aggregated_analytics(bot_ids=[bot.id])
        try:
            channels_response = client.channels_list()
        except:
            log.warning(f"[BotStatsUpdateJob]: Error to get channels list for bot {bot.id}.")
            return

        if not channels_response['ok']:
            if channels_response.get("error") == SlackErrors.INVALID_AUTH:
                BotStatsUpdateJob.__updated_invalid_creds_flag(bot, True)
            else:
                log.warning(f"[BotStatsUpdateJob]: Error during update bot {bot.id} stats. Error: {channels_response}")
            return
        channels = channels_response['channels']
        connected_channels = 0
        channels_users = {}
        active_channels = {}
        users_count = 0
        for channel in channels:
            if channel['is_member']:
                active_channels[channel['id']] = channel['name']
                connected_channels += 1
            num_members = channel.get('num_members', 0)
            channels_users[channel['id']] = num_members
            users_count += num_members

        bot.active_channels = active_channels
        bot.messages_received = received_messages.get(bot.source.source_name, 0)
        bot.messages_filtered = filtered_messages.get(bot.source.source_name, 0)
        bot.connected_channels = connected_channels
        bot.channels = len(channels)
        bot.channels_users = channels_users
        bot.users_count = users_count
        if bot.recent_messages is None:
            bot.recent_messages = []
        if bot.active_servers and bot.servers:
            channels = [Channel.from_dic(channel_dict) for channel_dict in channels]
            bot.active_servers[0].channels = bot.servers[0].channels = channels
        # save only last 50 messages
        bot.recent_messages = bot.recent_messages[-50:]
        bots_rep.add_or_update(bot)

    @staticmethod
    def __updated_invalid_creds_flag(bot: DedicatedBotModel, invalid_creds: bool):
        if bot.invalid_creds != invalid_creds:
            bot.invalid_creds = invalid_creds
            DedicatedBotRepository().add_or_update(bot)