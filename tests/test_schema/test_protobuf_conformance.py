# -*- coding: utf-8 -*-
"""Check that the LinkML schema is in sync with the phenopacket-schema release.

The reference is ``tests/input/phenopacket-schema-<release>/descriptors.json``:
everything that the protobuf files of the release define, as compiled by protoc
(see ``util/proto_inventory.py`` and ``make descriptors``). The release is the
one that the root module names as its ``source``. The tests fail when the schema
and the release drift apart, in either direction.

They also document how protobuf is translated to LinkML:

* a protobuf file is a module with the same name, which imports the modules of
  the files that the protobuf file imports
* a message is a class with the same name. A nested message has its simple name
  (``Pedigree.Person`` is ``Person``) unless that name is used by more than one
  message, in which case the names of the enclosing messages are prepended
  (``Haplotype.Member`` is ``HaplotypeMember``)
* a field is an attribute named after the JSON name of the field, with the field
  number as its ``rank`` annotation
* ``repeated`` fields are multivalued, and message fields are always inlined
* a ``map<string, string>`` field is a multivalued attribute that is inlined as
  a dictionary of ``DictionaryEntry`` objects
* ``google.protobuf.Timestamp`` and ``google.protobuf.Any`` fields are strings
* a ``oneof`` is a rule annotated with the name of the oneof, which says that
  exactly one of its fields is required
* an enum is an enum with the same values, in the same order, each with its
  number as ``rank`` annotation
* a comment above an element is its description. Other comments are kept as
  comments.
"""
import json
import re
import unittest
from collections import Counter

import yaml
from linkml_runtime import SchemaView

from phenopackets.datamodel import MAIN_SCHEMA_PATH, SCHEMA_DIRECTORY
from tests import INPUT_PATH

SCHEMA_ID_BASE = "https://w3id.org/linkml/phenopackets/"

# Modules that are not generated from protobuf
CURATED_MODULES = ["cv_terms", "constants"]

SCALAR_RANGES = {
    "string": "string",
    "bytes": "string",
    "bool": "boolean",
    "double": "double",
    "float": "float",
    "int32": "integer",
    "int64": "integer",
    "uint32": "integer",
    "uint64": "integer",
}

# Well known types are flattened to strings. In the protobuf JSON mapping a
# Timestamp is an RFC 3339 string.
WELL_KNOWN_TYPE_RANGES = {
    "google.protobuf.Timestamp": "string",
    "google.protobuf.Any": "string",
}

MAP_ENTRY_CLASS = "DictionaryEntry"

# The `source` of the root module is the file of the release that it was
# generated from. This is the only place where the schema states its release.
ROOT_SOURCE = re.compile(
    r"https://github\.com/phenopackets/phenopacket-schema/blob/([^/]+)"
    r"/src/main/proto/phenopackets/schema/v2/phenopackets\.proto"
)


def normalize(text):
    """Collapse whitespace, which differs between protoc and the schema."""
    return " ".join((text or "").split())


def module_name(proto_file):
    """phenopackets/schema/v2/core/base.proto => base"""
    return proto_file.split("/")[-1].replace(".proto", "")


def annotation(element, tag):
    annotations = element.annotations
    if not annotations or tag not in annotations:
        return None
    return annotations[tag].value


class TestProtobufConformance(unittest.TestCase):
    """Compare the schema with the protobuf descriptors of the release."""

    @classmethod
    def setUpClass(cls):
        cls.sv = SchemaView(str(MAIN_SCHEMA_PATH))
        source = cls.sv.schema.source
        release = ROOT_SOURCE.fullmatch(source or "")
        if not release:
            raise AssertionError(
                f"the source of the root module is {source}, "
                "expected the phenopackets.proto file of a phenopacket-schema release"
            )
        path = INPUT_PATH / f"phenopacket-schema-{release.group(1)}" / "descriptors.json"
        with open(path) as stream:
            cls.proto = json.load(stream)
        cls.messages = cls.proto["messages"]
        cls.enums = cls.proto["enums"]
        cls.classes = cls.sv.all_classes()
        simple_names = Counter(m["name"] for m in cls.messages.values())
        cls.class_names = {}
        for name, message in cls.messages.items():
            class_name = message["name"]
            if simple_names[class_name] > 1:
                parent = message["parent"]
                while parent:
                    class_name = cls.messages[parent]["name"] + class_name
                    parent = cls.messages[parent]["parent"]
            cls.class_names[name] = class_name

    def assertNoProblems(self, problems):
        self.assertEqual([], problems, "\n" + "\n".join(problems))

    def expected_range(self, field):
        if field["kind"] == "scalar":
            return SCALAR_RANGES[field["type"]]
        if field["kind"] == "map":
            self.assertEqual("map<string, string>", field["type"])
            return MAP_ENTRY_CLASS
        if field["type"] in WELL_KNOWN_TYPE_RANGES:
            return WELL_KNOWN_TYPE_RANGES[field["type"]]
        if field["kind"] == "message":
            return self.class_names[field["type"]]
        return self.enums[field["type"]]["name"]

    def test_modules(self):
        """Each protobuf file is a module that imports what the file imports."""
        problems = []
        for proto_file, file in self.proto["files"].items():
            name = module_name(proto_file)
            path = SCHEMA_DIRECTORY / f"{name}.yaml"
            if not path.exists():
                problems.append(f"{proto_file}: no module {name}")
                continue
            with open(path) as stream:
                module = yaml.safe_load(stream)
            if module["id"] != SCHEMA_ID_BASE + name:
                problems.append(f"{name}: id is {module['id']}")
            expected = sorted(module_name(d) for d in file["dependencies"])
            imports = sorted(
                i for i in module["imports"] if i != "linkml:types" and i not in CURATED_MODULES
            )
            if imports != expected:
                problems.append(f"{name}: imports {imports}, {proto_file} imports {expected}")
            # everything in a generated module is a class or an enum
            for section in ["slots", "types", "subsets"]:
                if module.get(section):
                    problems.append(f"{name}: defines {section} {sorted(module[section])}")
        modules = {path.stem for path in SCHEMA_DIRECTORY.glob("*.yaml")}
        expected = {module_name(f) for f in self.proto["files"]} | set(CURATED_MODULES)
        if modules != expected:
            problems.append(f"modules {sorted(modules)}, expected {sorted(expected)}")
        self.assertNoProblems(problems)

    def test_classes(self):
        """Every message is a class, and every class is a message."""
        problems = []
        self.assertEqual(
            len(self.class_names),
            len(set(self.class_names.values())),
            "two messages are translated to the same class",
        )
        for name, message in self.messages.items():
            class_name = self.class_names[name]
            if class_name not in self.classes:
                problems.append(f"{name}: no class {class_name}")
                continue
            expected = SCHEMA_ID_BASE + module_name(message["file"])
            if self.classes[class_name].from_schema != expected:
                problems.append(f"{class_name}: is not defined in {expected}")
        extra = set(self.classes) - set(self.class_names.values()) - {MAP_ENTRY_CLASS}
        if extra:
            problems.append(f"classes that are not a message: {sorted(extra)}")
        self.assertNoProblems(problems)

    def test_attributes(self):
        """Every field is an attribute with the same name, type and cardinality."""
        problems = []
        for name, message in self.messages.items():
            class_name = self.class_names[name]
            attributes = set(self.sv.class_slots(class_name))
            expected = {f["json_name"] for f in message["fields"]}
            if attributes != expected:
                problems.append(
                    f"{class_name}: attributes {sorted(attributes)}, fields {sorted(expected)}"
                )
            for field in message["fields"]:
                attribute_name = field["json_name"]
                if attribute_name not in attributes:
                    continue
                where = f"{class_name}.{attribute_name}"
                slot = self.sv.induced_slot(attribute_name, class_name)
                if str(annotation(slot, "rank")) != str(field["number"]):
                    problems.append(f"{where}: rank is not field number {field['number']}")
                expected_range = self.expected_range(field)
                if slot.range != expected_range:
                    problems.append(f"{where}: range {slot.range}, expected {expected_range}")
                is_map = field["kind"] == "map"
                if bool(slot.multivalued) != (field["repeated"] or is_map):
                    problems.append(f"{where}: multivalued is {slot.multivalued}")
                if bool(slot.deprecated) != field["deprecated"]:
                    problems.append(f"{where}: deprecated is {slot.deprecated}")
                if expected_range in self.classes:
                    # protobuf messages contain other messages, they never refer to them
                    if not self.sv.is_inlined(slot):
                        problems.append(f"{where}: is not inlined")
                    has_key = self.sv.get_identifier_slot(expected_range, use_key=True)
                    if is_map and (slot.inlined_as_list or not has_key):
                        problems.append(f"{where}: map is not inlined as a dictionary")
                    if field["repeated"] and has_key and not slot.inlined_as_list:
                        problems.append(f"{where}: repeated field is not inlined as a list")
        self.assertNoProblems(problems)

    def test_map_entry(self):
        """A protobuf map<string, string> is a list of entries with a key and a value."""
        attributes = self.sv.class_induced_slots(MAP_ENTRY_CLASS)
        self.assertCountEqual(["key", "value"], [a.name for a in attributes])
        self.assertEqual("key", self.sv.get_identifier_slot(MAP_ENTRY_CLASS, use_key=True).name)
        for attribute in attributes:
            self.assertEqual("string", attribute.range)

    def test_oneofs(self):
        """Every oneof is a rule, and every rule is a oneof."""
        problems = []
        for name, message in self.messages.items():
            class_name = self.class_names[name]
            expected = {
                oneof["name"]: sorted(
                    f["json_name"] for f in message["fields"] if f["oneof"] == oneof["name"]
                )
                for oneof in message["oneofs"]
            }
            rules = {}
            for rule in self.classes[class_name].rules:
                members = []
                # each alternative of the rule requires one field of the oneof
                for alternative in rule.postconditions.exactly_one_of:
                    conditions = alternative.slot_conditions
                    if len(conditions) != 1 or any(c.required is not True for c in conditions.values()):
                        problems.append(f"{class_name}: unexpected alternative {alternative}")
                    members.extend(conditions)
                rules[annotation(rule, "oneof")] = sorted(members)
            if rules != expected:
                problems.append(f"{class_name}: rules {rules}, oneofs {expected}")
        self.assertNoProblems(problems)

    def test_enums(self):
        """Every enum has the same values, in the same order, with the same numbers."""
        problems = []
        all_enums = self.sv.all_enums()
        for name, enum in self.enums.items():
            if enum["name"] not in all_enums:
                problems.append(f"{name}: no enum {enum['name']}")
                continue
            definition = all_enums[enum["name"]]
            expected = SCHEMA_ID_BASE + module_name(enum["file"])
            if definition.from_schema != expected:
                problems.append(f"{enum['name']}: is not defined in {expected}")
            values = [(v["name"], str(v["number"]), v["deprecated"]) for v in enum["values"]]
            permissible_values = [
                (text, str(annotation(pv, "rank")), bool(pv.deprecated))
                for text, pv in definition.permissible_values.items()
            ]
            if permissible_values != values:
                problems.append(f"{enum['name']}: {permissible_values}, expected {values}")
        curated = [SCHEMA_ID_BASE + module for module in CURATED_MODULES]
        generated = {n for n, e in all_enums.items() if e.from_schema not in curated}
        extra = generated - {enum["name"] for enum in self.enums.values()}
        if extra:
            problems.append(f"enums that are not a protobuf enum: {sorted(extra)}")
        self.assertEqual(
            len(self.enums),
            len({e["name"] for e in self.enums.values()}),
            "two protobuf enums have the same name",
        )
        self.assertNoProblems(problems)

    def check_documentation(self, where, element, comments, problems, is_block=False):
        """Compare an element with the comments that protoc attaches to it.

        The comment above an element (or else the one behind it) is its
        description. The other comments are kept as comments. A message, an enum
        or a oneof can have more comments than these: protoc does not attach the
        comments at the end of a block to anything, and the schema keeps them.
        """
        leading = normalize(comments["leading"])
        trailing = normalize(comments["trailing"])
        description = normalize(element.description)
        if description != (leading or trailing):
            problems.append(f"{where}: description {description!r}, expected {leading or trailing!r}")
        expected = [normalize(c) for c in comments["detached"]]
        if leading and trailing:
            expected.append(trailing)
        expected = [c for c in expected if c]
        actual = [normalize(c) for c in element.comments]
        if not is_block and sorted(actual) != sorted(expected):
            problems.append(f"{where}: comments {actual}, expected {expected}")
        if set(expected) - set(actual):
            problems.append(f"{where}: comments {sorted(set(expected) - set(actual))} are missing")

    def test_documentation(self):
        """Comments in the protobuf files are descriptions in the schema."""
        problems = []
        for name, message in self.messages.items():
            class_name = self.class_names[name]
            definition = self.classes[class_name]
            self.check_documentation(class_name, definition, message["comments"], problems, is_block=True)
            for field in message["fields"]:
                where = f"{class_name}.{field['json_name']}"
                slot = self.sv.induced_slot(field["json_name"], class_name)
                self.check_documentation(where, slot, field["comments"], problems)
            rules = {annotation(rule, "oneof"): rule for rule in definition.rules}
            for oneof in message["oneofs"]:
                where = f"{class_name} oneof {oneof['name']}"
                self.check_documentation(
                    where, rules[oneof["name"]], oneof["comments"], problems, is_block=True
                )
        all_enums = self.sv.all_enums()
        for enum in self.enums.values():
            definition = all_enums[enum["name"]]
            self.check_documentation(enum["name"], definition, enum["comments"], problems, is_block=True)
            for value in enum["values"]:
                where = f"{enum['name']}.{value['name']}"
                pv = definition.permissible_values[value["name"]]
                self.check_documentation(where, pv, value["comments"], problems)
        self.assertNoProblems(problems)


if __name__ == "__main__":
    unittest.main()
