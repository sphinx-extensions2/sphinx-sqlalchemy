"""Basic tests"""

import os.path
import sys

from sphinx_pytest.plugin import CreateDoctree


def test_multiline_docstring_d212(sphinx_doctree_no_tr: CreateDoctree, snapshot):
    """Basic test for models with multiline docstring with D212 format

    see: https://docs.astral.sh/ruff/rules/multi-line-summary-first-line
    """
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "modules"))
    sphinx_doctree_no_tr.set_conf({"extensions": ["sphinx_sqlalchemy"]})
    result = sphinx_doctree_no_tr(
        ".. sqla-model:: module2.TestUserMultilineDocstringD212"
    )
    assert not result.warnings
    assert "\n".join([li.rstrip() for li in result.pformat().splitlines()]) == snapshot


def test_multiline_docstring_d213(sphinx_doctree_no_tr: CreateDoctree, snapshot):
    """Basic test for models with multiline docstring with D213 format

    see: https://docs.astral.sh/ruff/rules/multi-line-summary-second-line
    """
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "modules"))
    sphinx_doctree_no_tr.set_conf({"extensions": ["sphinx_sqlalchemy"]})
    result = sphinx_doctree_no_tr(
        ".. sqla-model:: module2.TestUserMultilineDocstringD213"
    )
    assert not result.warnings
    assert "\n".join([li.rstrip() for li in result.pformat().splitlines()]) == snapshot
