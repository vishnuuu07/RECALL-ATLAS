from collectors.google_play import collect
import pytest
def test_restricted_collector_is_explicit():
    with pytest.raises(RuntimeError):collect()
