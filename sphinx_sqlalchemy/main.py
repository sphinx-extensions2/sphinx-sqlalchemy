import importlib
import logging
from typing import List, Optional, Set

from docutils import nodes
from docutils.statemachine import StringList

# from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sqlalchemy import Column, Constraint, inspect
from sqlalchemy.orm.mapper import Mapper
from sqlalchemy.sql.schema import (
    CheckConstraint,
    ForeignKeyConstraint,
    Index,
    PrimaryKeyConstraint,
    UniqueConstraint,
)

logger = logging.getLogger(__name__)


def setup_extension(app: Sphinx) -> None:
    """Set up the sphinx extension."""
    app.add_directive("sqla-model", SqlaModelDirective)


class SqlaModelDirective(SphinxDirective):
    """A sphinx directive to document an SQLAlchemy Model"""

    required_arguments = 1
    final_argument_whitespace = True
    has_content = False
    # option_spec = {"col-doc": directives.flag}

    def run(self) -> List[nodes.Node]:
        """Run the directive"""

        # get module.class from argument
        if "." not in self.arguments[0]:
            raise self.error(
                f"Argument not of format 'module.class': {self.arguments[0]}"
            )
        module_name, class_name = self.arguments[0].rsplit(".", 1)

        # check whether to show the module prefix
        show_module = True
        if module_name.startswith("~"):
            show_module = False
            module_name = module_name[1:]

        # try to load the class
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:
            raise self.error(f"Could not import module '{module_name}': {exc}")
        klass = getattr(module, class_name, None)
        if klass is None:
            raise self.error(f"No class '{class_name}' in module '{module_name}'")
        mapper: Optional[Mapper] = inspect(klass, raiseerr=False)
        if mapper is None:
            raise self.error(
                f"Class '{class_name}' in module '{module_name}' is not an SQLAlchemy Model"
            )

        # create initial structure:
        # <definition_list classes="simple sqla">
        #     <definition_list_item>
        #         <term>
        #             Term
        #         <definition>
        #             ...
        main = nodes.definition_list(classes=["simple", "sqla"])
        def_list = nodes.definition_list_item()
        main += def_list
        name = nodes.Text(f"{module_name}.{class_name}" if show_module else class_name)
        if mapper.local_table is not None:
            def_list += nodes.term(
                "",
                name,
                nodes.Text(" ("),
                nodes.emphasis(text=f"{mapper.class_.__tablename__}"),
                nodes.Text(")"),
            )
        else:
            def_list += nodes.term("", name)
        definition = nodes.definition()
        def_list += definition

        self.add_content(mapper, definition)

        return [main]

    def add_content(self, mapper: Mapper, definition: nodes.definition) -> None:
        """Add content to the definition node."""

        # class documentation
        if mapper.class_.__doc__:
            self.state.nested_parse(
                StringList(mapper.class_.__doc__.splitlines()),
                self.content_offset,
                definition,
            )

        # column documentation
        if mapper.columns:
            columns = []
            for column in mapper.columns:
                # Skip column expressions without a data type,
                # eg. query_expressions. See query_expression on
                # https://docs.sqlalchemy.org/en/14/orm/loading_columns.html
                if not isinstance(column, Column):
                    logger.warning(f"Skipping column '{column.name}' {type(column)}")
                else:
                    columns.append(column)

            definition += nodes.rubric(text="Columns:")
            doc_column = any(column.doc for column in columns)
            cols = 3 if doc_column else 2
            definition += nodes.table(
                "",
                nodes.tgroup(
                    "", *([nodes.colspec()] * cols + [nodes.tbody()]), cols=cols
                ),
                classes=["colwidths-auto"],
                align="left",
            )
            body = definition[-1][-1][-1]
            for column in columns:
                row = nodes.row()
                body += row
                col_name = f"{column.name}"
                if column.unique or column.primary_key:
                    col_name += "*"
                if column.foreign_keys:
                    col_name = "→ " + col_name
                if column.primary_key:
                    row += nodes.entry(
                        "", nodes.paragraph("", "", nodes.emphasis(text=col_name))
                    )
                else:
                    row += nodes.entry("", nodes.paragraph(text=col_name))
                col_type = f"{column.type}"
                if column.nullable:
                    col_type += "?"
                row += nodes.entry("", nodes.paragraph(text=col_type))
                if doc_column:
                    row += nodes.entry("", nodes.paragraph(text=f"{column.doc or ''}"))

        # table constraints
        if mapper.local_table is not None and mapper.local_table.constraints:
            constraints: Set[Constraint] = mapper.local_table.constraints
            definition += nodes.rubric(text="Constraints:")
            definition += nodes.bullet_list()
            for text in sorted(contraint_to_str(c) for c in constraints):
                definition[-1] += nodes.list_item("", nodes.paragraph(text=text))

        # table indexes
        if mapper.local_table is not None and mapper.local_table.indexes:
            definition += nodes.rubric(text="Indexes:")
            definition += nodes.bullet_list()
            for text in sorted(index_to_str(c) for c in mapper.local_table.indexes):
                definition[-1] += nodes.list_item("", nodes.paragraph(text=text))


def contraint_to_str(constraint: Constraint) -> str:
    """Convert a constraint to a string."""
    if isinstance(constraint, PrimaryKeyConstraint):
        return f"PRIMARY KEY ({', '.join(c.name for c in constraint.columns)})"
    if isinstance(constraint, ForeignKeyConstraint):
        from_keys = ", ".join(
            f"{el.column.table.name}.{el.column.name}" for el in constraint.elements
        )
        to_keys = ", ".join(str(c) for c in constraint.column_keys)
        return f"FOREIGN KEY ({from_keys} → {to_keys})"
    if isinstance(constraint, UniqueConstraint):
        return f"UNIQUE ({', '.join(c.name for c in constraint.columns)})"
    if isinstance(constraint, CheckConstraint):
        return f"CHECK ({constraint.sqltext.text})"  # type: ignore
    return "UNKNOWN"


def index_to_str(index: Index) -> str:
    """Convert an index to a string."""
    return f"{index.name} ({', '.join(c.name for c in index.columns)})"
