import os


class UploadProgress:
    def __init__(self, file_path):
        self.total_bytes = os.path.getsize(file_path)
        self.uploaded_bytes = 0

    def callback(self, result):
        self.uploaded_bytes += result['importedFileSizeOfBytes']
        print(f"Progress: {self.get_progress()}%")

    def get_progress(self):
        if not self.uploaded_bytes:
            return 0
        return round(self.uploaded_bytes / self.total_bytes, 2) * 100
