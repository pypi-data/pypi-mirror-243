import aiohttp

__virtualname__ = "basic"


async def gather(hub, profiles):
    """
    parse over profiles that are just request or request.basic_auth

    Example:
    .. code-block:: yaml

        request:
            default:
                ...

        request.basic:
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
                  version: request_version
                  connector_owner: True
                  raise_for_status: False
                  conn_timeout:
                  auto_decompress: True
                  trust_env: False
                  requote_redirect_url: True
                  trace_configs:
                  read_bufsize: 65536
    """
    # The return profiles
    sub_profiles = {}

    # Get all profiles that use the "request.basic" plugin
    all_profiles = profiles.get("request.basic", {})
    # Get all profiles that don't have a sub plugin as well; they basic
    all_profiles.update(profiles.get("request", {}))

    for profile_name, ctx in all_profiles.items():
        if ctx is None:
            continue

        auth = ctx.get("auth", {})

        if auth:
            sub_profiles[profile_name] = {"Auth": aiohttp.BasicAuth(**auth)}
        else:
            sub_profiles[profile_name] = {"Auth": None}

    return sub_profiles
