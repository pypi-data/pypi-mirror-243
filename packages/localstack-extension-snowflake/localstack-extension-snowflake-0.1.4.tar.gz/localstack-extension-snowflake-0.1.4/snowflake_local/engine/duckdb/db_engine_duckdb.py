import logging,duckdb
from duckdb.typing import VARCHAR
from snowflake_local.engine.db_engine import DBEngine
from snowflake_local.engine.extension_functions import load_data
from snowflake_local.engine.models import Query,QueryResult,TableColumn
from snowflake_local.engine.transforms import QueryTransformsDuckDB
LOG=logging.getLogger(__name__)
class State:initialized=False
class DBEngineDuckDB(DBEngine):
	def execute_query(F,query):
		B=query;_define_util_functions()
		try:LOG.debug('Running duckdb query with queries: `%s` - %s',B.query,B.params);A=duckdb.execute(B.query,B.params)
		except Exception as C:
			if'already exists'in str(C)and'database'in str(C):return QueryResult()
			raise
		if not A:return QueryResult()
		D=[]
		for E in A.description:D.append(TableColumn(name=E[0],type_name=E[1]))
		G=list(A.fetchall());A=QueryResult(rows=G,columns=D);F._postprocess_result(A);return A
	def _postprocess_result(B,result):
		for A in result.columns:
			if A.name=='count_star()':A.name='count'
	def prepare_query(B,query):A=QueryTransformsDuckDB();return A.apply(query)
def _define_util_functions():
	if State.initialized:return
	State.initialized=True;duckdb.create_function('load_data',load_data,None,VARCHAR)