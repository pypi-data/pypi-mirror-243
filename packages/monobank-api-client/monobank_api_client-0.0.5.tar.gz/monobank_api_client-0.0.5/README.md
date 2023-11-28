# monobank-api-client

## Name
monobank_api_client

## Installation
This framework is published at the PyPI, install it with pip:

    pip install monobank_api_client

To enable monobank_api_client for your Django REST Framework application, you need to install and configure monobank_api_client. To get started, add the following packages to your INSTALLED_APPS:

    INSTALLED_APPS = [
    ...
    'rest_framework',
    'monobank_api_client',
    ]

Include monobank_api_client urls to your urls.py:

    urlpatterns += [
        path(
            'mono/',
            include('monobank.urls', namespace='mono')
        ),
    ]
