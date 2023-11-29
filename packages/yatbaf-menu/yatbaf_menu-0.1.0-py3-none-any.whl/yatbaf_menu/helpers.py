from __future__ import annotations

__all__ = (
    "open_main_menu",
    "open_previous_menu",
    "open_menu",
    "refresh_menu",
)

from typing import TYPE_CHECKING
from typing import Literal

from yatbaf.exceptions import MethodInvokeError

if TYPE_CHECKING:
    from yatbaf.types import CallbackQuery

    from .menu import Menu

MENU_CTX: Literal["__menu__"] = "__menu__"


def get_submenu(menu: Menu, name: str, /) -> Menu:
    try:
        return menu.submenu[name]
    except KeyError:
        raise ValueError(f"Menu {name!r} not found in {menu!r}") from None


def find_menu(menu: Menu, path: str, /) -> Menu:
    for name in path.split("."):
        menu = get_submenu(menu, name)
    return menu


def find_root(menu: Menu, /) -> Menu:
    while menu._parent is not None:
        menu = menu._parent
    return menu


async def open_previous_menu(q: CallbackQuery, /) -> None:
    menu: Menu = q.ctx[MENU_CTX]
    if menu._parent is None:
        return
    await q.message.edit(**(await menu.get_message_params(q)))


async def open_main_menu(q: CallbackQuery, /) -> None:
    menu = find_root(q.ctx[MENU_CTX])
    await q.message.edit(**(await menu.get_message_params(q)))


async def open_menu(q: CallbackQuery, path: str, /) -> None:
    menu: Menu = q.ctx[MENU_CTX]
    if path[0] == ".":
        menu = find_menu(menu, path[1:])
    else:
        menu = find_menu(find_root(menu), path)

    await q.message.edit(**(await menu.get_message_params(q)))


async def refresh_menu(q: CallbackQuery, /) -> None:
    menu: Menu = q.ctx[MENU_CTX]
    await q.message.edit(**(await menu.get_message_params(q)))


async def close_menu(q: CallbackQuery, /) -> None:
    try:
        await q.message.delete()
    except MethodInvokeError:
        await q.message.edit_reply_markup()
