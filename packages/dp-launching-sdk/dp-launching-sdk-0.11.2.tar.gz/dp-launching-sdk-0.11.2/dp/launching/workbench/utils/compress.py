import os
import zipfile

__all__ = ["zip_directory"]


def zip_directory(folder_path, zip_path):
    zipf = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), folder_path)
            zipf.write(os.path.join(root, file), rel_path)
    zipf.close()
