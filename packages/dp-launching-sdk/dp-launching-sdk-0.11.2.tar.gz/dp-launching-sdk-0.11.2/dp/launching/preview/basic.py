from dp.launching.typing.basic import BaseModel
from typing import Any, Optional, Callable
from dataclasses import dataclass, field


@dataclass
class TableBasicProps:
    df: Any
    columns: list
    row_key: Optional[list] = field(default=None)
    hidden_columns: Optional[list] = field(default=None)
    fixed_left_columns: Optional[list] = field(default=None)
    fixed_right_columns: Optional[list] = field(default=None)
    custom_columns_width: Optional[dict] = field(default=None)
    default_column_width: int = field(default=None)
    tags_columns: Optional[list] = field(default=None)
    sorter_columns: Optional[list] = field(default=None)
    searchable_columns: Optional[list] = field(default=None)
    iframes_mapper: Optional[Callable] = field(default=None)
    actions: Optional[list] = field(default=None)
    actions_mapper: Optional[Callable] = field(default=None)
    iframe_height: int = field(default=300)
    default_expand_all_rows: Optional[bool] = field(default=False)
    batch_actions: Optional[list] = field(default=None)
    linkable_columns: Optional[list] = field(default=None)
    expand_column: Optional[str] = field(default=None)
    expand_json: Optional[bool] = field(default=False)
    action_width: Optional[int] = field(default=None)
    compact_layout: bool = field(default=False)
    show_pager: bool = field(default=True)
    color_backgroud: str = field(default="#f0f0f0")
    rows_per_page: int = field(default=20)
    min_height: int = field(default=200)
    enable_dynamic_pager: bool = field(default=False)
    dynamic_pager_total: int = field(default=0)
    dynamic_pager_page: int = field(default=0)
    unsafe_html_columns: Optional[list] = field(default=None)
    key: Optional[str] = field(default=None)


@dataclass
class DynamicTableProps(TableBasicProps):
    key: Optional[str] = field(default=None)
    df_loader: Callable = field(default=None)
    total: int = field(default=None)
    page_size: int = field(default=10)
    state: Optional[Any] = field(default=None)


class DynamicTable(BaseModel):
    Props = DynamicTableProps
    props: DynamicTableProps
    format = "dynamic_table"
    scope = "preview"


DynamicTable.Props = DynamicTableProps


class Table(BaseModel):
    Props = TableBasicProps
    props: TableBasicProps
    format = "table"
    scope = "preview"
