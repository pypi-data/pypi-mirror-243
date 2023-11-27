from duckberg import *
from pyiceberg.expressions import EqualTo
from pyiceberg.catalog import Catalog, load_rest
import sqlfluff

MINIO_URI = "http://localhost:9000/"
MINIO_USER = "admin"
MINIO_PASSWORD = "password"

catalog_config: dict[str, str] = {
  "type": "rest",
  "uri": "http://localhost:8181/",
  "credentials": "admin:password",
  "s3.endpoint": MINIO_URI,
  "s3.access-key-id": MINIO_USER,
  "s3.secret-access-key": MINIO_PASSWORD
}

catalog_name = "warehouse"

db = DuckBerg(
     catalog_name=catalog_name,
     catalog_config=catalog_config)

tbls = db.get_tables()

query: str = 'SELECT * FROM nyc.taxis WHERE payment_type = 1 AND trip_distance > 40 ORDER BY tolls_amount DESC'

