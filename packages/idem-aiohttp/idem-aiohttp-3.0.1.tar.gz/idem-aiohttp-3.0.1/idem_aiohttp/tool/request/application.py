import hashlib

import aiohttp.abc
import aiohttp.web_app


class AsyncClientSession(aiohttp.ClientSession):
    """
    Async request session that dereferences it's connection when deleted (Since it is stored elsewhere on the hub)
    """

    def __del__(self):
        if not self.closed:
            self._connector = None


class AsyncConnector(aiohttp.TCPConnector):
    """
    An async connector that cleans up and doesn't spew warnings when it is deleted
    """

    def __del__(self):
        for ev in self._throttle_dns_events.values():
            ev.cancel()
        super()._close()


def __init__(hub):
    hub.tool.request.application.APP = aiohttp.web_app.Application()


def _generate_key(**kwargs) -> str:
    """
    Generate a unique but reproducible key from a dictionary
    """
    return hashlib.sha512(
        b"".join((str(k) + str(kwargs[k])).encode() for k in sorted(kwargs.keys()))
    ).hexdigest()


async def client(hub, ctx, client_class=AsyncClientSession) -> aiohttp.ClientSession:
    """
    Create an aiohttp Client Session based on the context
    """
    session_kwargs = ctx.acct.get("session", {})
    auth = ctx.acct.get("Auth")

    # headers can contain Authorization token, client should be regenerated if it changes
    auth_header = ctx.acct.get("headers", {})

    hub.acct.UNLOCKED = True

    client_key = "client_" + _generate_key(
        auth=auth, auth_header=auth_header, **session_kwargs
    )
    if client_key not in hub.tool.request.application.APP:
        hub.tool.request.application.APP[client_key] = client_class(
            auth=auth,
            connector_owner=False,
            connector=await hub.tool.request.application.connector(ctx),
            headers=ctx.acct.get("headers", {}),
            cookie_jar=await hub.tool.request.application.cookie_jar(ctx),
            **session_kwargs,
        )
    return hub.tool.request.application.APP[client_key]


async def cookie_jar(
    hub, ctx, cookie_jar_class=aiohttp.DummyCookieJar
) -> aiohttp.abc.AbstractCookieJar:
    cookie_jar_kwargs = ctx.acct.get("cookie_jar", {})

    cookie_jar_key = "cookie_jar_" + _generate_key(**cookie_jar_kwargs)
    if cookie_jar_key not in hub.tool.request.application.APP:
        hub.tool.request.application.APP[cookie_jar_key] = cookie_jar_class(
            **cookie_jar_kwargs
        )
    return hub.tool.request.application.APP[cookie_jar_key]


async def resolver(
    hub, ctx, resolver_class=aiohttp.DefaultResolver
) -> aiohttp.abc.AbstractResolver:
    """
    Retrieve the resolver for the given context, create it if it doesn't exist
    """
    resolver_kwargs = ctx.acct.get("resolver", {})

    resolver_key = "resolver_" + _generate_key(**resolver_kwargs)
    if resolver_key not in hub.tool.request.application.APP:
        hub.tool.request.application.APP[resolver_key] = resolver_class(
            **resolver_kwargs
        )
    return hub.tool.request.application.APP[resolver_key]


async def connector(hub, ctx, connector_class=AsyncConnector) -> aiohttp.BaseConnector:
    """
    Retrieve the connector for the given context, create it if it doesn't exist
    """
    resolve = await hub.tool.request.application.resolver(ctx)
    connector_kwargs = ctx.acct.get("connector", {})
    connector_key = "connector_" + _generate_key(resolve=resolve, **connector_kwargs)
    if connector_key not in hub.tool.request.application.APP:
        hub.tool.request.application.APP[connector_key] = connector_class(
            resolver=resolve,
            **connector_kwargs,
        )

    return hub.tool.request.application.APP[connector_key]
