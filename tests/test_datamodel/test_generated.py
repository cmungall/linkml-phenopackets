# -*- coding: utf-8 -*-
import unittest
from pathlib import Path

from linkml.generators.pydanticgen import PydanticGenerator
from linkml.generators.pythongen import PythonGenerator

import phenopackets.datamodel.phenopackets as datamodel
import phenopackets.pydantic.model as pydantic_model
from phenopackets.datamodel import MAIN_SCHEMA_PATH


def code(text: str):
    """The lines of generated code, without the lines that state when it was generated,
    and under which path the schema was read."""
    lines = text.strip().splitlines()
    return [
        line for line in lines
        if not line.startswith("# Generation date:") and "'source_file':" not in line
    ]


class TestGenerated(unittest.TestCase):
    """The Python classes are generated from the schema, see the Makefile.

    These tests generate them again, and fail when the result differs from the
    code in the repository: the schema has changed and `make all py` or
    `make src/phenopackets/pydantic/model.py` was not run after that.
    """

    maxDiff = 2000

    def test_dataclasses(self):
        generated = PythonGenerator(str(MAIN_SCHEMA_PATH)).serialize(mergeimports=True)
        self.assertEqual(code(Path(datamodel.__file__).read_text()), code(generated))

    def test_pydantic(self):
        generated = PydanticGenerator(str(MAIN_SCHEMA_PATH)).serialize()
        self.assertEqual(code(Path(pydantic_model.__file__).read_text()), code(generated))
