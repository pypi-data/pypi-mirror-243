from typing import Dict
from typing import List

__virtualname__ = "json"


async def delete(
    hub,
    ctx,
    url: str,
    headers: Dict[str, str] = None,
    success_codes: List[int] = None,
    **kwargs,
):
    """
    Perform a delete request on the URL and return the parsed json result

    Args:
        url(str):
            Requested(str) URL
        headers(dict, Optional):
            HTTP Headers to send with the request
        success_codes(list, Optional):
            A list of status code integers that indicate a successful operation
        kwargs:
            All other keyword arguments will be passed to the aiohttp.request function
            https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.request

    Example:

    Calling this function from the CLI

    .. code-block:: bash

        $ idem exec request.json.delete "https://my_url.com"

    Calling this function from the state module

    .. code-block:: python

        async def my_state(hub, ctx, name):
            await hub.exec.request.json.delete(ctx, url="https://my_url.com")
    """
    result = dict(ret=None, result=True, status=None, comment=[], headers=None)
    if not success_codes:
        success_codes = [200]
    if not headers:
        headers = {}
    if not headers.get("content-type"):
        headers["content-type"] = "application/json"

    async with await hub.tool.request.session.delete(
        ctx, url=url, headers=headers, **kwargs
    ) as response:
        result["status"] = response.status
        result["result"] = response.status in success_codes
        result["comment"].append(response.reason)
        result["headers"] = response.headers
        try:
            result["ret"] = hub.tool.type.dict.namespaced(await response.json())
        except Exception as e:
            result["comment"].append(f"{e.__class__.__name__}: {e}")
            result["result"] = False
            ret = await response.read()
            result["ret"] = ret.decode() if hasattr(ret, "decode") else ret

        return result


async def get(
    hub,
    ctx,
    url: str,
    headers: Dict[str, str] = None,
    success_codes: List[int] = None,
    **kwargs,
):
    """
    Perform a get request on the URL and return the parsed json result

    Args:
        url(str):
            Requested(str) URL
        headers(dict, Optional):
            HTTP Headers to send with the request
        success_codes(list, Optional):
            A list of status code integers that indicate a successful operation
        kwargs:
            All other keyword arguments will be passed to the aiohttp.request function
            https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.request

    Example:

    Calling this function from the CLI

    .. code-block:: bash

        $ idem exec request.json.get "https://my_url.com" params='{}'

    Calling this function from the state module

    .. code-block:: python

        async def my_state(hub, ctx, name):
            await hub.exec.request.json.get(ctx, url="https://my_url.com", params={})
    """
    result = dict(ret=None, result=True, status=None, comment=[], headers=None)
    if not success_codes:
        success_codes = [200]
    if not headers:
        headers = {}
    if not headers.get("content-type"):
        headers["content-type"] = "application/json"

    async with await hub.tool.request.session.get(
        ctx, url=url, headers=headers, **kwargs
    ) as response:
        result["status"] = response.status
        result["result"] = response.status in success_codes
        result["comment"].append(response.reason)
        result["headers"] = response.headers
        try:
            result["ret"] = hub.tool.type.dict.namespaced(await response.json())
        except Exception as e:
            result["comment"].append(f"{e.__class__.__name__}: {e}")
            result["result"] = False
            ret = await response.read()
            result["ret"] = ret.decode() if hasattr(ret, "decode") else ret

        return result


async def head(
    hub,
    ctx,
    url: str,
    headers: Dict[str, str] = None,
    success_codes: List[int] = None,
    **kwargs,
):
    """
    Perform a head request on the URL and return the parsed json result

    Args:
        url(str):
            Requested(str) URL
        headers(dict, Optional):
            HTTP Headers to send with the request
        success_codes(list, Optional):
            A list of status code integers that indicate a successful operation
        kwargs:
            All other keyword arguments will be passed to the aiohttp.request function
            https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.request

    Example:

    Calling this function from the CLI

    .. code-block:: bash

        $ idem exec request.json.head "https://my_url.com"

    Calling this function from the state module

    .. code-block:: python

        async def my_state(hub, ctx, name):
            await hub.exec.request.json.head(ctx, url="https://my_url.com")
    """
    result = dict(ret=None, result=True, status=None, comment=[], headers=None)
    if not success_codes:
        success_codes = [200]
    if not headers:
        headers = {}
    if not headers.get("content-type"):
        headers["content-type"] = "application/json"

    async with await hub.tool.request.session.head(
        ctx, url=url, headers=headers, **kwargs
    ) as response:
        result["status"] = response.status
        result["result"] = response.status in success_codes
        result["comment"].append(response.reason)
        result["headers"] = response.headers
        result["ret"] = hub.tool.type.dict.namespaced(response.headers)

        return result


async def patch(
    hub,
    ctx,
    url: str,
    headers: Dict[str, str] = None,
    success_codes: List[int] = None,
    **kwargs,
):
    """
    Perform a patch request on the URL and return the parsed json result

    Args:
        url(str):
            Requested(str) URL
        headers(dict, Optional):
            HTTP Headers to send with the request
        success_codes(list, Optional):
            A list of status code integers that indicate a successful operation
        kwargs:
            All other keyword arguments will be passed to the aiohttp.request function
            https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.request


    Example:

    Calling this function from the CLI

    .. code-block:: bash

        $ idem exec request.json.patch "https://my_url.com" json='{}'

    Calling this function from the state module

    .. code-block:: python

        async def my_state(hub, ctx, name):
            await hub.exec.request.json.patch(ctx, url="https://my_url.com", json={})
    """
    result = dict(ret=None, result=True, status=None, comment=[], headers=None)
    if not success_codes:
        success_codes = [200]
    if not headers:
        headers = {}
    if not headers.get("content-type"):
        headers["content-type"] = "application/json"

    async with await hub.tool.request.session.patch(
        ctx, url=url, headers=headers, **kwargs
    ) as response:
        result["status"] = response.status
        result["result"] = response.status in success_codes
        result["comment"].append(response.reason)
        result["headers"] = response.headers
        try:
            result["ret"] = hub.tool.type.dict.namespaced(await response.json())
        except Exception as e:
            result["comment"].append(f"{e.__class__.__name__}: {e}")
            result["result"] = False
            ret = await response.read()
            result["ret"] = ret.decode() if hasattr(ret, "decode") else ret

        return result


async def post(
    hub,
    ctx,
    url: str,
    headers: Dict[str, str] = None,
    success_codes: List[int] = None,
    **kwargs,
):
    """
    Perform a post request on the URL and return the parsed json result

    Args:
        url(str):
            Requested(str) URL
        headers(dict, Optional):
            HTTP Headers to send with the request
        success_codes(list, Optional):
            A list of status code integers that indicate a successful operation
        kwargs:
            All other keyword arguments will be passed to the aiohttp.request function
            https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.request


    Example:

    Calling this function from the CLI

    .. code-block:: bash

        $ idem exec request.json.post "https://my_url.com" json='{}'

    Calling this function from the state module

    .. code-block:: python

        async def my_state(hub, ctx, name):
            await hub.exec.request.json.post(ctx, url="https://my_url.com", json={})
    """
    result = dict(ret=None, result=True, status=None, comment=[], headers=None)
    if not success_codes:
        success_codes = [200]
    if not headers:
        headers = {}
    if not headers.get("content-type"):
        headers["content-type"] = "application/json"

    async with await hub.tool.request.session.post(
        ctx, url=url, headers=headers, **kwargs
    ) as response:
        result["status"] = response.status
        result["result"] = response.status in success_codes
        result["comment"].append(response.reason)
        result["headers"] = response.headers
        try:
            result["ret"] = hub.tool.type.dict.namespaced(await response.json())
        except Exception as e:
            result["comment"].append(f"{e.__class__.__name__}: {e}")
            result["result"] = False
            ret = await response.read()
            result["ret"] = ret.decode() if hasattr(ret, "decode") else ret

        return result


async def put(
    hub,
    ctx,
    url: str,
    headers: Dict[str, str] = None,
    success_codes: List[int] = None,
    **kwargs,
):
    """
    Perform a put request on the URL and return the parsed json result

    Args:
        url(str):
            Requested(str) URL
        headers(dict, Optional):
            HTTP Headers to send with the request
        success_codes(list, Optional):
            A list of status code integers that indicate a successful operation
        kwargs:
            All other keyword arguments will be passed to the aiohttp.request function
            https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.request


    Example:

    Calling this function from the CLI

    .. code-block:: bash

        $ idem exec request.json.put "https://my_url.com" json='{}'

    Calling this function from the state module

    .. code-block:: python

        async def my_state(hub, ctx, name):
            await hub.exec.request.json.put(ctx, url="https://my_url.com", json={})
    """
    result = dict(ret=None, result=True, status=None, comment=[], headers=None)
    if not success_codes:
        success_codes = [200]
    if not headers:
        headers = {}
    if not headers.get("content-type"):
        headers["content-type"] = "application/json"

    async with await hub.tool.request.session.put(
        ctx, url=url, headers=headers, **kwargs
    ) as response:
        result["status"] = response.status
        result["result"] = response.status in success_codes
        result["comment"].append(response.reason)
        result["headers"] = response.headers
        try:
            result["ret"] = hub.tool.type.dict.namespaced(await response.json())
        except Exception as e:
            result["comment"].append(f"{e.__class__.__name__}: {e}")
            result["result"] = False
            ret = await response.read()
            result["ret"] = ret.decode() if hasattr(ret, "decode") else ret

        return result
