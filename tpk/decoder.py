
from .streams import StreamIn

from typing import Dict

import struct
import json
import zlib

class TPKDecoder:
    def __init__(self) -> None:
        self.sections: Dict[str, bytes] = {}
        self.atlas: bytes = b''
        self.interval: int = 67
        self.json: dict = {}
        self.scale: dict = {}

    @classmethod
    def from_file(cls, filename: str) -> "TPKDecoder":
        with open(filename, 'rb') as file:
            p = cls()
            p.parse(file.read())
            return p

    @classmethod
    def from_bytes(cls, data: bytes) -> "TPKDecoder":
        p = cls()
        p.parse(data)
        return p

    def parse(self, data: bytes) -> None:
        # Decompress the file with zlib
        stream = StreamIn(zlib.decompress(data))

        # Verify header
        assert stream.read(4) == b"KAPD", "Invalid TPK file"

        # Read how many sections there are and their size
        sizes = [stream.u32() for _ in range(stream.u16())]

        # Get the names for the sections (i, t, j, m)
        section_names = [
            stream.read(stream.u16()).decode()
            for _ in range(len(sizes))
        ]

        # Read the sections based on their size
        self.sections = {
            section_names[index]: stream.read(size)
            for index, size in enumerate(sizes)
        }

        self.atlas = self.sections.get('t', b'')
        self.json = json.loads(self.sections.get('j', '{}').decode())
        self.scale = json.loads(self.sections.get('m', '{}').decode())
        self.interval = struct.unpack('>I', self.sections.get('i', b'\x00\x00\x00C'))[0]
