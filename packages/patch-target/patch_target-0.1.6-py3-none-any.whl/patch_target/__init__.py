import typing
from types import ModuleType
from typing import Protocol, NewType, Any, TypeGuard, Callable

PatchTarget = NewType("PatchTarget", str)
NamedCallable: typing.TypeAlias = Callable[[Any], Any]


class Named(Protocol):
    __name__: str


UnverifiedVisitorCandidate = Named | NamedCallable | str | ModuleType
VisitorCandidate = NewType("VisitorCandidate", str)
ModulePathElement = str


class InvalidPatchTargetException(Exception):
    pass


def is_named(value: Named | NamedCallable | str) -> TypeGuard[Named]:
    return hasattr(value, "__name__")


""" 
object_to_be_patched may need to be split into all possible permutations of the dot-delimited module path
example:

tests.dummy_module may import tests.dummy_other_module
using

import tests.dummy_other_module
OR
from tests import dummy_other_module

But in either case the __name__ attribute of tests.dummy_other_module
will still be tests.dummy_other_module 

but only one of those two will pass the hasattr check on the host module.

HostModule -> UnverifiedVisitorCandidate -> Maybe PatchTarget

process_unverified_candidate :: UnverifiedVisitorCandidate -> Generator[VisitorCandidate, TypeError, None]
permute_module_candidate :: ModuleType -> List VisitorCandidate


process_unverified_candidate candidate =
    case candidate of
        -> ModuleType c = Gen (permute_module_candidate c)
        -> Named c = Gen c.name
        -> String(c) = Gen c
        -> raise TypeError
        

permute_module_candidate c = 
    path_items = split c.name "."
    

get_visitor_candidates_from_path_element_list :: List PathElement -> List VisitorCandidate

example module_path: 
    path.to.my.cool.submodule.yay
path_element list:
    [path, to, my, cool, submodule, yay]
output_visitor_candidates_list:
    [path.to.my.cool.submodule.yay, to.my.cool.submodule.yay, my.cool.submodule.yay, cool.submodule.yay, submodule.yay, yay]

"""


def get_visitor_candidates_from_path_element_list(
    module_path_elements: list[ModulePathElement],
) -> list[VisitorCandidate]:
    candidates = []
    for i in range(len(module_path_elements)):
        candidates.append(VisitorCandidate(".".join(module_path_elements[i:])))
    return candidates


def process_unverified_candidate(
    candidate: UnverifiedVisitorCandidate,
) -> typing.Generator[VisitorCandidate, TypeError, None]:
    match candidate:
        case str():
            for c in [candidate]:
                yield c
        case c if isinstance(c, ModuleType):
            for candidate in get_visitor_candidates_from_path_element_list(
                candidate.__name__.split(".")
            ):
                yield candidate
        case candidate if is_named(candidate):
            for c in [candidate.__name__]:
                yield c
        case _:
            raise TypeError


def patch_target(
    host_module: ModuleType, object_to_be_patched: UnverifiedVisitorCandidate
) -> PatchTarget:
    for name in process_unverified_candidate(object_to_be_patched):
        if hasattr(host_module, name):
            return PatchTarget(f"{host_module.__name__}.{name}")

    name_of_visitor = getattr(object_to_be_patched, "__name__", object_to_be_patched)
    raise InvalidPatchTargetException(
        f"'{name_of_visitor}' not found within {host_module.__name__}"
    )


__all__ = ["patch_target"]
