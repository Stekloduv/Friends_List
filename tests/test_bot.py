import pytest
from unittest.mock import AsyncMock, patch
from app import bot



@pytest.mark.asyncio
async def test_start_command():
    update = AsyncMock()
    context = AsyncMock()

    await bot.start(update, context)

    update.message.reply_text.assert_called_once()
    sent_text = update.message.reply_text.call_args[0][0]
    assert "Привіт! Я бот для керування друзями" in sent_text


@pytest.mark.asyncio
@patch("app.bot.requests.get")
async def test_list_friends(mock_get):
    mock_get.return_value.json.return_value = [
        {"id": "1", "name": "Alex", "profession": "Dev"},
        {"id": "2", "name": "John", "profession": "QA"},
    ]
    mock_get.return_value.raise_for_status = lambda: None

    update = AsyncMock()
    context = AsyncMock()

    await bot.list_friends(update, context)

    update.message.reply_text.assert_called_once()
    sent_text = update.message.reply_text.call_args[0][0]
    assert "Alex" in sent_text
    assert "John" in sent_text


@pytest.mark.asyncio
@patch("app.bot.requests.get")
async def test_get_friend(mock_get):
    mock_get.return_value.json.return_value = {
        "name": "Alex",
        "profession": "Dev",
        "profession_description": "Python dev",
        "photo_url": "http://test.com/pic.jpg",
    }
    mock_get.return_value.raise_for_status = lambda: None

    update = AsyncMock()
    update.message.reply_text = AsyncMock()
    context = AsyncMock()
    context.args = ["123"]

    await bot.get_friend(update, context)

    update.message.reply_text.assert_called_once()
    sent_text = update.message.reply_text.call_args[0][0]
    assert "Alex" in sent_text
    assert "Dev" in sent_text
    assert "http://test.com/pic.jpg" in sent_text


@pytest.mark.asyncio
@patch("app.bot.requests.get")
async def test_get_friend_no_id(mock_get):
    update = AsyncMock()
    update.message.reply_text = AsyncMock()
    context = AsyncMock()
    context.args = []

    await bot.get_friend(update, context)

    update.message.reply_text.assert_called_once()
    text = update.message.reply_text.call_args[0][0]
    assert "Будь ласка, вкажіть ID друга" in text