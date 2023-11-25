from __future__ import annotations

import pathlib
import typing as t
import urllib.error
import urllib.parse

import jsonschema

from ..builtin_schemas import get_builtin_schema
from ..formats import FormatOptions, make_format_checker
from ..parsers import ParserSet
from ..utils import is_url_ish
from .errors import UnsupportedUrlScheme
from .readers import HttpSchemaReader, LocalSchemaReader, StdinSchemaReader
from .resolver import make_reference_registry


def _extend_with_default(
    validator_class: type[jsonschema.protocols.Validator],
) -> type[jsonschema.Validator]:
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults_then_validate(
        validator: jsonschema.Validator,
        properties: dict[str, dict[str, t.Any]],
        instance: dict[str, t.Any],
        schema: dict[str, t.Any],
    ) -> t.Iterator[jsonschema.ValidationError]:
        for property_name, subschema in properties.items():
            if "default" in subschema and property_name not in instance:
                instance[property_name] = subschema["default"]

        yield from validate_properties(
            validator,
            properties,
            instance,
            schema,
        )

    return jsonschema.validators.extend(
        validator_class,
        {"properties": set_defaults_then_validate},
    )


class SchemaLoaderBase:
    def get_validator(
        self,
        path: pathlib.Path | str,
        instance_doc: dict[str, t.Any],
        format_opts: FormatOptions,
        fill_defaults: bool,
    ) -> jsonschema.protocols.Validator:
        raise NotImplementedError


class SchemaLoader(SchemaLoaderBase):
    validator_class: type[jsonschema.protocols.Validator] | None = None

    def __init__(
        self,
        schemafile: str,
        cache_filename: str | None = None,
        disable_cache: bool = False,
        base_uri: str | None = None,
        validator_class: type[jsonschema.protocols.Validator] | None = None,
    ) -> None:
        # record input parameters (these are not to be modified)
        self.schemafile = schemafile
        self.cache_filename = cache_filename
        self.disable_cache = disable_cache
        self.base_uri = base_uri
        self.validator_class = validator_class

        # if the schema location is a URL, which may include a file:// URL, parse it
        self.url_info = None
        if is_url_ish(self.schemafile):
            self.url_info = urllib.parse.urlparse(self.schemafile)

        # setup a parser collection
        self._parsers = ParserSet()

        # setup a schema reader lazily, when needed
        self._reader: LocalSchemaReader | HttpSchemaReader | StdinSchemaReader | None = (
            None
        )

    @property
    def reader(self) -> LocalSchemaReader | HttpSchemaReader | StdinSchemaReader:
        if self._reader is None:
            self._reader = self._get_schema_reader()
        return self._reader

    def _get_schema_reader(
        self,
    ) -> LocalSchemaReader | HttpSchemaReader | StdinSchemaReader:
        if self.schemafile == "-":
            return StdinSchemaReader()

        if self.url_info is None or self.url_info.scheme in ("file", ""):
            return LocalSchemaReader(self.schemafile)

        if self.url_info.scheme in ("http", "https"):
            return HttpSchemaReader(
                self.schemafile,
                self.cache_filename,
                self.disable_cache,
            )
        else:
            raise UnsupportedUrlScheme(
                "check-jsonschema only supports http, https, and local files. "
                f"detected parsed URL had an unrecognized scheme: {self.url_info}"
            )

    def get_schema_retrieval_uri(self) -> str | None:
        return self.reader.get_retrieval_uri()

    def get_schema(self) -> dict[str, t.Any]:
        data = self.reader.read_schema()
        if self.base_uri is not None:
            data["$id"] = self.base_uri
        return data

    def get_validator(
        self,
        path: pathlib.Path | str,
        instance_doc: dict[str, t.Any],
        format_opts: FormatOptions,
        fill_defaults: bool,
    ) -> jsonschema.protocols.Validator:
        retrieval_uri = self.get_schema_retrieval_uri()
        schema = self.get_schema()

        schema_dialect = schema.get("$schema")

        # format checker (which may be None)
        format_checker = make_format_checker(format_opts, schema_dialect)

        # reference resolution
        # with support for YAML, TOML, and other formats from the parsers
        reference_registry = make_reference_registry(
            self._parsers, retrieval_uri, schema
        )

        if self.validator_class is None:
            # get the correct validator class and check the schema under its metaschema
            validator_cls = jsonschema.validators.validator_for(schema)
            validator_cls.check_schema(schema)
        else:
            # for a user-provided validator class, don't check_schema
            # on the grounds that it might *not* be valid but the user wants to use
            # their custom validator anyway
            #
            # in fact, there's no real guarantee that a user-provided
            # validator_class properly conforms to the jsonschema.Validator protocol
            # we *hope* that it does, but we can't be fully sure
            validator_cls = self.validator_class

        # extend the validator class with default-filling behavior if appropriate
        if fill_defaults:
            validator_cls = _extend_with_default(validator_cls)

        # now that we know it's safe to try to create the validator instance, do it
        validator = validator_cls(
            schema,
            registry=reference_registry,
            format_checker=format_checker,
        )
        return t.cast(jsonschema.protocols.Validator, validator)


class BuiltinSchemaLoader(SchemaLoader):
    def __init__(self, schema_name: str, base_uri: str | None = None) -> None:
        self.schema_name = schema_name
        self.base_uri = base_uri
        self._parsers = ParserSet()

    def get_schema_retrieval_uri(self) -> str | None:
        return None

    def get_schema(self) -> dict[str, t.Any]:
        data = get_builtin_schema(self.schema_name)
        if self.base_uri is not None:
            data["$id"] = self.base_uri
        return data


class MetaSchemaLoader(SchemaLoaderBase):
    def __init__(self, base_uri: str | None = None) -> None:
        if base_uri is not None:
            raise NotImplementedError(
                "'--base-uri' was used with '--metaschema'. "
                "This combination is not supported."
            )

    def get_validator(
        self,
        path: pathlib.Path | str,
        instance_doc: dict[str, t.Any],
        format_opts: FormatOptions,
        fill_defaults: bool,
    ) -> jsonschema.protocols.Validator:
        schema_validator = jsonschema.validators.validator_for(instance_doc)
        meta_validator_class = jsonschema.validators.validator_for(
            schema_validator.META_SCHEMA, default=schema_validator
        )

        # format checker (which may be None)
        meta_schema_dialect = schema_validator.META_SCHEMA.get("$schema")
        format_checker = make_format_checker(format_opts, meta_schema_dialect)

        meta_validator = meta_validator_class(
            schema_validator.META_SCHEMA, format_checker=format_checker
        )
        return meta_validator
