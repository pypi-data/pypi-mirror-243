import copy
import schema

from enum import Enum
from typing import Self, Hashable, MutableSet, MutableSequence, MutableMapping

__all__ = ['Schema',
           'And', 'Or', 'Optional',
           'Regex', 'Use', 'Const',
           'SchemaError', 'SchemaWrongKeyError', 'SchemaMissingKeyError',
           'SchemaUnexpectedTypeError', 'SchemaForbiddenKeyError', 'SchemaOnlyOneAllowedError',
]


def make_hashable(x):
    if isinstance(x, tuple):
        return tuple([make_hashable(y) for y in x])
    elif isinstance(x, MutableSet):
        return frozenset([make_hashable(y) for y in x])
    elif isinstance(x, MutableSequence):
        return tuple([make_hashable(y) for y in x])
    elif isinstance(x, MutableMapping):
        return frozenset({y: make_hashable(z) for y, z in x.items()})
    else:
        return x


class Regex(schema.Regex):
    pass


class Use(schema.Use):
    pass


class SchemaError(schema.SchemaError):
    pass


class SchemaWrongKeyError(schema.SchemaWrongKeyError):
    pass


class SchemaOnlyOneAllowedError(schema.SchemaOnlyOneAllowedError):
    pass


class SchemaMissingKeyError(schema.SchemaMissingKeyError):
    pass


class SchemaForbiddenKeyError(schema.SchemaForbiddenKeyError):
    pass


class SchemaUnexpectedTypeError(schema.SchemaUnexpectedTypeError):
    pass


class Or(schema.Or):
    def __eq__(self, other: Self) -> bool:
        """ Equality comparison: Ors are equal iff their schemas are equal """
        if not isinstance(other, Or):
            return NotImplemented
        else:
            mine = set(make_hashable(self._args))
            their = set(make_hashable(other._args))
            return mine == their


class And(schema.And):
    def __eq__(self, other: Self) -> bool:
        """ Equality comparison: Ands are equal iff their schemas are equal """
        if not isinstance(other, And):
            return NotImplemented
        else:
            mine = set(make_hashable(self._args))
            their = set(make_hashable(other._args))
            return mine == their and self.__class__ == other.__class__


class Optional(schema.Optional):
    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Optional):
            return NotImplemented
        return self._schema == other._schema

    def __hash__(self):
        return super().__hash__()


class Const(schema.Const):
    def __eq__(self, other) -> bool:
        return self.schema == other.schema


class Schema(schema.Schema):
    def __eq__(self, other: Self) -> bool:
        """
            Determine whether two schemas are equal or not.
            Caveat: equality tests are difficult in Python and difficult in general for many objects.
            For instance (lambda x: x < 3) != (lambda x: x < 3) and there is no easy way around it.
        """
        if isinstance(other, Schema):
            return self._schema == other._schema
        else:
            # If our schema is equal to the other object, we are good to go.
            return self._schema == other

    def __or__(self, other: Self) -> Self:
        sch = copy.deepcopy(self)
        sch |= other
        return sch

    def __ior__(self, other: Self):
        assert isinstance(other, Schema), "Can only merge a Schema with another Schema"

        if isinstance(self.schema, dict) and isinstance(other.schema, dict):
            for key in other.schema:
                if key in self.schema:
                    if isinstance(self.schema[key], dict) and isinstance(other.schema[key], dict):
                        self.schema[key] |= other.schema[key]
                    # two Schemas can be merged recursively
                    elif isinstance(self.schema[key], Schema) and isinstance(other.schema[key], Schema):
                        self.schema[key] |= other.schema[key]
                    # otherwise use Or of the two subschemas
                    else:
                        self.schema[key] = Or(self.schema[key], other.schema[key])
                else:
                    self.schema[key] = other.schema[key]
        else:
            if self.schema == other.schema:
                # two identical schemas are replaced by one
                return self
            else:
                # two different schemas are simply Or-ed
                self._schema = Or(self.schema, other.schema)

        return self

