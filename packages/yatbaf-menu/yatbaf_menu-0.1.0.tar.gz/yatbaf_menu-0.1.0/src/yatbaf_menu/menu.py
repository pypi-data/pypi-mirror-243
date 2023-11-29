from __future__ import annotations

__all__ = ("Menu",)

import asyncio
from typing import TYPE_CHECKING
from typing import Any
from typing import final

from yatbaf import OnCallbackQuery
from yatbaf.types import InlineKeyboardMarkup

from .button import Back
from .filter import CallbackPayload
from .payload import Payload

if TYPE_CHECKING:
    from collections.abc import Awaitable
    from collections.abc import Callable
    from collections.abc import Sequence

    from yatbaf.enums import ParseMode
    from yatbaf.types import CallbackQuery
    from yatbaf.typing import Context
    from yatbaf.typing import Guard
    from yatbaf.typing import Middleware

    from .typing import Layout
    from .typing import Query

_root_payload_bucket = Payload()


@final
class Menu:
    """Menu object."""

    __slots__ = (
        "_title",
        "_name",
        "_submenu",
        "_buttons",
        "_guards",
        "_middleware",
        "_context",
        "_dynamic_title",
        "_back_button_title",
        "_parse_mode",
        "_parent",
        "_payload",
        "_bucket",
        "_router",
    )

    def __init__(
        self,
        *,
        name: str,
        title: str | None = None,
        buttons: Layout | None = None,
        dynamic_title: Callable[[Query], Awaitable[str]] | None = None,
        submenu: Sequence[Menu] | None = None,
        guards: Sequence[Guard[CallbackQuery]] | None = None,
        middleware: Sequence[Middleware[CallbackQuery]] | None = None,
        back_button_title: str | None = None,
        parse_mode: ParseMode | None = None,
        context: Context | None = None,
    ) -> None:
        """
        :param name: Menu name.
        :param title: *Optional.* Menu title.
        :param dynamic_title: *Optional.* Callable which return menu title.
        :param submenu: *Optional.* Sequence of :class:`Menu`.
        :param parse_mode: *Optional.* Parse mode for menu title.
        :param back_button_title: *Optional.* Pass a title if you want to add
            a 'back button' to this menu. For submenu only.
        :param guards: *Optional.* Sequence of :class:`~yatbaf.typing.Guard`
        :param middleware: *Optional.* Sequence of :class:`~yatbaf.typing.Middleware`
        :param context: *Optional.* :class:`~yatbaf.typing.Context` function.
        """  # noqa: E501
        self._name = name
        self._title = title
        self._dynamic_title = dynamic_title

        if title is None and dynamic_title is None:
            raise ValueError("you must use 'title' or 'dynamic_title'")

        self._submenu = {} if submenu is None else {m.name: m for m in submenu}
        self._buttons = buttons if buttons is not None else []
        self._guards = guards if guards is not None else []
        self._middleware = middleware if middleware is not None else []
        self._context = context

        self._back_button_title = back_button_title

        self._parse_mode = parse_mode
        self._parent: Menu | None = None
        self._payload = _root_payload_bucket.get()
        self._bucket = Payload()
        self._router: OnCallbackQuery | None = None

    def __repr__(self) -> str:
        return f"<Menu[{self._name}]>"

    @property
    def name(self) -> str:
        return self._name

    @property
    def submenu(self) -> dict[str, Menu]:
        return self._submenu

    async def _get_title(self, q: Query, /) -> str:
        if self._dynamic_title is not None:
            return await self._dynamic_title(q)
        return self._title

    async def _get_markup(self, q: Query, /) -> InlineKeyboardMarkup:
        async with asyncio.TaskGroup() as tg:
            # yapf: disable
            tasks = [
                [tg.create_task(btn._build(q)) for btn in row]
                for row in self._buttons
            ]
            # yapf: enable

        return InlineKeyboardMarkup([
            buttons for row in tasks if
            (buttons := [button for task in row if (button := task.result())])
        ])

    def _get_payload(self) -> str:
        return self._payload + self._bucket.get()

    async def get_message_params(self, query: Query) -> dict[str, Any]:
        """Create parameters for message.

        Use it to open menu::

            @on_message(filters=[Command("menu")])
            async def open_menu(message: Message) -> None:
                params = await menu.get_message_params(message)
                await message.answer(**params)

        :param query: :class:`~yatbaf.types.message.Message` or
            :class:`~yatbaf.types.callback_query.CallbackQuery` object.
        """
        async with asyncio.TaskGroup() as tg:
            title = tg.create_task(self._get_title(query))
            markup = tg.create_task(self._get_markup(query))

        return {
            "text": title.result(),
            "reply_markup": markup.result(),
            "parse_mode": self._parse_mode,
        }

    def _create_router(self) -> OnCallbackQuery:
        router = OnCallbackQuery(
            name=f"menu-{self.name}:{self._payload}",
            skip_with_nested=True,
            middleware=self._middleware,
            context=self._context,
        )

        @router.guard
        async def guard(query: CallbackQuery) -> bool:
            return query.data.startswith(self._payload)

        @router(filters=[CallbackPayload(self._payload)])
        async def open_menu(query: CallbackQuery) -> None:
            params = await self.get_message_params(query)
            await query.answer()
            await query.message.edit(**params)

        for func in self._guards:
            router.add_guard(func)

        return router

    def _init_buttons(self, router: OnCallbackQuery) -> None:
        if not self._buttons:
            raise ValueError(f"{self} has no buttons.")

        current_router = self._create_router()
        for row in self._buttons:
            for button in row:
                button._init(self, current_router)

        router.add_router(current_router)
        for menu in self._submenu.values():
            menu._init_buttons(current_router)

    def _init_submenu(self) -> None:
        for menu in self._submenu.values():
            _root_payload_bucket.put(menu._payload)
            menu._payload = self._get_payload()
            menu._parent = self

            # add `Back` button
            if menu._back_button_title is not None:
                menu._buttons.append([Back(title=menu._back_button_title)])
            menu._init_submenu()

    def _init_menu(self, router: OnCallbackQuery) -> None:
        self._init_submenu()
        self._init_buttons(router)

    def get_router(self) -> OnCallbackQuery:
        """Create router based on menu layout."""
        if self._router is None:
            router = OnCallbackQuery(
                name=f"{self._name}-router",
                skip_with_nested=True,
            )

            @router.guard
            async def guard(query: CallbackQuery) -> bool:
                return query.data is not None

            self._init_menu(router)
            self._router = router

        return self._router
