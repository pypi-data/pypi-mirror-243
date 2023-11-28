
from google.cloud import storage
from pathlib import Path

def download_folder(destination_dir_path,remote_bucket_name,remote_folder_path_relative_to_bucket,cache_files=True,keep_remote_relative_hierarchy=False):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(remote_bucket_name)
    reltaive_hierarchy_length = len(Path(remote_folder_path_relative_to_bucket).parts) -1
    blobs = bucket.list_blobs(prefix=remote_folder_path_relative_to_bucket)  # Get list of files
    for blob in blobs:
        if blob.name.endswith("/"):
            continue

        file_split = blob.name.split("/")
        file_name = file_split[-1]
        if keep_remote_relative_hierarchy:
            starting_index = 0
        
        else:
            starting_index = reltaive_hierarchy_length
        relative_dir = Path("/".join(file_split[starting_index:-1]))
        final_file_local_path = destination_dir_path/relative_dir/file_name
        
        if final_file_local_path.exists():
            if cache_files:
                continue
            else:
                pass

        (destination_dir_path/relative_dir).mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(final_file_local_path)