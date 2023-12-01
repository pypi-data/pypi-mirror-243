import base64,pyarrow,pyarrow.json
from localstack.utils.strings import to_str
from snowflake_local.server.models import QueryResponse
def to_pyarrow_table_bytes_b64(result):
	H='16777216';B=result;I={'byteLength':H,'charLength':H,'logicalType':'VARIANT','precision':'38','scale':'0','finalType':'T'};C=[];D=[A['name'].replace('_col','$')for A in B.data.rowtype]
	for J in range(len(D)):K=[A[J]for A in B.data.rowset];C.append(pyarrow.array(K))
	E=pyarrow.record_batch(C,names=D);F=pyarrow.BufferOutputStream();A=E.schema
	for G in range(len(A)):L=A.field(G);M=L.with_metadata(I);A=A.set(G,M)
	with pyarrow.ipc.new_stream(F,A)as N:N.write_batch(E)
	B=base64.b64encode(F.getvalue());return to_str(B)