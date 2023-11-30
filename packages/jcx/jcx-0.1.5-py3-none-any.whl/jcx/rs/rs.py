from typing import Optional, TypeVar

from jcx.rs.proto import Cloned
from rustshed import Option, Null, Some

T = TypeVar("T")

C = TypeVar("C", bound=Cloned)


def rs_option(v: Optional[T]) -> Option[T]:
    """Optional => Option"""
    if v is None:
        return Null
    return Some(v)


def rs_option_cloned(v: Optional[C]) -> Option[C]:
    """Optional => Option & cloned"""
    if v is None:
        return Null
    return Some(v.clone())


def py_optional(v: Option[T]) -> Optional[T]:
    """Option => Optional"""
    if v.is_null():
        return None
    return v.unwrap()
