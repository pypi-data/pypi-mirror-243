============
idem-aiohttp
============

aiohttp provider for Idem

DEVELOPMENT
===========

Clone the `idem-aiohttp` repository and install with pip.

.. code:: bash

    git clone git@gitlab.com:saltstack/idem/idem-aiohttp.git
    pip install -e idem-aiohttp

ACCT
====

After installation aiohttp Idem Provider execution and state modules will be accessible to the pop `hub`.
In order to use them we need to set up our credentials.

Create a new file called `credentials.yaml` and populate it with profiles.
The `default` profile will be used automatically by `idem` unless you specify one with `--acct-profile=profile_name` on the cli.

`acct backends <https://gitlab.com/saltstack/pop/acct-backends>`_ provide alternate methods for storing profiles.

A profile needs to specify the authentication parameters for aiohttp.
Every one of the parameters is optional.
Here, all available options are shown with their defaults:

credentials.yaml

..  code:: sls

    request.basic_auth:
      default:
        auth:
          # aiohttp.BasicAuth options
          login:
          password:
          encoding: latin1
        connector:
          # aiohttp.connector.TCPConnector options
          verify_ssl: True,
          fingerprint:
          use_dns_cache: True
          ttl_dns_cache: 10
          family: 0
          ssl_context:
          ssl:
          local_addr:
          keepalive_timeout:
          force_close: False
          limit: 100
          limit_per_host: 0
          enable_cleanup_closed: False
        resolver:
          # aiodns.DNSResolver options
          nameservers:
          # pycares.Channel options
          flags:
          timeout:
          tries:
          ndots:
          tcp_port:
          udp_port:
          servers:
          domains:
          lookups:
          sock_state_cb:
          socket_send_buffer_size:
          socket_receive_buffer_size:
          rotate:
          local_ip:
          local_dev:
          resolvconf_path:
        session:
          # aiohttp.ClientSession options
          cookies:
          headers:
          skip_auto_headers:
          version: http_version
          connector_owner: True
          raise_for_status: False
          conn_timeout:
          auto_decompress: True
          trust_env: False
          requote_redirect_url: True
          trace_configs:
          read_bufsize: 65536
        cookie_jar:
          quote_cookie=False
          unsafe=True

Now encrypt the credentials file and add the encryption key and encrypted file path to the ENVIRONMENT.

The `acct` command should be available as it is a requisite of `idem` and `idem_aiohttp`.
Encrypt the the credential file.

.. code:: bash

    acct encrypt credentials.yaml

output::

    -A9ZkiCSOjWYG_lbGmmkVh4jKLFDyOFH4e4S1HNtNwI=

Add these to your environment:

.. code:: bash

    export ACCT_KEY="-A9ZkiCSOjWYG_lbGmmkVh4jKLFDyOFH4e4S1HNtNwI="
    export ACCT_FILE=$PWD/credentials.yaml.fernet


USAGE
=====

If no profile is specified, the profile called "default", if one exists, will be used.
A profile can be specified from the command line when calling an exec module directly.

.. code:: bash

    idem exec --acct-profile my-staging-env request.raw.get https://my-url.com
