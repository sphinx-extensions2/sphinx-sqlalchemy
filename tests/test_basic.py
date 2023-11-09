"""Basic tests"""
import os.path
import sys

from sphinx_pytest.plugin import CreateDoctree


def test_basic(sphinx_doctree_no_tr: CreateDoctree, snapshot):
    """Basic test"""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "modules"))
    sphinx_doctree_no_tr.set_conf({"extensions": ["sphinx_sqlalchemy"]})
    result = sphinx_doctree_no_tr(".. sqla-model:: module1.TestUser")
    assert not result.warnings
    assert "\n".join([li.rstrip() for li in result.pformat().splitlines()]) == snapshot
