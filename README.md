# SimpleWebsite Kubernetes Operator

The **SimpleWebsite** Operator is a Kubernetes operator designed to manage SimpleWebsite custom resources, enabling the automated deployment of web applications using the Kubernetes ecosystem.

## Table of Contents

- [SimpleWebsite Kubernetes Operator](#simplewebsite-kubernetes-operator)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Custom Resource Definition (CRD)](#custom-resource-definition-crd)
    - [Example Custom Resource (Static Website)](#example-custom-resource-static-website)
    - [Example Service (Python)](#example-service-python)
  - [RBAC Configuration](#rbac-configuration)
  - [License](#license)

## Overview

The SimpleWebsite Operator simplifies the deployment of web applications by managing resources like ConfigMaps, Deployments, Services, and Ingress based on custom resources defined by the user. This operator supports the management of static websites hosted on Nginx or custom services like python rest service by defining own path, image and command.

## Features

- Automatically create, update, and delete Kubernetes resources such as ConfigMaps, Deployments, Services, and Ingress.
- Validate configuration files before creating resources to ensure compliance with Kubernetes requirements.
- Uses Custom Resource Definitions (CRDs) to represent user-defined applications.

## Installation

To install the SimpleWebsite Operator, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd simplewebsite-operator

__Apply the provided Kubernetes manifests:__

```bash
kubectl create ns simplewebsite
kubectl -n simplewebsite apply -f resources/1_customresource.yaml
kubectl -n simplewebsite apply -f resources/2_rbac.yaml
kubectl -n simplewebsite apply -f resources/3_controller.yaml
```


## Usage
Once the operator is running, you can create instances of the SimpleWebsite custom resource. The operator will automatically manage the associated Kubernetes resources.

### Custom Resource Definition (CRD)
The Custom Resource Definition (CRD) for SimpleWebsite is defined as follows:

```
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: simplewebsites.mbx360.de
spec:
  group: mbx360.de
  names:
    kind: SimpleWebsite
    listKind: SimpleWebsiteList
    plural: simplewebsites
    singular: simplewebsite
  scope: Namespaced  # or Cluster if it's a cluster-scoped resource
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                domain:
                  type: string
                siteName:
                  type: string
                image:
                  type: string
                filePaths:
                  type: string
                command:
                  type: array
                  items:
                    type: string
                files:
                  type: array
                  items:
                    type: object
                    properties:
                      filename:
                        type: string
                      content:
                        type: string
```

### Example Custom Resource (Static Website)

Here is an example of how to define a SimpleWebsite resource:

```
apiVersion: mbx360.de/v1
kind: SimpleWebsite
metadata:
  name: hello-world
  namespace: simplewebsite
spec:
  domain: hello-world.mibexx.de
  siteName: hello-world
  files:
    - filename: index.html
      content: |
        <!DOCTYPE html>
        <html>
        <head>
            <title>Hello World</title>
        </head>
        <body>
            <h1>Hello, World!</h1>
            <p>Welcome to my Hello World website!</p>
        </body>
        </html>
    - filename: page2.html
      content: |
        <!DOCTYPE html>
        <html>
        <head>
            <title>Page 2</title>
        </head>
        <body>
            <h1>Welcome to Page 2!</h1>
        </body>
        </html>
```

### Example Service (Python)

```
# example_cr.yaml
apiVersion: mbx360.de/v1
kind: SimpleWebsite
metadata:
  name: sw-service
  namespace: simplewebsite
spec:
  domain: sw-service.mibexx.de
  siteName: sw-service
  port: 5000
  image: python:3.9-slim
  command:                  
    - /bin/sh
    - -c
    - |
      pip install Flask && python /app/main.py
  filePaths: /app
  files:
    - filename: main.py
      content: |
        from flask import Flask

        app = Flask(__name__)

        @app.route('/hello', methods=['GET'])
        def hello():
            return "Hello World", 200

        if __name__ == '__main__':
            app.run(host='0.0.0.0', port=5000)
```


## RBAC Configuration
The operator requires certain permissions to create and manage resources. Ensure that you have the appropriate RBAC configuration in place as defined in resources/2_rbac.yaml.

## License
This project is licensed under the MIT License