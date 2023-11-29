import unittest.mock as mock

import pytest

from yatbaf import OnCallbackQuery
from yatbaf.types import InlineKeyboardButton
from yatbaf_menu import Action
from yatbaf_menu import Menu
from yatbaf_menu import Submenu
from yatbaf_menu.button import BaseButton


@pytest.fixture
def router():
    return OnCallbackQuery()


@pytest.fixture
def query():
    return mock.Mock()


class Button(BaseButton):

    async def _build(self, _):
        pass

    def _init(self, _, __):
        pass


@pytest.mark.asyncio
async def test_is_visible(query):
    assert await Button(title="title")._is_visible(query)


@pytest.mark.asyncio
@pytest.mark.parametrize("visible", [True, False])
async def test_is_visible_dynamic(visible, query):

    async def dyn_show(_):
        return visible

    button = Button(title="button", show=dyn_show)
    if visible:
        assert await button._is_visible(query)
    else:
        assert not await button._is_visible(query)


@pytest.mark.asyncio
async def test_get_title(query):
    title = "button_title"
    assert await Button(title=title)._get_title(query) == title


@pytest.mark.asyncio
@pytest.mark.parametrize("title", ["open", "close"])
async def test_get_title_dynamic(title):

    async def dyn_title(_):
        return title

    assert await Button(dynamic_title=dyn_title)._get_title(None) == title


def test_button_title_error():
    with pytest.raises(ValueError):
        Button()


def test_init_submenu_button_error(router):
    button = Submenu(title="submenu", menu="submenu")
    menu = Menu(title="menu", name="menu")

    with pytest.raises(ValueError):
        button._init(menu, router)


@pytest.mark.asyncio
async def test_submenu_button(router):
    button = Submenu(title="submenu", menu="submenu")
    submenu = Menu(title="submenu", name="submenu")
    menu = Menu(title="menu", name="menu", submenu=[submenu])

    button._init(menu, router)
    assert button._payload == submenu._payload
    assert not router._handlers

    result = await button._build(query)
    assert result is not None
    assert result == InlineKeyboardButton(
        text="submenu",
        callback_data=submenu._payload,
    )


@pytest.mark.asyncio
async def test_action_button(query, router):

    async def action(_):
        pass

    menu = Menu(title="menu", name="menu")
    button = Action(title="button", action=action)
    button._init(menu, router)

    assert button._payload is not None
    assert router._handlers[0]._fn is action
    assert router._handlers[0]._filters[0].payload == button._payload

    result = await button._build(query)
    assert result is not None
    assert result == InlineKeyboardButton(
        text="button",
        callback_data=button._payload,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("visible", [True, False])
async def test_action_button_dyn_show(visible, query, router):

    async def action(_):
        pass

    async def show(_):
        return visible

    menu = Menu(title="menu", name="menu")
    button = Action(title="button", action=action, show=show)
    button._init(menu, router)
    result = await button._build(query)

    if visible:
        assert result is not None
        assert result == InlineKeyboardButton(
            text="button",
            callback_data=button._payload,
        )
    else:
        assert result is None
