'''
# Terraform CDK cloudinit Provider tracks ~> 2.2

This repo builds and publishes the Terraform cloudinit Provider bindings for [CDK for Terraform](https://cdk.tf).

Is based directly on cloudinit 2.3.3

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-cloudinit](https://www.npmjs.com/package/@cdktf/provider-cloudinit).

`npm install @cdktf/provider-cloudinit`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-cloudinit](https://pypi.org/project/cdktf-cdktf-provider-cloudinit).

`pipenv install cdktf-cdktf-provider-cloudinit`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Cloudinit](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Cloudinit).

`dotnet add package HashiCorp.Cdktf.Providers.Cloudinit`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-cloudinit](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-cloudinit).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-cloudinit</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-cloudinit-go`](https://github.com/cdktf/cdktf-provider-cloudinit-go) package.

`go get github.com/cdktf/cdktf-provider-cloudinit-go/cloudinit`

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-cloudinit).

## Versioning

This project is explicitly not tracking the Terraform cloudinit Provider version 1:1. In fact, it always tracks `latest` of `~> 2.2` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by generating the [provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [Terraform CDK](https://cdk.tf)
* [Terraform cloudinit Provider](https://registry.terraform.io/providers/hashicorp/cloudinit/2.3.3)

  * This links to the minimum version being tracked, you can find the latest released version [in our releases](https://github.com/cdktf/cdktf-provider-cloudinit/releases)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped.

## Features / Issues / Bugs

Please report bugs and issues to the [terraform cdk](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

### projen

This is mostly based on [projen](https://github.com/eladb/projen), which takes care of generating the entire repository.

### cdktf-provider-project based on projen

There's a custom [project builder](https://github.com/hashicorp/cdktf-provider-project) which encapsulate the common settings for all `cdktf` providers.

### Provider Version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).

### Repository Management

The repository is managed by [Repository Manager](https://github.com/hashicorp/cdktf-repository-manager/)
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

__all__ = [
    "config",
    "data_cloudinit_config",
    "provider",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import config
from . import data_cloudinit_config
from . import provider
