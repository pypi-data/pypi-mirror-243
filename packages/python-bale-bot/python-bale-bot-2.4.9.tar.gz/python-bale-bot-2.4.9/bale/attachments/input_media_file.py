from __future__ import annotations
from typing import Optional, Dict
from io import BufferedReader
from bale.utils import MediaType, MediaTypeRaw, to_json
from . import InputFile, Audio, Photo, Document, Animation, Video


__all__ = (
    "InputMediaFile",
)

class InputMediaFile(InputFile):
    __slots__ = InputFile.__slots__ + (
        "media_type",
    )

    def __init__(self, media_type: MediaType, file: str | "BufferedReader" | bytes):
        if not isinstance(media_type, (Audio, Photo, Document, Animation, Video)):
            raise TypeError(
                "media_type param must be type of attachments class"
            )

        super().__init__(file)
        self.media_type: MediaTypeRaw = media_type.__FILE_TYPE__

    def to_dict(self) -> Dict:
        payload = {
            "media": self.file,
            "type": self.media_type
        }

        return payload

    def to_json(self) -> str:
        return to_json(self.to_dict())