import os
from google.cloud import storage
from datetime import datetime, UTC
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

class BackupController:
    def __init__(self, key, project, bucket, logs, medias):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key
        self.storage_client = storage.Client(project)
        self.bucket = self.storage_client.bucket(bucket)
        self.logs = os.path.join(BASE_DIR, logs)
        self.medias = os.path.join(BASE_DIR, medias)

    def _upload_directory(self, folder_path, prefix):
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                local_path = os.path.join(root, filename)

                relative_path = os.path.relpath(local_path, folder_path)
                blob_path = os.path.join(prefix, relative_path).replace("\\", "/")

                blob = self.bucket.blob(blob_path)

                local_mtime = os.path.getmtime(local_path)
                local_updated = datetime.fromtimestamp(local_mtime, UTC)

                if blob.exists():
                    blob.reload()
                    remote_updated = blob.updated

                    if local_updated <= remote_updated:
                        continue

                blob.upload_from_filename(local_path)

    def upload(self):
        self._upload_directory(self.logs, "logs")
        self._upload_directory(self.medias, "medias")
