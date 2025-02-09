# resources/service.py
from kubernetes import client

class ServiceManager:
    def __init__(self, core_api_instance, namespace):
        self.core_api_instance = core_api_instance
        self.namespace = namespace
        self.default_port = 80

    def create(self, cr):
        site_name = cr['spec']['siteName']
        port = cr['spec'].get('port', self.default_port)
        service_name = f"sw-{site_name}"

        # Check if the Service already exists
        try:
            self.core_api_instance.read_namespaced_service(name=service_name, namespace=self.namespace)
            print(f"Service '{service_name}' already exists. Skipping creation.")
            return
        except client.rest.ApiException as e:
            if e.status != 404:
                raise

        service = client.V1Service(
            api_version="v1",
            kind="Service",
            metadata=client.V1ObjectMeta(name=service_name, namespace=self.namespace),
            spec=client.V1ServiceSpec(
                selector={"app": service_name},
                ports=[client.V1ServicePort(port=port, target_port=port)],
                type="ClusterIP"
            )
        )

        # Create the Service in Kubernetes
        self.core_api_instance.create_namespaced_service(namespace=self.namespace, body=service)
        print(f"Service '{service_name}' created.")

    def update(self, cr):
        self.delete(cr)
        self.create(cr)

    def delete(self, cr):
        site_name = cr['spec']['siteName']
        service_name = f"sw-{site_name}"

        # Check if the Service exists before attempting to delete
        try:
            self.core_api_instance.read_namespaced_service(name=service_name, namespace=self.namespace)
            # Delete the Service in Kubernetes
            self.core_api_instance.delete_namespaced_service(name=service_name, namespace=self.namespace)
            print(f"Service '{service_name}' deleted.")
        except client.exceptions.NotFound:
            print(f"Service '{service_name}' does not exist, skipping delete.")