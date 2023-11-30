from __future__ import annotations
from enum import Enum
from typing import Callable, List, Optional, Type, TYPE_CHECKING
from pydantic import BaseModel
from uuid import uuid4
import json

if TYPE_CHECKING:
    from models.article import Article


class BlockTypeEnum(Enum):
    """Enum for type of block"""
    Normal = "normal"
    Bold = "bold"
    Italic = "italic"
    Underline = "underline"
    Light = "light"
    Title = "title"
    Custom = "custom"
    Quote = "quote"
    Checkbox = "checkbox"
    Button = "button"


class BlockLevelEnum(Enum):
    Paragraph = "paragraph"
    Sentence = "sentence"
    Word = "word"
    Global = "global"


class BlockStatusEnum(Enum):
    Untouched = "untouched"
    New = "new"
    Modified = "modified"


BlockAction = Callable[["Article", "Block"], "Article"]


class Block:
    def __init__(self, level: BlockLevelEnum, type: BlockTypeEnum, content: Optional[str],
                 children: Optional[List['Block']], status: Optional[BlockStatusEnum] = None,
                 extra: Optional['Block'] = None,
                 onclick: Optional['BlockAction'] = None,
                 render: Callable = None,
                 # allow any custom data to be stored in the block
                 id: str = None,
                 custom_data: Optional[dict] = None
                 ):
        self.level = level
        self.type = type
        self.content = content
        self.children = children
        self.status = status if status is not None else BlockStatusEnum.Untouched
        self.extra = extra
        self.onclick = onclick
        self.render = render
        self.id = str(uuid4()) if id is None else id
        self.custom_data = custom_data if custom_data is not None else {}

    def __dict__(self):
        children = []
        if self.children is not None:
            children = [subBlock.__dict__ for subBlock in self.children]
        return {
            "level": self.level.value,
            "type": self.type.value,
            "content": self.content,
            "blocks": children,
            "status": self.status.value,
            "extra": self.extra if self.extra is not None else "",
            "id": self.id,
            "custom_data": self.custom_data if self.custom_data is not None else ""
        }

    def print_tree(self, header="", last=True):
        elbow = "└──"
        pipe = "│  "
        tee = "├──"
        blank = "   "
        # content = self.content if self.content is not None else "" + "
        content = f"{self.content} ({self.status.value}) ({self.type.value}) ({self.level.value})"
        print((elbow if last else tee) + content)
        if self.children is not None:
            children = self.children
            for i, c in enumerate(children):
                c.print_tree(header=header + (blank if last else pipe),
                             last=i == len(children) - 1)

    def get_content(self):
        if self.content is None:
            return "".join([child.get_content() for child in self.children])
        return self.content

    def to_dict(self):
        children = [child.to_dict()
                    for child in self.children] if self.children else []
        return {
            "level": self.level.value,
            "type": self.type.value,
            "content": self.content,
            "children": children,
            "status": self.status.value,
            "id": self.id,
            "extra": self.extra.to_dict() if self.extra else None,
            "custom_data": self.custom_data if self.custom_data else None
        }

    @classmethod
    def from_dict(cls, data):
        children_data = data.get("children")
        children = [cls.from_dict(child_data)
                    for child_data in children_data] if children_data else []
        return cls(
            level=BlockLevelEnum(data["level"]),
            type=BlockTypeEnum(data["type"]),
            content=data["content"],
            children=children,
            status=BlockStatusEnum(data["status"]),
            id=data["id"],
            extra=cls.from_dict(data["extra"]) if data.get("extra") else None,
            custom_data=data.get("custom_data"),
        )


# convert to pydantic model
# class Block(BaseModel):
#     level: BlockLevelEnum
#     type: BlockTypeEnum
#     content: Optional[str]
#     children: Optional[List[Block]] = None
#     status: Optional[BlockStatusEnum] = None
#     extra: Optional[Block] = None
#     onclick: Optional[BlockAction] = None
#     render: Callable = None
#     id: str
#     custom_data: Optional[dict] = None

#     def __init__(self, level: BlockLevelEnum, type: BlockTypeEnum, content: Optional[str],
#                  children: Optional[List['Block']], status: Optional[BlockStatusEnum] = None,
#                  extra: Optional['Block'] = None,
#                  onclick: Optional['BlockAction'] = None,
#                  render: Callable = None,
#                  # allow any custom data to be stored in the block
#                  custom_data: Optional[dict] = None
#                  ):
#         super().__init__(
#             level=level,
#             type=type,
#             content=content,
#             children=children,
#             status=status if status is not None else BlockStatusEnum.Untouched,
#             extra=extra,
#             onclick=onclick,
#             render=render,
#             id=uuid4(),
#             custom_data=custom_data
#         )

#     def print_tree(self, header="", last=True):
#         elbow = "└──"
#         pipe = "│  "
#         tee = "├──"
#         blank = "   "
#         # content = self.content if self.content is not None else "" + "
#         content = f"{self.content} ({self.status.value}) ({self.type.value}) ({self.level.value})"
#         print((elbow if last else tee) + content)
#         if self.children is not None:
#             children = self.children
#             for i, c in enumerate(children):
#                 c.print_tree(header=header + (blank if last else pipe),
#                              last=i == len(children) - 1)

#     def get_content(self):
#         if self.content is None:
#             return "".join([child.get_content() for child in self.children])
#         return self.content

#     def __dict__(self):
#         children = []
#         if self.children is not None:
#             children = [subBlock.__dict__ for subBlock in self.children]
#         return {
#             "level": self.level.value,
#             "type": self.type.value,
#             "content": self.content,
#             "blocks": children,
#             "status": self.status.value,
#             "extra": self.extra if self.extra is not None else "",
#             "custom_data": self.custom_data if self.custom_data is not None else ""
#         }
