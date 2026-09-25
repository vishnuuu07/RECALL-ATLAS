"""Reddit API requires credentials; this collector does not scrape unauthorised endpoints."""
def collect(*args, **kwargs):
    raise RuntimeError('Configure an authorised Reddit API client or import permitted records.')

