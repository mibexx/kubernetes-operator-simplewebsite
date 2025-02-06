# resources/deployment.py
from kubernetes import client

class DeploymentManager:
    def __init__(self, apps_api_instance, namespace):
        self.apps_api_instance = apps_api_instance
        self.namespace = namespace

    def create(self, cr):
        site_name = cr['spec']['siteName']
        deployment_name = f"sw-{site_name}"
        config_map_name = f"sw-{site_name}"

        # Check if the Deployment already exists
        try:
            self.apps_api_instance.read_namespaced_deployment(name=deployment_name, namespace=self.namespace)
            print(f"Deployment '{deployment_name}' already exists. Skipping creation.")
            return
        except client.rest.ApiException as e:
            if e.status != 404:
                raise

        # Define the container and the deployment
        container = client.V1Container(
            name=deployment_name,
            image="nginx:alpine",
            ports=[client.V1ContainerPort(container_port=80)],
            volume_mounts=[client.V1VolumeMount(
                name="config-volume",
                mount_path="/usr/share/nginx/html/"
            )],
            command=["nginx", "-g", "daemon off;"]
        )

        volume = client.V1Volume(
            name="config-volume",
            config_map=client.V1ObjectReference(name=config_map_name)
        )

        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=deployment_name, namespace=self.namespace),
            spec=client.V1DeploymentSpec(
                replicas=1,
                selector=client.V1LabelSelector(
                    match_labels={"app": deployment_name}
                ),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(labels={"app": deployment_name}),
                    spec=client.V1PodSpec(containers=[container], volumes=[volume])
                )
            )
        )

        # Create the Deployment in Kubernetes
        self.apps_api_instance.create_namespaced_deployment(namespace=self.namespace, body=deployment)
        print(f"Deployment '{deployment_name}' created.")

    def update(self, cr):
        self.delete(cr)
        self.create(cr)

    def delete(self, cr):
        site_name = cr['spec']['siteName']
        deployment_name = f"sw-{site_name}"

        # Check if the Deployment exists before attempting to delete
        try:
            self.apps_api_instance.read_namespaced_deployment(name=deployment_name, namespace=self.namespace)
            # Delete the Deployment in Kubernetes
            self.apps_api_instance.delete_namespaced_deployment(name=deployment_name, namespace=self.namespace)
            print(f"Deployment '{deployment_name}' deleted.")
        except client.exceptions.NotFound:
            print(f"Deployment '{deployment_name}' does not exist, skipping delete.")