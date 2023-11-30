def __func_alias__(hub):
    """
    pop construct to put request methods on the hub
    """

    def _get_caller(method):
        async def _request(ctx, url: str, **kwargs):
            return await hub.tool.request.session.request(
                ctx, method, url=url, **kwargs
            )

        return _request

    return {
        method: _get_caller(method)
        for method in ("delete", "head", "get", "patch", "post", "put")
    }


async def request(hub, ctx, method: str, url: str, **kwargs):
    """
    Make an aiohttp request using the named method
    :param hub:
    :param ctx: The context retrieved from the acct plugin
    :param method: delete|get|head|patch|post|put
    :param url: The url to request
    :param kwargs: kwargs to pass directly to aiohttp.ClientSession.request
    :return: A request-like response
    """
    session = await hub.tool.request.application.client(ctx)
    ret = await session.request(method=method, url=url, **kwargs)
    return ret
