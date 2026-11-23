"""Compile protobuf files with protoc and write what they define to a JSON file.

    python util/proto_inventory.py PROTO_ROOT OUT.json ENTRY.proto [ENTRY.proto ...]

PROTO_ROOT is the directory that protobuf imports are resolved against
(``src/main/proto`` of phenopacket-schema) and each ENTRY.proto is a path
relative to it. The entry files and everything they import are compiled.

The output lists every message and enum, including nested ones, by its fully
qualified name. For each field it has the number, the name, the JSON name,
the type, whether it is repeated or deprecated and the oneof it belongs to, as
well as the comments that protoc attaches to each element. This is the
reference that ``tests/test_schema`` compares the LinkML schema with, so that
the schema cannot drift from the release that it was generated from.

Requires ``grpcio-tools``, which is not a dependency of this project. It is
normally run with ``make descriptors``.
"""
import json
import os
import sys
import tempfile

import grpc_tools
from google.protobuf import descriptor_pb2
from grpc_tools import protoc

FIELD = descriptor_pb2.FieldDescriptorProto

SCALARS = {
    FIELD.TYPE_DOUBLE: "double",
    FIELD.TYPE_FLOAT: "float",
    FIELD.TYPE_INT64: "int64",
    FIELD.TYPE_UINT64: "uint64",
    FIELD.TYPE_INT32: "int32",
    FIELD.TYPE_FIXED64: "fixed64",
    FIELD.TYPE_FIXED32: "fixed32",
    FIELD.TYPE_BOOL: "bool",
    FIELD.TYPE_STRING: "string",
    FIELD.TYPE_BYTES: "bytes",
    FIELD.TYPE_UINT32: "uint32",
    FIELD.TYPE_SFIXED32: "sfixed32",
    FIELD.TYPE_SFIXED64: "sfixed64",
    FIELD.TYPE_SINT32: "sint32",
    FIELD.TYPE_SINT64: "sint64",
}

# Field numbers in descriptor.proto, used in the paths of SourceCodeInfo
FILE_MESSAGE, FILE_ENUM = 4, 5
MESSAGE_FIELD, MESSAGE_NESTED, MESSAGE_ENUM, MESSAGE_ONEOF = 2, 3, 4, 8
ENUM_VALUE = 2


def compile_descriptors(root, entries):
    """Run protoc on the entry files and return the FileDescriptorSet."""
    well_known_types = os.path.join(os.path.dirname(grpc_tools.__file__), "_proto")
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "descriptors.pb")
        # root is listed first, so that google/protobuf/*.proto files found there
        # are used in preference to the ones bundled with grpcio-tools
        status = protoc.main(
            [
                "protoc",
                f"-I{root}",
                f"-I{well_known_types}",
                "--include_imports",
                "--include_source_info",
                f"--descriptor_set_out={out}",
                *entries,
            ]
        )
        if status != 0:
            sys.exit(f"protoc failed with status {status}")
        descriptors = descriptor_pb2.FileDescriptorSet()
        with open(out, "rb") as stream:
            descriptors.ParseFromString(stream.read())
    return descriptors


def inventory(descriptors):
    """Summarize a FileDescriptorSet as plain dictionaries."""
    inv = {"files": {}, "messages": {}, "enums": {}}
    for file in descriptors.file:
        comments = {
            tuple(location.path): {
                "leading": location.leading_comments,
                "trailing": location.trailing_comments,
                "detached": list(location.leading_detached_comments),
            }
            for location in file.source_code_info.location
        }
        inv["files"][file.name] = {
            "package": file.package,
            "dependencies": list(file.dependency),
            "syntax": file.syntax,
            "messages": [],
            "enums": [],
        }

        def comments_at(path):
            return comments.get(tuple(path), {"leading": "", "trailing": "", "detached": []})

        def add_enum(enum, name, path, parent):
            inv["enums"][name] = {
                "file": file.name,
                "name": enum.name,
                "parent": parent,
                "comments": comments_at(path),
                "values": [
                    {
                        "name": value.name,
                        "number": value.number,
                        "deprecated": value.options.deprecated,
                        "comments": comments_at(path + [ENUM_VALUE, i]),
                    }
                    for i, value in enumerate(enum.value)
                ],
            }
            inv["files"][file.name]["enums"].append(name)

        def add_message(message, name, path, parent):
            # map<K, V> fields are declared by protoc as a nested *Entry message
            map_entries = {
                f".{name}.{nested.name}": nested
                for nested in message.nested_type
                if nested.options.map_entry
            }
            # a proto3 `optional` field is declared by protoc as a oneof of its own
            oneofs = {
                field.oneof_index
                for field in message.field
                if field.HasField("oneof_index") and not field.proto3_optional
            }
            fields = []
            for i, field in enumerate(message.field):
                record = {
                    "name": field.name,
                    "number": field.number,
                    "json_name": field.json_name,
                    "repeated": field.label == FIELD.LABEL_REPEATED,
                    "deprecated": field.options.deprecated,
                    "oneof": (
                        message.oneof_decl[field.oneof_index].name
                        if field.HasField("oneof_index") and field.oneof_index in oneofs
                        else None
                    ),
                    "comments": comments_at(path + [MESSAGE_FIELD, i]),
                }
                if field.type in SCALARS:
                    record["kind"], record["type"] = "scalar", SCALARS[field.type]
                elif field.type == FIELD.TYPE_ENUM:
                    record["kind"], record["type"] = "enum", field.type_name.lstrip(".")
                elif field.type_name in map_entries:
                    key, value = map_entries[field.type_name].field
                    record["kind"] = "map"
                    record["repeated"] = False
                    record["type"] = "map<%s, %s>" % (
                        SCALARS.get(key.type, key.type_name.lstrip(".")),
                        SCALARS.get(value.type, value.type_name.lstrip(".")),
                    )
                else:
                    record["kind"], record["type"] = "message", field.type_name.lstrip(".")
                fields.append(record)
            inv["messages"][name] = {
                "file": file.name,
                "name": message.name,
                "parent": parent,
                "comments": comments_at(path),
                "oneofs": [
                    {"name": oneof.name, "comments": comments_at(path + [MESSAGE_ONEOF, i])}
                    for i, oneof in enumerate(message.oneof_decl)
                    if i in oneofs
                ],
                "fields": fields,
            }
            inv["files"][file.name]["messages"].append(name)
            for i, nested in enumerate(message.nested_type):
                if not nested.options.map_entry:
                    add_message(nested, f"{name}.{nested.name}", path + [MESSAGE_NESTED, i], name)
            for i, enum in enumerate(message.enum_type):
                add_enum(enum, f"{name}.{enum.name}", path + [MESSAGE_ENUM, i], name)

        prefix = f"{file.package}." if file.package else ""
        for i, message in enumerate(file.message_type):
            add_message(message, prefix + message.name, [FILE_MESSAGE, i], None)
        for i, enum in enumerate(file.enum_type):
            add_enum(enum, prefix + enum.name, [FILE_ENUM, i], None)
    return inv


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    root, out, entries = sys.argv[1], sys.argv[2], sys.argv[3:]
    inv = inventory(compile_descriptors(root, entries))
    with open(out, "w") as stream:
        json.dump(inv, stream, indent=1, sort_keys=True)
        stream.write("\n")
    print(
        f"{out}: {len(inv['files'])} files, {len(inv['messages'])} messages, "
        f"{len(inv['enums'])} enums"
    )


if __name__ == "__main__":
    main()
