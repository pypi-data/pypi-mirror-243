from __future__ import annotations
from configparser import RawConfigParser
from typing import Iterable, TypeVar

T = TypeVar('T')


def get_iterable_element_type(iterable: Iterable, *possible_types: type) -> type|None:
    """
    Get the type of all elements of the iterable amongst the possible types given as argument.
    """
    if not possible_types:
        raise NotImplementedError() # TODO: requires more thinking
    
    remaining_types = list(possible_types)

    for element in iterable:
        types_to_remove = []

        for possible_type in remaining_types:
            if not issubclass(type(element), possible_type):
                types_to_remove.append(possible_type)

        for type_to_remove in types_to_remove:
            remaining_types.remove(type_to_remove)
    
    return remaining_types[0] if remaining_types else None


def is_iterable_of(iterable: Iterable, element_type: type|tuple[type]):
    for element in iterable:
        if not isinstance(element, element_type):
            return False
        
    return True


def to_bool(value, if_none: bool = None) -> bool:
    if isinstance(value, bool):
        return value

    elif value is None:
        if if_none is not None:
            return if_none
    
    elif isinstance(value, int):
        if value == 0:
            return False
        elif value == 1:
            return True
        
    elif isinstance(value, str):
        lower = value.lower()    
        if lower in RawConfigParser.BOOLEAN_STATES:
            return RawConfigParser.BOOLEAN_STATES[lower]
    
    raise ValueError('Not a boolean: %s' % value)


def get_leaf_classes(cls: type[T]) -> list[type[T]]:
    cls_list = []

    def recurse(cls: type):
        subclasses = cls.__subclasses__()
        if subclasses:
            for subcls in subclasses:
                recurse(subcls)
        else:
            cls_list.append(cls)

    recurse(cls)
    return cls_list