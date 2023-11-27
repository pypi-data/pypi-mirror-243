import csv,gzip,io,os.path,re
from localstack.aws.connect import connect_to
from localstack.utils.strings import to_str
from snowflake_local.engine.queries import insert_rows_into_table
from snowflake_local.files.staging import get_stage_s3_location
from snowflake_local.files.storage import FileRef
from snowflake_local.server.models import QueryResponse
class FileParseOptions:parse_header=False
def handle_put_file_query(query,result):
	A=result;D=re.match('^PUT\\s+(\\S+)\\s+(\\S+)',query,flags=re.IGNORECASE);B=D.group(1);C=D.group(2);B=B.removeprefix('file://')
	if'/'not in C:C=f"{C}/{os.path.basename(B)}"
	E=FileRef.parse(C);A.data.command='UPLOAD';A.data.src_locations=[B];A.data.stageInfo=get_stage_s3_location(E);A.data.sourceCompression='none';return A
def handle_copy_into_query(query,result):
	A=query;B=re.match('^COPY\\s+INTO\\s+(\\S+)\\s+.*FROM\\s+(\\S+)',A,flags=re.I);E=B.group(1);F=B.group(2);C=FileParseOptions();C.parse_header=bool(re.search('PARSE_HEADER\\s*=\\s*TRUE',A,flags=re.I));G=FileRef.parse(F);H=get_stage_s3_location(G);D,L,I=H['location'].partition('/');J=connect_to().s3
	for K in J.list_objects(Bucket=D,Prefix=I)['Contents']:_copy_file_into_table(E,D,s3_key=K['Key'],parse_opts=C)
	return result
def _copy_file_into_table(table_name,s3_bucket,s3_key,parse_opts):
	B=connect_to().s3;C=B.get_object(Bucket=s3_bucket,Key=s3_key);A=C['Body'].read()
	try:A=gzip.decompress(A)
	except gzip.BadGzipFile:pass
	D=_parse_tabular_data(to_str(A),parse_opts=parse_opts);insert_rows_into_table(table_name,D)
def _parse_tabular_data(content,parse_opts):
	A=content;A=to_str(A);B=csv.reader(io.StringIO(A))
	if not parse_opts.parse_header:return list(B)
	D=next(B,None);C=[]
	for E in B:C.append({A:B for(A,B)in zip(D,E)})
	return C