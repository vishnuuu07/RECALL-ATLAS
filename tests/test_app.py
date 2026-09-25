from pathlib import Path
def test_app_has_all_primary_sections():
    text=(Path(__file__).parents[1]/'app.py').read_text()
    for section in ['Research overview','Research questions','Memory & retrieval journey','Failure mechanisms','Opportunity lab','Evidence explorer','Research bridge','Methodology & audit']:
        assert section in text

def test_all_pages_render_without_exceptions():
    from streamlit.testing.v1 import AppTest
    app=AppTest.from_file(str(Path(__file__).parents[1]/'app.py'))
    app.run(timeout=30)
    for section in ['Research overview','Research questions','Memory & retrieval journey','Failure mechanisms','Opportunity lab','Evidence explorer','Research bridge','Methodology & audit']:
        app.radio[0].set_value(section).run(timeout=30)
        assert not app.exception
