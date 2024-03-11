
from .streams import StreamOut

import zlib
import json

class TPKEncoder:
    def __init__(self, atlas: bytes, json: dict) -> None:
        self.stream = StreamOut()
        self.atlas = atlas
        self.json = json
        self.interval = 67 # TODO
        self.scale = {}    # TODO

    @property
    def sections(self) -> dict:
        return {
            "i": self.interval.to_bytes(4, 'big'),
            "t": self.atlas,
            "j": bytes(json.dumps(self.json), 'utf-8'),
            "m": bytes(json.dumps(self.scale), 'utf-8')
        }

    @classmethod
    def from_files(
        cls,
        atlas_filename: str,
        json_filename: str
    ) -> "TPKEncoder":
        with open(atlas_filename, 'rb') as file:
            atlas = file.read()
        with open(json_filename, 'r') as file:
            data = file.read()
        return cls(atlas, json.loads(data))

    def to_bytes(self) -> bytes:
        self.stream.write(b"KAPD")
        self.stream.u16(len(self.sections))

        for data in self.sections.values():
            self.stream.u32(len(data))

        for name in self.sections.keys():
            self.stream.u16(len(name))
            self.stream.write(bytes(name, 'utf-8'))

        for data in self.sections.values():
            self.stream.write(data)

        return zlib.compress(self.stream.get())

    def to_file(self, filename: str) -> None:
        with open(filename, 'wb') as file:
            file.write(self.to_bytes())
