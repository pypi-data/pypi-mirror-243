import os
from google.cloud import secretmanager
import google.auth

class GcpSecretManager:
    """
    Instantiate a GCP Secret Manager object.

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
        self.credentials, self.project = google.auth.load_credentials_from_file(credential_file)

    def list_secret(self, project_id):
        """
        List all secrets in a project.

        Args:
            project_id (str): Project ID

        Returns:
            secret_list (list): List of secrets
        """
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        parent = f"projects/{project_id}"
        secrets = client.list_secrets(request={"parent": parent})
        results = []
        secret_list = []
        for secret in secrets:
            secret_list.append(secret.name)
        return secret_list
    
    def get_secret(self, project_id, secret_id):
        """
        Get a secret from a project.

        Args:
            project_id (str): Project ID
            secret_id (str): Secret ID

        Returns:
            result (str): Secret value
        """
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        result = response.payload.data.decode("UTF-8")
        return result
    
    def get_secret_version(self, project_id, secret_id, secret_version):
        """
        Get a secret from a project.

        Args:
            project_id (str): Project ID
            secret_id (str): Secret ID
            secret_version (str): Secret version

        Returns:
            result (str): Secret value
        """
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{secret_version}"
        response = client.access_secret_version(request={"name": name})
        result = response.payload.data.decode("UTF-8")
        return result
    
    def get_secret_versions(self, project_id, secret_id):
        """
        Get all secret versions from a project.

        Args:
            project_id (str): Project ID
            secret_id (str): Secret ID

        Returns:
            secret_list (list): Secret version list
        """
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        name = f"projects/{project_id}/secrets/{secret_id}"
        response = client.list_secret_versions(request={"parent": name})
        result = []
        version_list = []
        for version in response:
            version_list.append(version.name)
        return version_list
    
    def get_secret_version_create_time(self, project_id, secret_id, secret_version):
        """
        Get secret version create time from a project.

        Args:
            project_id (str): Project ID
            secret_id (str): Secret ID
            secret_version (str): Secret version

        Returns:
            result (str): Secret version create time
        """
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{secret_version}"
        response = client.access_secret_version(request={"name": name})
        result = response.create_time
        return result
    
    def get_secret_version_state(self, project_id, secret_id, secret_version):
        """
        Get secret version state from a project.

        Args:
            project_id (str): Project ID
            secret_id (str): Secret ID
            secret_version (str): Secret version

        Returns:
            result (str): Secret version state
        """
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{secret_version}"
        response = client.access_secret_version(request={"name": name})
        result = response.state
        return result
    
    def get_secret_version_destroy_time(self, project_id, secret_id, secret_version):
        """
        Get secret version destroy time from a project.

        Args:
            project_id (str): Project ID
            secret_id (str): Secret ID
            secret_version (str): Secret version

        Returns:
            result (str): Secret version destroy time
        """
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{secret_version}"
        response = client.access_secret_version(request={"name": name})
        result = response.destroy_time
        return result
    
    def create_secret(self, project_id, secret_id):
        """
        Create a secret in a project.

        Args:
            project_id (str): Project ID
            secret_id (str): Secret ID

        Returns:
            result (str): Secret name
        """
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        parent = f"projects/{project_id}"
        secret = {"replication": {"automatic": {}}}
        response = client.create_secret(request={"parent": parent, "secret_id": secret_id, "secret": secret})
        result = response.name
        return result
    
    def add_secret_version(self, project_id, secret_id, payload):
        """
        Add a secret version in a project.

        Args:
            project_id (str): Project ID
            secret_id (str): Secret ID
            payload (str): Secret value

        Returns:
            result (str): Secret version name
        """
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        parent = f"projects/{project_id}/secrets/{secret_id}"
        response = client.add_secret_version(request={"parent": parent, "payload": {"data": payload.encode("UTF-8")}})
        result = response.name
        return result
    
    def delete_secret(self, project_id, secret_id):
        """
        Delete a secret from a project.

        Args:
            project_id (str): Project ID
            secret_id (str): Secret ID

        Returns:
            result (str): It returns 'OK' when successful
        """
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        name = f"projects/{project_id}/secrets/{secret_id}"
        client.delete_secret(request={"name": name})
        result = 'OK'
        return result
    
    def destroy_secret_version(self, project_id, secret_id, secret_version):
        """
        Destroy a secret version from a project.

        Args:
            project_id (str): Project ID
            secret_id (str): Secret ID
            secret_version (str): Secret version

        Returns:
            result (str): It returns 'OK' when successful
        """
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{secret_version}"
        client.destroy_secret_version(request={"name": name})
        result = 'OK'
        return result
    
    def disable_secret_version(self, project_id, secret_id, secret_version):
        """
        Disable a secret version from a project.

        Args:
            project_id (str): Project ID
            secret_id (str): Secret ID
            secret_version (str): Secret version

        Returns:
            result (str): It returns 'OK' when successful
        """
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{secret_version}"
        client.disable_secret_version(request={"name": name})
        result = 'OK'
        return result
    
    def enable_secret_version(self, project_id, secret_id, secret_version):
        """
        Enable a secret version from a project.

        Args:
            project_id (str): Project ID
            secret_id (str): Secret ID
            secret_version (str): Secret version

        Returns:
            result (str): It returns 'OK' when successful
        """
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{secret_version}"
        client.enable_secret_version(request={"name": name})
        result = 'OK'
        return result
    
    def get_secret_policy(self, project_id, secret_id):
        """
        Get a secret policy from a project.

        Args:
            project_id (str): Project ID
            secret_id (str): Secret ID

        Returns:
            result (str): Secret policy
        """
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        name = f"projects/{project_id}/secrets/{secret_id}"
        response = client.get_iam_policy(request={"resource": name})
        result = response
        return result

    def set_secret_policy(self, project_id, secret_id, member, role):
        """
        Set a secret policy from a project.

        Args:
            project_id (str): Project ID
            secret_id (str): Secret ID
            member (str): Member
            role (str): Role

        Returns:
            result (str): It returns 'OK' when successful
        """
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        name = f"projects/{project_id}/secrets/{secret_id}"
        policy = {"bindings": [{"role": role, "members": [member]}]}
        response = client.set_iam_policy(request={"resource": name, "policy": policy})
        result = 'OK'
        return result
    
    def test_iam_permissions(self, project_id, secret_id, permissions):
        """
        Test a secret policy from a project.

        Args:
            project_id (str): Project ID
            secret_id (str): Secret ID
            permissions (list): Permissions

        Returns:
            result (str): It returns 'OK' when successful
        """
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        name = f"projects/{project_id}/secrets/{secret_id}"
        response = client.test_iam_permissions(request={"resource": name, "permissions": permissions})
        result = response
        return result
    
    def add_secret_version_from_file(self, project_id, secret_id, file_path):
        """
        Add a secret version from a file in a project.

        Args:
            project_id (str): Project ID
            secret_id (str): Secret ID
            file_path (str): File path

        Returns:
            result (str): Secret version name
        """
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        parent = f"projects/{project_id}/secrets/{secret_id}"
        with open(file_path, "rb") as f:
            payload = {"data": f.read()}
        response = client.add_secret_version(request={"parent": parent, "payload": payload})
        result = response.name
        return result
    
    def add_secret_version_from_string(self, project_id, secret_id, payload):
        """
        Add a secret version from a string in a project.

        Args:
            project_id (str): Project ID
            secret_id (str): Secret ID
            payload (str): Secret value

        Returns:
            result (str): Secret version name
        """
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        parent = f"projects/{project_id}/secrets/{secret_id}"
        response = client.add_secret_version(request={"parent": parent, "payload": {"data": payload.encode("UTF-8")}})
        result = response.name
        return result
    
    def get_secret_version_to_file(self, project_id, secret_id, secret_version, file_path):
        """
        Get a secret version in a project and store it in a file.
        
        Args:
            project_id (str): Project ID
            secret_id (str): Secret ID
            secret_version (str): Secret version
            file_path (str): File path
            
        Returns:
            result (str): It returns 'OK' when successful
        """
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{secret_version}"
        response = client.access_secret_version(request={"name": name})
        with open(file_path, "wb") as f:
            f.write(response.payload.data)
        result = 'OK'
        return result
    
    
