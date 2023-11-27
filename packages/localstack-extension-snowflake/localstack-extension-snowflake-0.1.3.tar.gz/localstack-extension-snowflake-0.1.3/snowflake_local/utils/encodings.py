import base64,io,logging,struct
from hashlib import sha256
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from localstack.utils.strings import to_bytes
from pyarrow import parquet
LOG=logging.getLogger(__name__)
def decrypt_blob(blob,key,blob_path):B=struct.pack('q',0)+struct.pack('q',0);C=base64.b64decode(to_bytes(key));D=C+to_bytes(blob_path);E=sha256(D).digest();F=Cipher(algorithms.AES(E),modes.CTR(B));A=F.decryptor();G=A.update(blob)+A.finalize();return G
def get_parquet_from_blob(blob,key,blob_path):
	A=decrypt_blob(blob,key=key,blob_path=blob_path)
	for E in range(4):
		if A[-1]==0:A=A[:-1]
	try:B=io.BytesIO(A);C=parquet.read_table(B)
	except Exception as D:LOG.warning('Unable to parse parquet from decrypted data: %s... - %s',A[:300],D);raise
	return C.to_pylist()