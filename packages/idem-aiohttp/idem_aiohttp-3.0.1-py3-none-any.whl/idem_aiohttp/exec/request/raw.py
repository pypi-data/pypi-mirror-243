from typing import List


async def delete(hub, ctx, url: str, success_codes: List[int] = None, **kwargs):
    """
    Perform a delete request on the URL and return the result.

    Args:
        url(str):
            Requested(str) URL
        success_codes(list, Optional):
            A list of status code integers that indicate a successful operation
        kwargs:
            All other keyword arguments will be passed to the aiohttp.request function
            https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.request


    Example:

    Calling this function from the CLI

    .. code-block:: bash

        $ idem exec request.raw.delete "https://my_url.com"

    Calling this function from the state module

    .. code-block:: python

        async def my_state(hub, ctx, name):
            await hub.exec.request.raw.delete(ctx, url="https://my_url.com")
    """
    result = dict(ret=None, result=True, status=None, comment=[], headers=None)
    if not success_codes:
        success_codes = [200]
    async with await hub.tool.request.session.delete(
        ctx, url=url, **kwargs
    ) as response:
        result["status"] = response.status
        result["result"] = response.status in success_codes
        result["comment"].append(response.reason)
        result["headers"] = response.headers
        result["ret"] = await response.read()

    return result


async def get(hub, ctx, url: str, success_codes: List[int] = None, **kwargs):
    """
    Perform a get request on the URL and return the result.

    Args:
        url(str):
            Requested(str) URL
        success_codes(list, Optional):
            A list of status code integers that indicate a successful operation
        kwargs:
            All other keyword arguments will be passed to the aiohttp.request function
            https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.request


    Example:

    Calling this function from the CLI

    .. code-block:: bash

        $ idem exec request.raw.get "https://my_url.com" params='{}'

    Calling this function from the state module

    .. code-block:: python

        async def my_state(hub, ctx, name):
            await hub.exec.request.raw.get(ctx, url="https://my_url.com", params={})
    """
    result = dict(ret=None, result=True, status=None, comment=[], headers=None)
    if not success_codes:
        success_codes = [200]
    async with await hub.tool.request.session.get(ctx, url=url, **kwargs) as response:
        result["status"] = response.status
        result["result"] = response.status in success_codes
        result["comment"].append(response.reason)
        result["headers"] = response.headers
        result["ret"] = await response.read()

    return result


async def head(hub, ctx, url: str, success_codes: List[int] = None, **kwargs):
    """
    Perform a get request on the URL and return the result.

    Args:
        url(str):
            Requested(str) URL
        success_codes(list, Optional):
            A list of status code integers that indicate a successful operation
        kwargs:
            All other keyword arguments will be passed to the aiohttp.request function
            https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.request


    Example:

    Calling this function from the CLI

    .. code-block:: bash

        $ idem exec request.raw.get "https://my_url.com"

    Calling this function from the state module

    .. code-block:: python

        async def my_state(hub, ctx, name):
            await hub.exec.request.raw.get(ctx, url="https://my_url.com")
    """
    result = dict(ret=None, result=True, status=None, comment=[], headers=None)
    if not success_codes:
        success_codes = [200]
    async with await hub.tool.request.session.head(ctx, url=url, **kwargs) as response:
        result["status"] = response.status
        result["result"] = response.status in success_codes
        result["comment"].append(response.reason)
        result["headers"] = response.headers
        result["ret"] = hub.tool.type.dict.namespaced(response.headers)

    return result


async def patch(hub, ctx, url: str, success_codes: List[int] = None, **kwargs):
    """
    Perform a patch request on the URL and return the result.

    Args:
        url(str):
            Requested(str) URL
        success_codes(list, Optional):
            A list of status code integers that indicate a successful operation
        kwargs:
            All other keyword arguments will be passed to the aiohttp.request function
            https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.request


    Example:

    Calling this function from the CLI

    .. code-block:: bash

        $ idem exec request.raw.patch "https://my_url.com" json='{}'

    Calling this function from the state module

    .. code-block:: python

        async def my_state(hub, ctx, name):
            await hub.exec.request.raw.patch(ctx, url="https://my_url.com", json={})
    """
    result = dict(ret=None, result=True, status=None, comment=[], headers=None)
    if not success_codes:
        success_codes = [200]
    async with await hub.tool.request.session.patch(ctx, url=url, **kwargs) as response:
        result["status"] = response.status
        result["result"] = response.status in success_codes
        result["comment"].append(response.reason)
        result["headers"] = response.headers
        result["ret"] = await response.read()

    return result


async def post(hub, ctx, url: str, success_codes: List[int] = None, **kwargs):
    """
    Perform a post request on the URL and return the result.

    Args:
        url(str):
            Requested(str) URL
        success_codes(list, Optional):
            A list of status code integers that indicate a successful operation
        kwargs:
            All other keyword arguments will be passed to the aiohttp.request function
            https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.request


    Example:

    Calling this function from the CLI

    .. code-block:: bash

        $ idem exec request.raw.post "https://my_url.com" json='{}'

    Calling this function from the state module

    .. code-block:: python

        async def my_state(hub, ctx, name):
            await hub.exec.request.raw.post(ctx, url="https://my_url.com", json={})
    """
    result = dict(ret=None, result=True, status=None, comment=[], headers=None)
    if not success_codes:
        success_codes = [200]
    async with await hub.tool.request.session.post(ctx, url=url, **kwargs) as response:
        result["status"] = response.status
        result["result"] = response.status in success_codes
        result["comment"].append(response.reason)
        result["headers"] = response.headers
        result["ret"] = await response.read()

    return result


async def put(hub, ctx, url: str, success_codes: List[int] = None, **kwargs):
    """
    Perform a put request on the URL and return the result.

    Args:
        url(str):
            Requested(str) URL
        success_codes(list, Optional):
            A list of status code integers that indicate a successful operation
        kwargs:
            All other keyword arguments will be passed to the aiohttp.request function
            https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.request


    Example:

    Calling this function from the CLI

    .. code-block:: bash

        $ idem exec request.raw.put "https://my_url.com" json='{}'

    Calling this function from the state module

    .. code-block:: python

        async def my_state(hub, ctx, name):
            await hub.exec.request.raw.put(ctx, url="https://my_url.com", json={})
    """
    result = dict(ret=None, result=True, status=None, comment=[], headers=None)
    if not success_codes:
        success_codes = [200]
    async with await hub.tool.request.session.put(ctx, url=url, **kwargs) as response:
        result["status"] = response.status
        result["result"] = response.status in success_codes
        result["comment"].append(response.reason)
        result["headers"] = response.headers
        result["ret"] = await response.read()

    return result
