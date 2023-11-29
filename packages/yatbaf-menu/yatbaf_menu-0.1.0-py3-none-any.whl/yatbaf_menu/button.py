from __future__ import annotations

__all__ = (
    "AbstractButton",
    "Action",
    "URL",
    "Submenu",
    "Back",
)

import asyncio
from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

from yatbaf.types import InlineKeyboardButton

from .filter import CallbackPayload
from .helpers import get_submenu

if TYPE_CHECKING:
    from collections.abc import Awaitable
    from collections.abc import Callable

    from yatbaf import OnCallbackQuery
    from yatbaf.types import CallbackQuery
    from yatbaf.typing import HandlerFunc

    from .menu import Menu
    from .typing import Query


class AbstractButton(ABC):
    __slots__ = ()

    @abstractmethod
    async def _build(self, q: Query, /) -> InlineKeyboardButton | None:
        pass

    @abstractmethod
    def _init(self, menu: Menu, router: OnCallbackQuery, /) -> None:
        pass


class BaseButton(AbstractButton):
    __slots__ = (
        "_title",
        "_dynamic_title",
        "_show",
    )

    def __init__(
        self,
        *,
        title: str | None = None,
        dynamic_title: Callable[[Query], Awaitable[str]] | None = None,
        show: Callable[[Query], Awaitable[bool]] | None = None,
    ) -> None:
        if title is None and dynamic_title is None:
            raise ValueError("you must use `title` or `dynamic_title`")
        self._title = title
        self._dynamic_title = dynamic_title
        self._show = show

    def __repr__(self) -> str:
        title = self._title or "`dynamic`"
        return f"<{self.__class__.__name__}[{title=!r}]>"

    async def _get_title(self, q: Query, /) -> str:
        if self._dynamic_title is not None:
            return await self._dynamic_title(q)
        return self._title

    async def _is_visible(self, q: Query, /) -> bool:
        if self._show is not None:
            return await self._show(q)
        return True


class Action(BaseButton):
    """This button does the action"""
    __slots__ = (
        "_action",
        "_payload",
    )

    def __init__(
        self,
        *,
        action: Callable[[Query], Awaitable[None]],
        title: str | None = None,
        dynamic_title: Callable[[Query], Awaitable[str]] | None = None,
        show: Callable[[Query], Awaitable[bool]] | None = None,
    ) -> None:
        """
        :param action: Callable to run on click.
        :param title: *Optional.* Button title.
        :param dynamic_title: *Optional.* Callable which returns button title.
        :param show: *Optional.* Callable which returns visibility status.

        .. important::

            You must use ``title`` or ``dynamic_title``.
        """
        super().__init__(
            title=title,
            dynamic_title=dynamic_title,
            show=show,
        )
        self._action = action
        self._payload: str | None = None

    def _init(self, m: Menu, r: OnCallbackQuery, /) -> None:
        if self._payload is not None:
            raise ValueError(
                f"{self!r}: you cannot register the same button twice."
            )

        for handler in r._handlers:
            if handler._fn is self._action:
                raise ValueError(
                    f"{self!r}: you cannot assign different buttons with the "
                    f"same action in in one menu ({m!r})."
                )

        # inject menu object to handler
        def middleware(
            handler: HandlerFunc[CallbackQuery]
        ) -> HandlerFunc[CallbackQuery]:

            async def wrapper(q: CallbackQuery) -> None:
                q.ctx["__menu__"] = m
                await handler(q)

            return wrapper

        self._payload = m._get_payload()
        r.add_handler(
            self._action,
            filters=[CallbackPayload(self._payload)],
            middleware=[middleware],
        )

    async def _build(self, q: Query, /) -> InlineKeyboardButton | None:
        if not await self._is_visible(q):
            return None

        return InlineKeyboardButton(
            text=await self._get_title(q),
            callback_data=self._payload,
        )


class URL(BaseButton):
    """This button will open URL"""
    __slots__ = (
        "_url",
        "_dynamic_url",
    )

    def __init__(
        self,
        url: str | None = None,
        dynamic_url: Callable[[Query], Awaitable[str]] | None = None,
        title: str | None = None,
        dynamic_title: Callable[[Query], Awaitable[str]] | None = None,
        show: Callable[[Query], Awaitable[bool]] | None = None,
    ) -> None:
        """
        :param url: URL.
        :param dynamic_url: Callable which returns url.
        :param title: *Optional.* Button title.
        :param dynamic_title: *Optional.* Callable which returns button title.
        :param show: *Optional.* Callable which returns visibility status.

        .. important::

            You must use ``url`` or ``dynamic_url`` and ``title`` or
            ``dynamic_title``.
        """
        super().__init__(
            title=title,
            dynamic_title=dynamic_title,
            show=show,
        )
        if url is None and dynamic_url is None:
            raise ValueError("you must use `url` or `dynamic_url`")

        self._url = url
        self._dynamic_url = dynamic_url

    def _init(self, m: Menu, r: OnCallbackQuery, /) -> None:  # noqa: U100
        pass  # nothing to do

    async def _get_url(self, q: Query, /) -> str:
        if self._dynamic_url is not None:
            return await self._dynamic_url(q)
        return self._url

    async def _build(self, q: Query, /) -> InlineKeyboardButton | None:
        if not await self._is_visible(q):
            return None

        async with asyncio.TaskGroup() as tg:
            title = tg.create_task(self._get_title(q))
            url = tg.create_task(self._get_url(q))

        return InlineKeyboardButton(
            text=title.result(),
            url=url.result(),
        )


class Submenu(BaseButton):
    """This button will open next menu"""
    __slots__ = (
        "_menu",
        "_payload",
    )

    def __init__(
        self,
        *,
        menu: str,
        title: str | None = None,
        dynamic_title: Callable[[Query], Awaitable[str]] | None = None,
        show: Callable[[Query], Awaitable[bool]] | None = None,
    ) -> None:
        """
        :param menu: Submenu name (see :class:`~yatbaf_menu.menu.Menu`).
        :param title: *Optional.* Button title.
        :param dynamic_title: *Optional.* Callable which returns button title.
        :param show: *Optional.* Callable which returns visibility status.

        .. important::

            You must use ``title`` or ``dynamic_title``.
        """
        super().__init__(
            title=title,
            dynamic_title=dynamic_title,
            show=show,
        )
        self._menu = menu
        self._payload: str | None = None

    def _init(self, m: Menu, r: OnCallbackQuery, /) -> None:  # noqa: U100
        if self._payload is not None:
            raise ValueError(
                f"{self!r}: you cannot register the same button twice."
            )
        self._payload = get_submenu(m, self._menu)._payload

    async def _build(self, q: Query, /) -> InlineKeyboardButton | None:
        if not await self._is_visible(q):
            return None

        return InlineKeyboardButton(
            text=await self._get_title(q),
            callback_data=self._payload,
        )


class Back(BaseButton):
    """This button will open previous menu"""
    __slots__ = (
        "_visible",
        "_payload",
    )

    def __init__(
        self,
        *,
        title: str | None = None,
        dynamic_title: Callable[[Query], Awaitable[str]] | None = None,
    ) -> None:
        """
        :param title: *Optional.* Button title.
        :param dynamic_title: *Optional.* Callable which returns button title.

        .. important::

            You must use ``title`` or ``dynamic_title``.
        """
        super().__init__(
            title=title,
            dynamic_title=dynamic_title,
        )
        self._visible: bool = False
        self._payload: str | None = None

    def _init(self, m: Menu, r: OnCallbackQuery, /) -> None:
        if self._payload is not None:
            raise ValueError(
                f"{self!r}: you cannot register the same button twice."
            )

        if m._parent is not None:
            self._visible = True
            self._payload = m._parent._payload

    async def _build(self, q: Query, /) -> InlineKeyboardButton | None:
        if not self._visible:
            return None

        return InlineKeyboardButton(
            text=await self._get_title(q),
            callback_data=self._payload,
        )
