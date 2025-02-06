# SimpleWebsite Kubernetes Operator

The **SimpleWebsite** Operator is a Kubernetes operator designed to manage SimpleWebsite custom resources, enabling the automated deployment of web applications using the Kubernetes ecosystem.

## Table of Contents

- [SimpleWebsite Kubernetes Operator](#simplewebsite-kubernetes-operator)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Installation](#installation)
  - [RBAC Configuration](#rbac-configuration)
  - [Contributing](#contributing)
  - [License](#license)

## Overview

The SimpleWebsite Operator simplifies the deployment of web applications by managing resources like ConfigMaps, Deployments, Services, and Ingress based on custom resources defined by the user. This operator supports the management of static websites hosted on Nginx.

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
kubectl create ns simplewebsite
kubectl -n simplewebsite apply -f resources/1_customresource.yaml
kubectl -n simplewebsite apply -f resources/2_rbac.yaml
kubectl -n simplewebsite apply -f resources/3_controller.yaml


## Usage
Once the operator is running, you can create instances of the SimpleWebsite custom resource. The operator will automatically manage the associated Kubernetes resources.

### Custom Resource Definition (CRD)
The Custom Resource Definition (CRD) for SimpleWebsite is defined as follows:

```
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: simplewebsite.mbx360.de
spec:
  group: mbx360.de
  names:
    kind: SimpleWebsite
    listKind: SimpleWebsiteList
    plural: simplewebsites
    singular: simplewebsite
  scope: Namespaced
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

### Example Custom Resource

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

## RBAC Configuration
The operator requires certain permissions to create and manage resources. Ensure that you have the appropriate RBAC configuration in place as defined in rbac_definition.yaml.

## Contributing
Contributions are welcome! Please feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

This README provides a clear overview of your SimpleWebsite Operator, guides users through installation and usage, describes the custom resource and its structure, and includes RBAC configuration details. It is structured to facilitate understanding and usage by other developers.