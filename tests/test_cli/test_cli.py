# -*- coding: utf-8 -*-
import os

from click.testing import CliRunner

from phenopackets.cli.cli import main
from tests import INPUT_EXAMPLES_PATH, INPUT_PATH

"""Test the module can be imported."""

import unittest

EXAMPLE_PACKET = str(INPUT_PATH / "Phenopacket-migrate-example.yaml")
TEST_ONTOLOGY = str(INPUT_PATH / "hp-subset.obo")


class TestCreate(unittest.TestCase):
    """A test case for create tests."""

    def setUp(self) -> None:
        self.runner = CliRunner(mix_stderr=False)

    def test_main_help(self):
        result = self.runner.invoke(main, ["--help"])
        out = result.stdout
        self.assertEqual(result.exit_code, 0)
        cases = [
            ("migrate-obsoletes", "OntologyClass"),
        ]
        for command, expected in cases:
            self.assertIn(command, out)
            result = self.runner.invoke(main, [command, "--help"])
            cmd_out = result.stdout
            self.assertEqual(result.exit_code, 0)
            self.assertIn(expected, cmd_out)

    def test_migrate_obsoletes(self):
        args = ["migrate-obsoletes", EXAMPLE_PACKET, "--ontology", TEST_ONTOLOGY]
        result = self.runner.invoke(main, args)
        out = result.stdout
        print(out)
        print(result.stderr)
        self.assertEqual(result.exit_code, 0)
        print(out)

    def test_update_labels(self):
        args = ["update-labels", EXAMPLE_PACKET, "--ontology", TEST_ONTOLOGY]
        result = self.runner.invoke(main, args)
        out = result.stdout
        print(out)
        print(result.stderr)
        self.assertEqual(result.exit_code, 0)
