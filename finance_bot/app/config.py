"""
Модуль конфигурации для Finance Tracker Bot.

Использует pydantic_settings для валидации и загрузки настроек из переменных окружения.
Все настройки загружаются из .env файла при старте приложения.

Attributes:
    settings (Settings): Глобальный экземпляр настроек приложения
"""


from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Конфигурация приложения с валидацией типов.

    Attributes:
        DATABASE_URL (str): URL подключения к PostgreSQL базе данных
        BOT_TOKEN (str): Токен Telegram бота от BotFather
        API_ID (int): ID приложения из my.telegram.org
        API_HASH (str): Hash приложения из my.telegram.org
        API_V1_STR (str): Префикс для API эндпоинтов
        PROJECT_NAME (str): Название проекта

    Example:
        DATABASE_URL=postgresql://user:password@localhost/dbname
        BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
        API_ID=12345
        API_HASH=0123456789abcdef0123456789abcdef
    """

    DATABASE_URL: str
    BOT_TOKEN: str 
    API_ID: int
    API_HASH: str
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Finance Tracker"

    class Config:
        """
        Конфигурация для pydantic модели Settings.

        Attributes:
            case_sensitive (bool): Учитывать регистр при сопоставлении переменных окружения
        """
        case_sensitive = True

# Глобальный экземпляр настроек
settings = Settings()
