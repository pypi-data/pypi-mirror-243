import gzip
import shutil
from hashlib import sha256
from pathlib import Path

import dill

# NOTE: pickleだと並列で動かした時にエラーが出るのでdillを使う
# import pickle


class KVS:
    def __init__(self, db_path="db"):
        self.db_path = Path(db_path)
        self.db_path.mkdir(exist_ok=True)

    def get_digest(self, __key):
        return sha256(bytes(__key, "utf8")).hexdigest()[:24]

    def flash(self, __key, datum):
        key = self.get_digest(__key)
        value = gzip.compress(dill.dumps(datum))
        with Path(self.db_path, f"{key}").open(mode="wb") as f:
            f.write(value)

    def is_exists(self, __key):
        key = self.get_digest(__key)
        if Path(self.db_path, f"{key}").exists():
            return True
        else:
            return False

    def get(self, __key):
        key = self.get_digest(__key)
        if self.is_exists(__key) is False:
            return None
        with Path(self.db_path, f"{key}").open(mode="rb") as f:
            value = f.read()
        datum = dill.loads(gzip.decompress(value))
        return datum

    def cleanup(self):
        shutil.rmtree(self.db_path, ignore_errors=True)
