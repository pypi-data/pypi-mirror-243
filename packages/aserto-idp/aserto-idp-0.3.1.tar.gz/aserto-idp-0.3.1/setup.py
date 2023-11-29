# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aserto_idp', 'aserto_idp.oidc']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.0,<4.0.0', 'python-jose[cryptography]>=3.3.0,<4.0.0']

setup_kwargs = {
    'name': 'aserto-idp',
    'version': '0.3.1',
    'description': 'Common identity providers for use with Aserto client libraries',
    'long_description': '# Aserto Identity Providers\nCommon identity providers for use with Aserto client libraries\n\n## Installation\n### Using Pip\n```sh\npip install aserto-idp\n```\n### Using Poetry\n```sh\npoetry add aserto-idp\n```\n## Current Identity Providers\n### OpenID Connect\n```py\nfrom aserto_idp.oidc import identity_provider\n```\n## Usage\n### With [`aserto-authorizer-grpc`](https://github.com/aserto-dev/aserto-python/tree/HEAD/packages/aserto-authorizer-grpc)\n```py\nfrom aserto.client import IdentityContext, IdentityType\nfrom aserto_idp.oidc import AccessTokenError, identity_provider\n\noidc_provider = identity_provider(issuer=OIDC_ISSUER, client_id=OIDC_CLIENT_ID)\n\ntry:\n    subject = await oidc_provider.subject_from_jwt_auth_header(request.headers["Authorization"])\n\n    identity_context = IdentityContext(\n        type=IdentityType.IDENTITY_TYPE_SUB,\n        identity=subject,\n    )\nexcept AccessTokenError:\n    identity_context = IdentityContext(type=IdentityType.IDENTITY_TYPE_NONE)\n\n```\n### With [`aserto`](https://github.com/aserto-dev/aserto-python/tree/HEAD/packages/aserto)\n```py\nfrom aserto import Identity\nfrom aserto_idp.oidc import AccessTokenError, IdentityProvider\n\noidc_provider = identity_provider(issuer=OIDC_ISSUER, client_id=OIDC_CLIENT_ID)\n\ntry:\n    subject = await oidc_provider.subject_from_jwt_auth_header(request.headers["Authorization"])\n\n    identity = Identity(type="SUBJECT", subject=subject)\nexcept AccessTokenError:\n    identity = Identity(type="NONE")\n```\n',
    'author': 'Aserto, Inc.',
    'author_email': 'pypi@aserto.com',
    'maintainer': 'authereal',
    'maintainer_email': 'authereal@aserto.com',
    'url': 'https://github.com/aserto-dev/aserto-python/tree/HEAD/packages/aserto-idp',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
