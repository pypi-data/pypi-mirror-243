# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aserto',
 'aserto.authorizer.v2',
 'aserto.authorizer.v2.api',
 'google',
 'google.api',
 'protoc_gen_openapiv2',
 'protoc_gen_openapiv2.options']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.49,<2.0', 'protobuf>=4.21.0,<5.0.0']

setup_kwargs = {
    'name': 'aserto-authorizer',
    'version': '0.20.2rc1',
    'description': 'gRPC client for Aserto Authorizer service instances',
    'long_description': '# Aserto Authorizer gRPC client\nThis is an automatically generated client for interacting with Aserto\'s [Authorizer service](https://docs.aserto.com/docs/authorizer-guide/overview) using the gRPC protocol.\n\n## Installation\n### Using Pip\n```sh\npip install aserto-authorizer\n```\n### Using Poetry\n```sh\npoetry add aserto-authorizer\n```\n## Usage\n```py\nimport grpc\nfrom aserto.authorizer.v2.api import (\n    IdentityContext,\n    IdentityType,\n    PolicyContext,\n    PolicyInstance,\n)\nfrom aserto.authorizer.v2 import (\n    AuthorizerStub,\n    DecisionTreeRequest,\n    DecisionTreeOptions,\n    DecisionTreeResponse,\n    PathSeparator,\n)\nfrom grpclib.client import Channel\n\n\nwith grpc.secure_channel(\n    target="authorizer.prod.aserto.com:8443",\n    credentials=grpc.ssl_channel_credentials(),\n) as channel:\n    client = AuthorizerStub(channel)\n\n    response = client.DecisionTree(\n        DecisionTreeRequest(\n            policy_context=PolicyContext(\n                path=ASERTO_POLICY_PATH_ROOT,\n                decisions=["visible", "enabled", "allowed"],\n            ),\n            policy_instance=PolicyInstance(\n                name=ASERTO_POLICY_NAME,\n                instance_label=ASERTO_POLICY_INSTANCE_LABEL,\n            ),\n            identity_context=IdentityContext(type=IdentityType.IDENTITY_TYPE_NONE),\n            options=DecisionTreeOptions(\n                path_separator=PathSeparator.PATH_SEPARATOR_DOT,\n            ),\n        )\n    )\n\n    assert response == DecisionTreeResponse(\n        path_root=ASERTO_POLICY_PATH_ROOT,\n        path=Proto.Struct(\n            fields={\n                "GET.your.policy.path": Proto.Value(\n                    struct_value=Proto.Struct(\n                        fields={\n                            "visible": Proto.Value(bool_value=True),\n                            "enabled": Proto.Value(bool_value=True),\n                            "allowed": Proto.Value(bool_value=False),\n                        },\n                    ),\n                ),\n            },\n        ),\n    )\n```\n',
    'author': 'Aserto, Inc.',
    'author_email': 'pypi@aserto.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aserto-dev/python-authorizer',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
