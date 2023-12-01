import json
from localstack.utils.json import extract_jsonpath
from localstack.utils.numbers import is_number
from localstack.utils.strings import to_str
def load_data(file_ref,file_format):
	from snowflake_local.files.storage import FILE_STORAGE as D,FileRef as E;F=E.parse(file_ref);A=D.load_file(F);A=json.loads(to_str(A));G=A if isinstance(A,list)else[A];B=[]
	for C in G:
		if isinstance(C,dict):B.append({'_col1':json.dumps(C)})
		else:B.append(C)
	return B
def object_construct(*A,**E):
	B={}
	for C in range(0,len(A),2):D=A[C+1];B[A[C]]=json.loads(D)
	return json.dumps(B)
def to_json_str(obj):return json.dumps(obj)
def get_path(obj,path):
	C=obj;B=path
	if not B.startswith('.'):B=f".{B}"
	if not B.startswith('$'):B=f"${B}"
	if C is not None and not isinstance(C,(list,dict)):C=json.loads(C)
	A=extract_jsonpath(C,B)
	if A==[]:return''
	if is_number(A)and not isinstance(A,bool)and int(A)==A:A=int(A)
	A=json.dumps(A);return A
def to_variant(obj):return obj
def parse_json(obj):json.loads(obj);return obj
def to_char(obj):return str(obj)
def cancel_all_queries(session):return'canceled'