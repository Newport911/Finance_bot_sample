pytest_plugins = ('pytest_asyncio',)

import pytest
from unittest.mock import MagicMock, AsyncMock
from pyrogram import Client, types

@pytest.fixture
def mock_client():
    return MagicMock(spec=Client)

@pytest.fixture
def mock_message():
    message = MagicMock(spec=types.Message)
    message.reply_text = AsyncMock()
    return message