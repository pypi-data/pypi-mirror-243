# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aserto',
 'aserto.directory.common.v2',
 'aserto.directory.common.v3',
 'aserto.directory.exporter.v2',
 'aserto.directory.exporter.v3',
 'aserto.directory.importer.v2',
 'aserto.directory.importer.v3',
 'aserto.directory.model.v3',
 'aserto.directory.openapi.v3',
 'aserto.directory.reader.v2',
 'aserto.directory.reader.v3',
 'aserto.directory.schema.v2',
 'aserto.directory.schema.v3',
 'aserto.directory.writer.v2',
 'aserto.directory.writer.v3',
 'buf',
 'buf.validate',
 'buf.validate.priv',
 'google',
 'google.api']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.49,<2.0', 'protobuf>=4.21.0,<5.0.0']

extras_require = \
{':python_version >= "3.11"': ['protovalidate>=0.3.0,<0.4.0']}

setup_kwargs = {
    'name': 'aserto-directory',
    'version': '0.30.0',
    'description': 'gRPC client for Aserto Directory service instances',
    'long_description': '# Aserto Directory gRPC client\nThis is an automatically generated client for interacting with Aserto\'s\n[Directory service](https://docs.aserto.com/docs/overview/directory) using the gRPC protocol.\n\n## Installation\n### Using Pip\n```sh\npip install aserto-directory\n```\n### Using Poetry\n```sh\npoetry add aserto-directory\n```\n## Usage\n```py\nimport grpc\nfrom aserto.directory.reader.v2 import ReaderStub, GetObjectTypesRequest\n\nwith grpc.secure_channel(\n    target="directory.prod.aserto.com:8443",\n    credentials=grpc.ssl_channel_credentials(),\n) as channel:\n    reader = ReaderStub(channel)\n\n    # List all object types in the directory\n    response = reader.GetObjectTypes(\n        GetObjectTypesRequest(),\n        metadata=(\n            ("authorization", f"basic {ASERTO_DIRECTORY_API_KEY}"),\n            ("aserto-tenant-id", ASERTO_TENANT_ID),\n        ),\n    )\n\n    for object_type in response.results:\n        print("Object Type:", object_type.name)\n',
    'author': 'Aserto, Inc.',
    'author_email': 'pypi@aserto.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aserto-dev/python-directory',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
