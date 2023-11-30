async def gather(hub, profiles):
    default_idem_profile = hub.OPT.idem.get("acct_profile", hub.acct.DEFAULT)

    if not any(
        (
            name.startswith("request.")
            or name == "request"
            or name.startswith("http.")
            or name == "http"
        )
        for name in profiles
    ):
        return {default_idem_profile: {"dummy_key": "value"}}
    return {}
