"""Test reading of html files."""
import pymscada_html


def test_read():
    """Test file read."""
    fh = pymscada_html.get_html_file('favicon.ico')
    assert fh.name == 'favicon.ico'
