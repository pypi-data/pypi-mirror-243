_G='OBJECT_CONSTRUCT'
_F='expression'
_E=None
_D=False
_C='postgres'
_B='this'
_A='kind'
import re
from typing import Callable
from localstack.utils.numbers import is_number
from sqlglot import exp,parse_one
from sqlglot.dialects import Snowflake
from snowflake_local.engine.models import Query
TYPE_MAPPINGS={'VARIANT':'JSONB','OBJECT':'JSONB','STRING':'TEXT'}
class QueryTransforms:
	def apply(C,query):
		A=query;B=parse_one(A.query,read='snowflake')
		for D in C.get_transformers():B=B.transform(D,query=A)
		A.query=B.sql(dialect=_C);return A
	def get_transformers(A):return[remove_transient_keyword,remove_if_not_exists,remove_create_or_replace,replace_unknown_types,replace_create_schema,replace_identifier_function,insert_create_table_placeholder,replace_json_field_access,replace_db_references]
class QueryTransformsPostgres(QueryTransforms):
	def get_transformers(A):return super().get_transformers()+[pg_replace_describe_table,pg_replace_show_schemas,pg_replace_show_objects,pg_replace_questionmark_placeholder,pg_replace_object_construct,pg_return_inserted_items]
class QueryTransformsDuckDB(QueryTransforms):
	def get_transformers(A):return super().get_transformers()+[ddb_replace_create_database,pg_replace_show_schemas,pg_replace_show_objects]
def remove_transient_keyword(expression,**F):
	E='properties';A=expression
	if not _is_create_table_expression(A):return A
	B=A.copy()
	if B.args[E]:
		C=B.args[E].expressions;D=exp.TransientProperty()
		if D in C:C.remove(D)
	return B
def remove_if_not_exists(expression,**D):
	C='exists';A=expression
	if not isinstance(A,exp.Create):return A
	B=A.copy()
	if B.args.get(C):B.args[C]=_D
	return B
def remove_create_or_replace(expression,**D):
	C='replace';A=expression
	if not isinstance(A,exp.Create):return A
	B=A.copy()
	if B.args.get(C):B.args[C]=_D
	return B
def replace_unknown_types(expression,**E):
	B=expression
	for(D,C)in TYPE_MAPPINGS.items():
		C=getattr(exp.DataType.Type,C.upper());A=B
		if isinstance(A,exp.Alias):A=A.this
		if isinstance(A,exp.Cast)and A.to==exp.DataType.build(D):A.args['to']=exp.DataType.build(C)
		if isinstance(B,exp.ColumnDef):
			if B.args.get(_A)==exp.DataType.build(D):B.args[_A]=exp.DataType.build(C)
	return B
def replace_create_schema(expression,query):
	A=expression
	if not isinstance(A,exp.Create):return A
	A=A.copy();B=A.args.get(_A)
	if str(B).upper()=='SCHEMA':query.database=A.this.db;A.this.args['db']=_E
	return A
def insert_create_table_placeholder(expression,query):
	A=expression
	if not _is_create_table_expression(A):return A
	if isinstance(A.this.this,exp.Placeholder)or str(A.this.this)=='?':A=A.copy();A.this.args[_B]=query.params.pop(0)
	return A
def replace_identifier_function(expression,**C):
	A=expression
	if isinstance(A,exp.Func)and str(A.this).upper()=='IDENTIFIER'and A.expressions:B=A.expressions[0].copy();B.args['is_string']=_D;return B
	return A
def replace_json_field_access(expression,**J):
	C=expression
	if not C.parent_select:return C
	if not isinstance(C,(exp.Dot,exp.Bracket)):return C
	F=_E;B=C;G=[]
	while hasattr(B,_B):
		if isinstance(B,(exp.Column,exp.Identifier)):F=B;break
		H=B.name or B.output_name;G.insert(0,H);B=B.this
	if not F:return C
	A=''
	for D in G:
		if is_number(D):A+=f"[{D}]"
		else:A+=f".{D}"
	A=A.strip('.')
	if not A.startswith('.'):A=f".{A}"
	if not A.startswith('$'):A=f"${A}"
	class I(exp.Binary,exp.Func):_sql_names=['get_path']
	E=I();E.args[_B]=B;E.args[_F]=f"'{A}'";return E
def replace_db_references(expression,query):
	E='catalog';C=query;A=expression;D=A.args.get(E)
	if isinstance(A,exp.Table)and A.args.get('db')and D:C.database=D.this;A.args[E]=_E
	if isinstance(A,exp.UserDefinedFunction):
		B=str(A.this).split('.')
		if len(B)==3:A.this.args[_B]=B[1];C.database=B[0]
	return A
def pg_replace_describe_table(expression,**G):
	A=expression
	if not isinstance(A,exp.Describe):return A
	C=A.args.get(_A)
	if str(C).upper()=='TABLE':B=A.this.name;D=f"'{B}'"if B else'?';E=f"SELECT * FROM information_schema.columns WHERE table_name={D}";F=parse_one(E,read=_C);return F
	return A
def pg_replace_show_schemas(expression,**F):
	A=expression
	if not isinstance(A,exp.Command):return A
	C=str(A.this).upper();B=str(A.args.get(_F)).strip().lower();B=B.removeprefix('terse').strip()
	if C=='SHOW'and B.startswith('schemas'):D='SELECT * FROM information_schema.schemata';E=parse_one(D,read=_C);return E
	return A
def pg_replace_show_objects(expression,**H):
	A=expression
	if not isinstance(A,exp.Command):return A
	E=str(A.this).upper();B=str(A.args.get(_F)).strip().lower();B=B.removeprefix('terse').strip()
	if E=='SHOW'and B.startswith('objects'):
		C='SELECT * FROM information_schema.tables';F='^\\s*objects\\s+(\\S+)\\.(\\S+)(.*)';D=re.match(F,B)
		if D:C+=f" WHERE table_schema = '{D.group(2)}'"
		G=parse_one(C,read=_C);return G
	return A
def pg_replace_questionmark_placeholder(expression,**B):
	A=expression
	if isinstance(A,exp.Placeholder):return exp.Literal(this='%s',is_string=_D)
	return A
def pg_replace_object_construct(expression,**H):
	C='expressions';A=expression
	if isinstance(A,exp.Func)and str(A.this).upper()==_G:
		class E(exp.Func):_sql_names=['TO_JSON_STR'];arg_types={_B:True,C:True}
		B=A.args[C]
		for D in range(1,len(B),2):F=B[D];B[D]=G=E();G.args[C]=F
	return A
def pg_return_inserted_items(expression,**B):
	A=expression
	if isinstance(A,exp.Insert):A.args['returning']=' RETURNING 1'
	return A
def ddb_replace_create_database(expression,**D):
	A=expression
	if isinstance(A,exp.Create)and str(A.args.get(_A)).upper()=='DATABASE':assert(C:=A.find(exp.Identifier)),f"No identifier in {A.sql}";B=C.this;return exp.Command(this='ATTACH',expression=exp.Literal(this=f"DATABASE ':memory:' AS {B}",is_string=True),create_db_name=B)
	return A
def _is_create_table_expression(expression,**C):A=expression;return isinstance(A,exp.Create)and(B:=A.args.get(_A))and isinstance(B,str)and B.upper()=='TABLE'
def _patch_sqlglot():Snowflake.Parser.FUNCTIONS.pop(_G,_E)
_patch_sqlglot()