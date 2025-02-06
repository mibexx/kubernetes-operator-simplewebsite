# resources/configmap.py
from kubernetes import client
import re

class ConfigMapManager:
    def __init__(self, core_api_instance, namespace):
        self.core_api_instance = core_api_instance
        self.namespace = namespace

    def create(self, cr):
        site_name = cr['spec']['siteName']
        config_map_name = f"sw-{site_name}"
        
        # Check if the ConfigMap already exists
        try:
            self.core_api_instance.read_namespaced_config_map(name=config_map_name, namespace=self.namespace)
            print(f"ConfigMap '{config_map_name}' already exists. Skipping creation.")
            return
        except client.exceptions.ApiException as e:
            if e.status != 404:
                # Re-raise exception if it's not a 'Not Found' error
                raise

        # Validate filenames and log errors if invalid
        files = cr['spec']['files']
        data = {}
        for file in files:
            filename = file['filename']
            if not self.is_valid_key(filename):
                print(f"Skipping creation of ConfigMap '{config_map_name}' due to invalid filename: '{filename}'")
                return
            data[filename] = file['content']

        config_map = client.V1ConfigMap(
            api_version="v1",
            kind="ConfigMap",
            metadata=client.V1ObjectMeta(name=config_map_name, namespace=self.namespace),
            data=data
        )
        
        # Create the ConfigMap in Kubernetes
        self.core_api_instance.create_namespaced_config_map(namespace=self.namespace, body=config_map)
        print(f"ConfigMap '{config_map_name}' created.")

    def update(self, cr):
        site_name = cr['spec']['siteName']
        config_map_name = f"sw-{site_name}"

        # Delete the existing ConfigMap if it exists
        self.delete(cr)
        
        # Create the new ConfigMap
        self.create(cr)

    def delete(self, cr):
        site_name = cr['spec']['siteName']
        config_map_name = f"sw-{site_name}"

        # Check if the ConfigMap exists before attempting to delete
        try:
            self.core_api_instance.read_namespaced_config_map(name=config_map_name, namespace=self.namespace)
            # Delete the ConfigMap in Kubernetes
            self.core_api_instance.delete_namespaced_config_map(name=config_map_name, namespace=self.namespace)
            print(f"ConfigMap '{config_map_name}' deleted.")
        except client.exceptions.ApiException as e:
            if e.status != 404:
                # Re-raise exception if it's not a 'Not Found' error
                raise
            print(f"ConfigMap '{config_map_name}' does not exist, skipping delete.")

    def is_valid_key(self, key):
        # Check if the key is valid according to Kubernetes naming rules
        return bool(re.match(r'^[A-Za-z0-9_.-]+$', key))