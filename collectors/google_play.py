"""Intentionally disabled by default: use an authorised export/import, not unverified scraping."""
def collect(*args, **kwargs):
    raise RuntimeError('Google Play collection requires an authorised export. Use generic_import.py.')

