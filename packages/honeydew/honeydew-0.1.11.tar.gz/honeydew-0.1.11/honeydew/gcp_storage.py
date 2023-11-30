import os
from google.cloud import storage
class GcpCloudStorage:
    """
    Instantiate a GCS connector.
    Args:
        credential_file (str): Credential json file
        proxy (str): Proxy address
    """
    def __init__(self, credential_file, proxy=''):
        self.credential_file = credential_file
        self.proxy = proxy
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_file
        if proxy != '':
            os.environ['HTTP_PROXY'] = proxy
            os.environ['HTTPS_PROXY'] = proxy

    def download_blob(self, project_id, bucket_id, source_blob_path, destination_path):
        """
        Download a single object from Google Cloud Storage (GCS).

        Args:
            project_id (str): Project ID
            bucket_id (str): Bucket ID
            source_blob_path (str): The path of source object. Example: 'gcs-directory/my-filename.txt'
            destination_path (str): Local destination path. Example: '/my-directory/my-filename.txt'

        Returns:
            result (result): Iterator of row data. Reference: https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.job.QueryJob.html?highlight=job%20result#google.cloud.bigquery.job.QueryJob.result
        """
        gcs_client = storage.Client(project=project_id)
        bucket = gcs_client.bucket(bucket_id)
        blob = bucket.blob(source_blob_path)
        blob.download_to_filename(destination_path)
        results = 'OK'
        return results    
    
    def download_many_blobs(self, project_id, bucket_id, blob_prefix, destination_dir_path, printout=True):
        """
        Download multiple objects which have same prefix pattern from Google Cloud Storage (GCS).

        Args:
            project_id (str): Project ID
            bucket_id (str): Bucket ID
            blob_prefix (str): The blob prefix pattern that wil be downloaded. Example: 'gcs-directory/tickets-20220101-'
            destination_dir_path (str): Local destination directory path. Example: '/my-directory'
            printout (boolean): File name will be displayed if this value is true. Default: True
        
        Returns:
            result (str): It returns 'OK' when successful            
        """

        delimiter='/'
        storage_client = storage.Client(project_id)
        bucket=storage_client.get_bucket(bucket_id)
        # List blobs iterate in folder 
        blobs=bucket.list_blobs(prefix=blob_prefix, delimiter=delimiter) # Excluding folder inside bucket
        for blob in blobs:
            if printout == True:
                print(blob.name)
            filename_raw = blob.name.split('/')
            filename = filename_raw[len(filename_raw)-1]
            destination_uri = '{}{}'.format(destination_dir_path, filename) 
            blob.download_to_filename(destination_uri)
        results = 'OK'   
        return results
    
    def upload_blob(self, project_id, bucket_id, local_file, destination_blob):
        """
        Upload a single object from Google Cloud Storage (GCS).

        Args:
            project_id (str): Project ID
            bucket_id (str): Bucket ID
            local_file (str): Local file as source. Example: '/local-directory/my-filename.txt'
            destination_blob (str): Destination blob in GCS bucket. Example: 'gcs-directory/my-filename.txt'
        
        Returns:
            result (str): It returns 'OK' when successful
        """
        gcs_client = storage.Client(project=project_id)
        bucket = gcs_client.bucket(bucket_id)
        blob = bucket.blob(destination_blob)
        blob.upload_from_filename(local_file)
        results = 'OK'
        return results          
    
    def upload_many_blobs(self, project_id, bucket_id, local_dir, destination_dir):
        """
        Upload multiple objects to Google Cloud Storage (GCS).

        Args:
            project_id (str): Project ID
            bucket_id (str): Bucket ID
            local_dir (str): Local directory as source. Example: '/local-directory'
            destination_dir (str): Destination directory in GCS bucket. Example: 'gcs-directory'
        
        Returns:
            result (str): It returns 'OK' when successful
        """
        gcs_client = storage.Client(project=project_id)
        bucket = gcs_client.bucket(bucket_id)
        for filename in os.listdir(local_dir):
            blob = bucket.blob(f'{destination_dir}/{filename}')
            blob.upload_from_filename(f'{local_dir}/{filename}')
        results = 'OK'
        return results

    def delete_blob(self, project_id, bucket_id, blob_name):
        """
        Delete a single object from Google Cloud Storage (GCS).

        Args:
            project_id (str): Project ID
            bucket_id (str): Bucket ID
            blob_name (str): Blob name. Example: 'gcs-directory/my-filename.txt'
        
        Returns:
            result (str): It returns 'OK' when successful
        """
        gcs_client = storage.Client(project=project_id)
        bucket = gcs_client.bucket(bucket_id)
        blob = bucket.blob(blob_name)
        blob.delete()
        results = 'OK'
        return results
    
    def delete_many_blobs(self, project_id, bucket_id, blob_prefix):
        """
        Delete multiple objects from Google Cloud Storage (GCS).

        Args:
            project_id (str): Project ID
            bucket_id (str): Bucket ID
            blob_prefix (str): Blob prefix. Example: 'gcs-directory/my-filename.txt'
        
        Returns:
            result (str): It returns 'OK' when successful
        """
        delimiter='/'
        storage_client = storage.Client(project_id)
        bucket=storage_client.get_bucket(bucket_id)
        # List blobs iterate in folder 
        blobs=bucket.list_blobs(prefix=blob_prefix, delimiter=delimiter)
        for blob in blobs:
            blob.delete()
        results = 'OK'
        return results
    
    def list_blobs(self, project_id, bucket_id, blob_prefix):
        """
        List objects from Google Cloud Storage (GCS).

        Args:
            project_id (str): Project ID
            bucket_id (str): Bucket ID
            blob_prefix (str): Blob prefix. Example: 'gcs-directory/my-filename.txt'
        
        Returns:
            blob_list (list): Blob list
        """
        delimiter='/'
        storage_client = storage.Client(project_id)
        bucket=storage_client.get_bucket(bucket_id)
        # List blobs iterate in folder 
        blobs=bucket.list_blobs(prefix=blob_prefix, delimiter=delimiter)
        blob_list = []
        for blob in blobs:
            blob_list.append(blob.name)
        results = 'OK'
        return blob_list
    
    def copy_blob_between_buckets(self, project_id, source_bucket_id, destination_bucket_id, blob_name):
        """
        Copy a single object between buckets in Google Cloud Storage (GCS).

        Args:
            project_id (str): Project ID
            source_bucket_id (str): Source bucket ID
            destination_bucket_id (str): Destination bucket ID
            blob_name (str): Blob name. Example: 'gcs-directory/my-filename.txt'
        
        Returns:
            result (str): It returns 'OK' when successful
        """
        gcs_client = storage.Client(project=project_id)
        source_bucket = gcs_client.bucket(source_bucket_id)
        destination_bucket = gcs_client.bucket(destination_bucket_id)
        blob = source_bucket.blob(blob_name)
        new_blob = source_bucket.copy_blob(blob, destination_bucket, blob_name)
        results = 'OK'
        return results
    
    def copy_many_blobs_between_buckets(self, project_id, source_bucket_id, destination_bucket_id, blob_prefix):
        """
        Copy multiple objects between buckets in Google Cloud Storage (GCS).
        
        Args:
            project_id (str): Project ID
            source_bucket_id (str): Source bucket ID
            destination_bucket_id (str): Destination bucket ID
            blob_prefix (str): Blob prefix. Example: 'gcs-directory/my-filename.txt'
        
        Returns:
            result (str): It returns 'OK' when successful
        """
        delimiter='/'
        storage_client = storage.Client(project_id)
        source_bucket = storage_client.bucket(source_bucket_id)
        destination_bucket = storage_client.bucket(destination_bucket_id)
        # List blobs iterate in folder 
        blobs=source_bucket.list_blobs(prefix=blob_prefix, delimiter=delimiter)
        for blob in blobs:
            new_blob = source_bucket.copy_blob(blob, destination_bucket, blob.name)
        results = 'OK'
        return results