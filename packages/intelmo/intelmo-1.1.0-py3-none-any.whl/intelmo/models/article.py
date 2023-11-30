from typing import List, Optional
from pydantic import BaseModel
import json

from ..models.block import Block


class Article:
    def __init__(self, title: str, url: str, blocks: Optional[List['Block']] = None, global_block: Optional['Block'] = None):
        self.title = title
        self.url = url
        self.blocks = blocks
        self.global_block = global_block

    def copy(self):
        return Article(self.title, self.url, self.blocks, self.global_block)

    def to_dict(self):
        blocks_data = [block.to_dict()
                       for block in self.blocks] if self.blocks else []
        return {
            "title": self.title,
            "url": self.url,
            "blocks": blocks_data,
            "global_block": self.global_block.to_dict() if self.global_block else None
        }

    def to_json(self):
        return json.dumps(self.to_dict(), default=lambda o: o.__dict__, indent=4)

    @classmethod
    def from_dict(cls, data):
        blocks_data = data.get("blocks")
        blocks = [Block.from_dict(block_data)
                  for block_data in blocks_data] if blocks_data else []
        global_block_data = data.get("global_block")
        global_block = Block.from_dict(
            global_block_data) if global_block_data else None
        return cls(
            title=data["title"],
            url=data["url"],
            blocks=blocks,
            global_block=global_block
        )

    @classmethod
    def from_json(cls, data):
        return cls.from_dict(json.loads(data))

# convert to pydantic model
# class Article(BaseModel):
#     title: str
#     url: str
#     blocks: Optional[List[Block]] = None
#     global_block: Optional[Block] = None

#     def copy(self):
#         return Article(self.title, self.url, self.blocks, self.global_block)

#     def get_content(self):
#         return "\n".join(block.get_content() for block in self.blocks)
