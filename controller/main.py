# main.py
import sys
from kubernetes import client, config, watch
from resources.deployment import DeploymentManager
from resources.configmap import ConfigMapManager
from resources.service import ServiceManager
from resources.ingress import IngressManager

def main():
    config.load_incluster_config()
    namespace = open("/var/run/secrets/kubernetes.io/serviceaccount/namespace").read().strip()
    
    api_instance = client.CustomObjectsApi()
    apps_api_instance = client.AppsV1Api()
    core_api_instance = client.CoreV1Api()
    batch_api_instance = client.BatchV1Api()
    networking_api_instance = client.NetworkingV1Api()
    
    # Create instances of managers
    config_map_manager = ConfigMapManager(core_api_instance, namespace)
    deployment_manager = DeploymentManager(apps_api_instance, namespace)
    service_manager = ServiceManager(core_api_instance, namespace)
    ingress_manager = IngressManager(networking_api_instance, namespace)

    print(f"Watching for SimpleWebsite resources in namespace {namespace}...")
    sys.stdout.flush()
    
    w = watch.Watch()
    for event in w.stream(api_instance.list_namespaced_custom_object,
                          group="mbx360.de",
                          version="v1",
                          namespace=namespace,
                          plural="simplewebsites"):
        handle_event(event, config_map_manager, deployment_manager, service_manager, ingress_manager)

def handle_event(event, config_map_manager, deployment_manager, service_manager, ingress_manager):
    event_type = event['type']
    cr = event['object']
    name = cr['metadata']['name']
    if event_type == "ADDED":
        print(f"SimpleWebsite resource '{name}' created...")
        sys.stdout.flush()
        create_simple_website(cr, config_map_manager, deployment_manager, service_manager, ingress_manager)
    elif event_type == "MODIFIED":
        print(f"SimpleWebsite resource '{name}' updated...")
        sys.stdout.flush()
        update_simple_website(cr, config_map_manager, deployment_manager, service_manager, ingress_manager)
    elif event_type == "DELETED":
        print(f"SimpleWebsite resource '{name}' deleted...")
        sys.stdout.flush()
        delete_simple_website(cr, config_map_manager, deployment_manager, service_manager, ingress_manager)

    sys.stdout.flush()

def create_simple_website(cr, config_map_manager, deployment_manager, service_manager, ingress_manager):
    config_map_manager.create(cr)
    deployment_manager.create(cr)
    service_manager.create(cr)
    ingress_manager.create(cr)

def update_simple_website(cr, config_map_manager, deployment_manager, service_manager, ingress_manager):
    config_map_manager.update(cr)
    deployment_manager.update(cr)
    service_manager.update(cr)
    ingress_manager.update(cr)

def delete_simple_website(cr, config_map_manager, deployment_manager, service_manager, ingress_manager):
    ingress_manager.delete(cr)
    service_manager.delete(cr)
    deployment_manager.delete(cr)
    config_map_manager.delete(cr)

if __name__ == '__main__':
    main()