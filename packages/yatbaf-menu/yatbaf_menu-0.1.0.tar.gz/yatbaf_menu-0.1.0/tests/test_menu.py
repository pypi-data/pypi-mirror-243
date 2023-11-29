import unittest.mock as mock

import pytest

from yatbaf import OnCallbackQuery
from yatbaf_menu import URL
from yatbaf_menu import Action
from yatbaf_menu import Back
from yatbaf_menu import Menu
from yatbaf_menu import Submenu


@pytest.fixture
def action():
    return mock.AsyncMock()


def test_menu():
    title = "menu_title"
    name = "menu_name"

    button = URL(title="button", url="t.me/bot")
    menu = Menu(
        title=title,
        name=name,
        buttons=[[button]],
    )

    assert menu._title == title
    assert menu._name == name
    assert menu._dynamic_title is None
    assert menu._parse_mode is None
    assert menu._router is None
    assert button in menu._buttons[-1]
    assert not menu._submenu
    assert not menu._middleware
    assert not menu._guards


def test_create_router():
    menu = Menu(title="title", name="name")
    router = menu._create_router()
    assert isinstance(router, OnCallbackQuery)


def test_create_router_guards():
    guard = object()
    menu = Menu(title="title", name="name", guards=[guard])
    router = menu._create_router()
    assert guard in router._guards


def test_create_router_middleware():
    middleware = object()
    menu = Menu(title="title", name="name", middleware=[middleware])
    router = menu._create_router()
    assert middleware in router._middleware


def test_init_button_url():
    button = URL(title="title", url="url")
    menu = Menu(
        title="title",
        name="name",
        buttons=[[button]],
    )
    router = menu._create_router()
    menu._init_buttons(router)
    # `open_menu` handler
    assert len(router._handlers) == 1


def test_init_button_action(action):
    button = Action(title="title", action=action)
    menu = Menu(
        title="title",
        name="name",
        buttons=[[button]],
    )
    router = OnCallbackQuery()
    menu._init_buttons(router)
    assert len(router._routers) == 1
    assert button._payload is not None
    # 1st router is `open_menu`
    assert router._routers[0]._handlers[1]._fn is action


def test_button_action_duplicate_action(action):
    button1 = Action(title="title1", action=action)
    button2 = Action(title="title2", action=action)
    menu = Menu(
        title="title",
        name="name",
        buttons=[[button1, button2]],
    )
    router = OnCallbackQuery()
    with pytest.raises(ValueError):
        menu._init_buttons(router)


def test_button_action_duplicate_button(action):
    button1 = Action(title="title1", action=action)
    menu = Menu(
        title="title",
        name="name",
        buttons=[[button1, button1]],
    )
    router = OnCallbackQuery()
    with pytest.raises(ValueError):
        menu._init_buttons(router)


def test_button_action_duplicate_diff_menu(action):
    button1 = Action(title="title1", action=action)
    menu1 = Menu(
        title="title",
        name="name",
        buttons=[[button1]],
    )
    router1 = OnCallbackQuery()
    menu1._init_buttons(router1)

    menu2 = Menu(
        title="title",
        name="name",
        buttons=[[button1]],
    )

    router2 = OnCallbackQuery()
    with pytest.raises(ValueError):
        menu2._init_buttons(router2)


def test_button_back_duplicate_button():
    button = Back(title="back")
    menu = Menu(
        title="title",
        name="name",
        buttons=[[Submenu(title="button", menu="name1")]],
        submenu=[
            Menu(
                title="title",
                name="name1",
                buttons=[[button, button]],
            ),
        ],
    )
    router = OnCallbackQuery()
    with pytest.raises(ValueError):
        menu._init_menu(router)


def test_empty_menu():
    menu = Menu(
        title="title",
        name="name",
    )
    router = OnCallbackQuery()
    with pytest.raises(ValueError):
        menu._init_buttons(router)


@pytest.mark.asyncio
async def test_menu_markup_url_button():
    title = "button"
    url = "t.me/bot"
    button = URL(title=title, url=url)
    menu = Menu(
        title="title",
        name="name",
        buttons=[[button]],
    )

    router = menu.get_router()
    # `open_menu` handler
    assert len(router._routers[0]._handlers) == 1

    layout = (await menu._get_markup(None)).inline_keyboard
    assert len(layout) == 1
    assert len(layout[0]) == 1
    assert layout[0][0].text == title
    assert layout[0][0].url == url
    assert layout[0][0].callback_data is None


@pytest.mark.asyncio
async def test_menu_markup_action_button(action):
    title = "button"
    button = Action(title=title, action=action)
    menu = Menu(
        title="title",
        name="name",
        buttons=[[button]],
    )

    router = menu.get_router()
    assert router._routers[0]._handlers[1]._fn is action

    layout = (await menu._get_markup(None)).inline_keyboard
    assert len(layout) == 1
    assert len(layout[0]) == 1
    assert layout[0][0].text == title
    assert layout[0][0].url is None
    assert layout[0][0].callback_data is not None
    assert layout[0][0].callback_data.startswith(menu._payload)


def test_menu_markup_submenu_button_no_submenu_back_button():
    submenu = "submenu"
    menu = Menu(
        title="title",
        name="name",
        buttons=[[Submenu(title="button", menu=submenu)]],
        submenu=[
            Menu(
                title="submenu",
                name=submenu,
            ),
        ],
    )
    with pytest.raises(ValueError):
        menu.get_router()


@pytest.mark.asyncio
async def test_menu_markup_submenu_button():
    title = "button"
    submenu = "submenu"
    button = Submenu(title=title, menu=submenu)
    menu = Menu(
        title="title",
        name="name",
        buttons=[[button]],
        submenu=[
            Menu(
                title="submenu",
                name=submenu,
                back_button_title="back",
            ),
        ],
    )

    router = menu.get_router()
    router = menu.get_router()
    assert len(router._routers[0]._handlers) == 1

    main_layout = (await menu._get_markup(None)).inline_keyboard
    assert len(main_layout) == 1
    assert len(main_layout[0]) == 1
    assert main_layout[0][0].text == title
    assert main_layout[0][0].url is None
    assert main_layout[0][0].callback_data.startswith(menu._payload)

    submenu_layout = (
        await menu._submenu[submenu]._get_markup(None)
    ).inline_keyboard
    assert submenu_layout[0][0].text == "back"
    assert submenu_layout[0][0].url is None
    assert submenu_layout[0][0].callback_data.startswith(menu._payload)

    # submenu `Back` button
    assert menu._submenu[submenu]._buttons
