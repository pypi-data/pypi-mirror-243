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


class ContactMessage:
    """This object shows a Message Contact.

    Attributes
    ----------
        phone_number: int
        first_name: :class:`str`
        last_name: Optional[:class:`str`]
    """
    __slots__ = (
        "phone_number",
        "first_name",
        "last_name",
        "bot"
    )

    def __init__(self, phone_number: int, first_name: str = None, last_name: str = None):
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def from_dict(cls, data: dict):
        return cls(first_name=data.get("first_name"), last_name=data.get("last_name"), phone_number=data.get("phone_number"))

    def to_dict(self):
        return {
            'phone_number': self.phone_number,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

    def __eq__(self, other):
        return isinstance(other, ContactMessage) and self.phone_number == other.phone_number

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"<ContactMessage phone_number={self.phone_number} first_name={self.first_name} last_name={self.last_name} >"
