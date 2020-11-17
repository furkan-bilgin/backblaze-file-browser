from b2sdk.v1 import *
import os


class BackblazeFileUploader():
    def __init__(self):
        info = InMemoryAccountInfo()
        self.b2_api = B2Api(info)
        
        self.b2_api.authorize_account("production", os.environ["backblaze_key_id"], os.environ["backblaze_app_key"])
        self.bucket = self.b2_api.get_bucket_by_name(os.environ["backblaze_bucket_name"])

        super().__init__()
        

    def upload_file(self, filename, blob):
        file_info = self.bucket.upload_bytes(blob, filename)
        return file_info.id_    


    def delete_file(self, file_id, filename):
        try:
            self.b2_api.delete_file_version(file_id, filename)
            return True
        except:
            return False