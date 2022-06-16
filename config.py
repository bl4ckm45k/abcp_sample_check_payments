from dataclasses import dataclass
from typing import List

from environs import Env


@dataclass
class DbConfig:
    host: str
    port: str
    password: str
    user: str


@dataclass
class TgBot:
    token: str
    admin_ids: List[int]
    use_redis: bool


@dataclass
class TgChats:
    payments_chat: str


@dataclass
class Abcp:
    host: str
    login: str
    password: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    abcp: Abcp
    tg_chats: TgChats


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS")
        ),
        db=DbConfig(
            host=env.str('DB_HOST'), port=env.str('DB_PORT'),
            user=env.str('DB_USER'), password=env.str('DB_PASS')
        ),
        abcp=Abcp(
            host=env.str('ABCP_HOST'),
            login=env.str('ABCP_LOGIN'), password=env.str('ABCP_PASSWORD')
        ),
        tg_chats=TgChats(payments_chat=env.str('PAYMENTS_CHAT_ID'))

        )
