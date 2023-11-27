_A=None
import dataclasses
from sqlglot import exp
@dataclasses.dataclass
class Query:query:str|exp.Expression;params:list|_A=_A;database:str|_A=_A
@dataclasses.dataclass
class TableColumn:name:str;type_name:str;type_size:int=0
@dataclasses.dataclass
class QueryResult:rows:list[tuple]=dataclasses.field(default_factory=list);columns:list[TableColumn]=dataclasses.field(default_factory=list)