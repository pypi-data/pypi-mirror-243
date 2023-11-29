from dataclasses import dataclass, field
from enum import Enum


class TableFieldAlignment(Enum):

    LEFT = 'left'
    CENTER = 'center'
    RIGHT = 'right'


class TableFieldType(Enum):

    NONE = ''
    STRING = '_string'
    MONETARY = '_monetary'
    FLOAT = '_float'


@dataclass
class TableField:

    label: str
    name: str
    alignment: type[TableFieldAlignment] = TableFieldAlignment.LEFT
    header_alignment: type[TableFieldAlignment] = None
    field_type: type[TableFieldType] = TableFieldType.NONE
    prefix: str = ''
    suffix: str = ''
    truncate_after: int = 0


@dataclass
class BreadCrumb:

    name: str
    url: str


@dataclass
class ClientAction:

    name: str
    url: str = ''
    query_params: str = ''
    attrs: list[str] = field(default_factory=list)
    submit: bool = False
    form_id: str = 'form'
    class_list: list = field(default_factory=list)
