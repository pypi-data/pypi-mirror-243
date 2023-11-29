from __future__ import annotations

from typing import TYPE_CHECKING
from typing import TypeAlias

if TYPE_CHECKING:
    from yatbaf.types import CallbackQuery
    from yatbaf.types import Message

    from .button import AbstractButton

Layout: TypeAlias = "list[list[AbstractButton]]"
Query: TypeAlias = "Message | CallbackQuery"
