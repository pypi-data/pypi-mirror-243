_A='test'
import atexit,logging,re,time
from localstack.utils.net import get_free_tcp_port,wait_for_port_open
from localstack_ext.services.rds.engine_postgres import get_type_name
from localstack_ext.utils.postgresql import Postgresql
from snowflake_local.engine.db_engine import DBEngine
from snowflake_local.engine.models import Query,QueryResult,TableColumn
from snowflake_local.engine.transforms import QueryTransformsPostgres
LOG=logging.getLogger(__name__)
PG_VARIANT_TYPE='JSONB'
PG_VARIANT_COMPATIBLE_TYPES='JSONB','FLOAT','BIGINT','BOOLEAN','TEXT'
class State:server=None
class DBEnginePostgres(DBEngine):
	def execute_query(F,query):
		A=_execute_query(query)
		if isinstance(A,list):return QueryResult(rows=A)
		if not A._context.columns:return QueryResult()
		B=list(A);B=[tuple(A)for A in B];D=QueryResult(rows=B)
		for C in A._context.columns:E=TableColumn(name=C['name'],type_name=get_type_name(C['type_oid']),type_size=C['type_size']);D.columns.append(E)
		return D
	def prepare_query(B,query):A=QueryTransformsPostgres();return A.apply(query)
def _execute_query(query):
	A=query;C=_start_postgres();LOG.debug('Running query: %s - %s',A.query,A.params)
	try:D=A.params or[];return C.run_query(A.query,*D,database=A.database)
	except Exception as B:
		if'already exists'in str(B):
			if'database'in str(B)or'schema'in str(B):return[]
			if'relation'in str(B):E=re.match('.*relation \\"(.+)\\" already exists',str(B)).group(1);C.run_query(f"DROP TABLE {E}",*A.params);return C.run_query(A.query,*A.params)
		raise
def _start_postgres(user=_A,password=_A,database=_A):
	if not State.server:
		A=get_free_tcp_port();State.server=Postgresql(port=A,user=user,password=password,database=database,boot_timeout=30,include_python_venv_libs=True);time.sleep(1)
		try:B=20;wait_for_port_open(A,retries=B,sleep_time=.8)
		except Exception:raise Exception('Unable to start up Postgres process (health check failed after 10 secs)')
		_define_util_functions(State.server)
		def C():State.server.terminate()
		atexit.register(C)
	return State.server
def _define_util_functions(server):
	B=server;B.run_query('CREATE EXTENSION IF NOT EXISTS plpython3u');A='\n    CREATE OR REPLACE FUNCTION load_data (\n       file_ref text,\n       file_format text\n    ) RETURNS SETOF RECORD\n    LANGUAGE plpython3u IMMUTABLE\n    AS $$\n        from snowflake_local.engine.extension_functions import load_data\n        return load_data(file_ref, file_format)\n    $$;\n    ';B.run_query(A)
	for D in range(10):E=', '.join([f"k{A} TEXT, v{A} TEXT"for A in range(D)]);F=', '.join([f"k{A}, v{A}"for A in range(D)]);A=f"""
        CREATE OR REPLACE FUNCTION object_construct ({E}) RETURNS JSONB
        LANGUAGE plpython3u IMMUTABLE
        AS $$
            from snowflake_local.engine.extension_functions import object_construct
            return object_construct({F})
            $$;
        """;B.run_query(A)
	for C in PG_VARIANT_COMPATIBLE_TYPES:A=f"""
        CREATE OR REPLACE FUNCTION to_variant (obj {C}) RETURNS {PG_VARIANT_TYPE}
        LANGUAGE plpython3u IMMUTABLE
        AS $$
            from snowflake_local.engine.extension_functions import to_variant
            return to_variant(obj)
        $$;
        """;B.run_query(A)
	for C in PG_VARIANT_COMPATIBLE_TYPES:A=f"""
        CREATE OR REPLACE FUNCTION to_json_str (obj {C}) RETURNS TEXT
        LANGUAGE plpython3u IMMUTABLE
        AS $$
            from snowflake_local.engine.extension_functions import to_json_str
            return to_json_str(obj)
        $$;
        """;B.run_query(A)
	A=f"""
    CREATE OR REPLACE FUNCTION get_path (obj {PG_VARIANT_TYPE}, path TEXT) RETURNS TEXT
    LANGUAGE plpython3u IMMUTABLE
    AS $$
        from snowflake_local.engine.extension_functions import get_path
        return get_path(obj, path)
    $$;
    """;B.run_query(A);A=f"""
    CREATE OR REPLACE FUNCTION parse_json (obj TEXT) RETURNS {PG_VARIANT_TYPE}
    LANGUAGE plpython3u IMMUTABLE
    AS $$
        from snowflake_local.engine.extension_functions import parse_json
        return parse_json(obj)
    $$;
    """;B.run_query(A)
	for C in PG_VARIANT_COMPATIBLE_TYPES:A=f"""
        CREATE OR REPLACE FUNCTION to_char (obj {C}) RETURNS TEXT
        LANGUAGE plpython3u IMMUTABLE
        AS $$
            from snowflake_local.engine.extension_functions import to_char
            return to_char(obj)
        $$;
        """;B.run_query(A)
	A='\n    CREATE OR REPLACE FUNCTION "system$cancel_all_queries" (session TEXT) RETURNS TEXT\n    LANGUAGE plpython3u IMMUTABLE\n    AS $$\n        from snowflake_local.engine.extension_functions import cancel_all_queries\n        return cancel_all_queries(session)\n    $$;\n    ';B.run_query(A)