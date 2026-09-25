from pathlib import Path

def test_app_has_reviewer_sections_and_no_plotly_dependency():
    text=(Path(__file__).parents[1]/'app.py').read_text()
    for section in ['Overview','Research answers','Explore evidence','Opportunities','Methodology']:
        assert section in text
    assert '.plotly_chart(' not in text

def test_all_pages_render_without_exceptions():
    import pytest
    pytest.importorskip("streamlit", reason="Streamlit runtime must be installed for AppTest")
    from streamlit.testing.v1 import AppTest
    app=AppTest.from_file(str(Path(__file__).parents[1]/'app.py'))
    app.run(timeout=45)
    assert not app.exception
    for section in ['Overview','Research answers','Explore evidence','Opportunities','Methodology']:
        app.radio[0].set_value(section).run(timeout=45)
        assert not app.exception
