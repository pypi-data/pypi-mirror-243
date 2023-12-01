import base64,logging,re
from localstack.utils.strings import to_bytes,to_str,truncate
from simple_ddl_parser import DDLParser
from snowflake_local.engine.db_engine import get_db_engine
from snowflake_local.engine.models import Query,QueryResult
LOG=logging.getLogger(__name__)
def cleanup_query(query):A=query;A=A.strip(' ;');A=re.sub('/\\*.*?\\*/','',A,flags=re.I);A=re.sub('^\\s*--.*','',A,flags=re.M);return A
def execute_query(query):A=query;B=get_db_engine();A=prepare_query(A);return B.execute_query(A)
def prepare_query(query_obj):A=query_obj;A.query=A.query.replace('\n',' ');A.query=_create_tmp_table_for_file_queries(A.query);B=get_db_engine();A=B.prepare_query(A);return A
def insert_rows_into_table(table,rows,schema=None,database=None):
	I=database;H=schema;G=table;F=', ';A=rows;J=f'"{H}"."{G}"'if H else G
	if A and isinstance(A[0],dict):
		B=set()
		for C in A:B.update(C.keys())
		B=list(B);K=F.join(B);E=F.join(['?'for A in B]);L=f"INSERT INTO {J} ({K}) VALUES ({E})"
		for C in A:M=[C.get(A)for A in B];D=Query(query=L,params=list(M),database=I);execute_query(D)
	elif A and isinstance(A[0],(list,tuple)):
		for C in A:N=len(C);E=F.join(['?'for A in range(N)]);D=f"INSERT INTO {J} VALUES ({E})";D=Query(query=D,params=list(C),database=I);execute_query(D)
	elif A:raise Exception(f"Unexpected values when storing list of rows to table: {truncate(str(A))}")
def _create_tmp_table_for_file_queries(query):
	A=query;C='(\\s*SELECT\\s+.+\\sFROM\\s+)(@[^\\(\\s]+)(\\s*\\([^\\)]+\\))?';F=re.match(C,A)
	if not F:return A
	G=re.findall('\\$\\d+',A);D='_col1 TEXT';B=[int(A.removeprefix('$'))for A in G]
	if B:H=list(range(1,max(B)+1));D=','.join([f"_col{A} TEXT"for A in H])
	def I(match):A=match;B=to_str(base64.b64encode(to_bytes(A.group(3)or'')));return f"{A.group(1)} load_data('{A.group(2)}', '{B}') as _tmp({D})"
	A=re.sub(C,I,A)
	if B:
		for E in range(max(B),0,-1):A=A.replace(f"${E}",f"_col{E}")
	return A
def get_table_from_creation_query(query):
	A=DDLParser(query).run()
	if not A:return
	B=A[0].get('table_name')
	if B and not A[0].get('alter'):return B