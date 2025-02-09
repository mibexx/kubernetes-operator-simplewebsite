# resources/ingress.py
from kubernetes import client

class IngressManager:
    def __init__(self, networking_api_instance, namespace):
        self.networking_api_instance = networking_api_instance
        self.namespace = namespace
        self.default_port = 80

    def create(self, cr):
        site_name = cr['spec']['siteName']
        domain = cr['spec']['domain']
        port = cr['spec'].get('port', self.default_port)
        ingress_name = f"sw-{site_name}"

        # Check if the Ingress already exists
        try:
            self.networking_api_instance.read_namespaced_ingress(name=ingress_name, namespace=self.namespace)
            print(f"Ingress '{ingress_name}' already exists. Skipping creation.")
            return
        except client.rest.ApiException as e:
            if e.status != 404:
                raise

        # Define the Ingress resource using the correct API version
        ingress = client.V1Ingress(
            api_version="networking.k8s.io/v1",
            kind="Ingress",
            metadata=client.V1ObjectMeta(
                name=ingress_name,
                namespace=self.namespace,
                annotations={
                    "cert-manager.io/cluster-issuer": "letsencrypt-prod"
                }
            ),
            spec=client.V1IngressSpec(
                ingress_class_name="nginx",
                rules=[
                    client.V1IngressRule(
                        host=domain,
                        http=client.V1HTTPIngressRuleValue(
                            paths=[
                                client.V1HTTPIngressPath(
                                    path="/",
                                    path_type="Prefix",
                                    backend=client.V1IngressBackend(
                                        service=client.V1IngressServiceBackend(
                                            name=f"sw-{site_name}",
                                            port=client.V1ServiceBackendPort(number=port)
                                        )
                                    )
                                )
                            ]
                        )
                    )
                ],
                tls=[
                    client.V1IngressTLS(
                        hosts=[domain],
                        secret_name=f"tls-{site_name}"
                    )
                ]
            )
        )

        # Create the Ingress in Kubernetes
        self.networking_api_instance.create_namespaced_ingress(namespace=self.namespace, body=ingress)
        print(f"Ingress '{ingress_name}' created.")

    def update(self, cr):
        # Delete the existing Ingress if it exists
        self.delete(cr)
        
        # Create the new Ingress
        self.create(cr)

    def delete(self, cr):
        site_name = cr['spec']['siteName']
        ingress_name = f"sw-{site_name}"

        # Check if the Ingress exists before attempting to delete
        try:
            self.networking_api_instance.read_namespaced_ingress(name=ingress_name, namespace=self.namespace)
            # Delete the Ingress in Kubernetes
            self.networking_api_instance.delete_namespaced_ingress(name=ingress_name, namespace=self.namespace)
            print(f"Ingress '{ingress_name}' deleted.")
        except client.exceptions.NotFound:
            print(f"Ingress '{ingress_name}' does not exist, skipping delete.")