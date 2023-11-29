"""
MIT License

Copyright (c) 2023 Kian Ahmadian

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Optional
from json import dumps
if TYPE_CHECKING:
    from bale import Bot

class BaleObject:
    def __init__(self):
        self.__bot = None

    @property
    def bot(self) -> Optional["Bot"]:
        return self.__bot

    @bot.setter
    def bot(self, value):
        self.set_bot(value)

    def to_json(self) -> str:
        return dumps(self.to_dict())

    def to_dict(self) -> "Dict":
        function = self.__dict__


    def set_bot(self, bot: "Bot"):
        if not isinstance(bot, Bot):
            raise TypeError(
                "bot param must be type of Bot"
            )

        self.__bot = bot