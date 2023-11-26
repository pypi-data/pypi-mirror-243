from typing import Any, Dict, Literal, Optional, Union

import pydantic
from pydantic import Extra

from classiq.interface.generator.arith.register_user_input import (
    RegisterArithmeticInfo,
    RegisterUserInput,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.helpers.hashable_pydantic_base_model import (
    HashablePydanticBaseModel,
)
from classiq.interface.helpers.pydantic_model_helpers import values_with_discriminator

from classiq.exceptions import ClassiqValueError


class QuantumType(HashablePydanticBaseModel):
    class Config:
        extra = Extra.forbid

    _size_in_bits: Optional[int] = pydantic.PrivateAttr(default=None)

    def _update_size_in_bits_from_declaration(self) -> None:
        pass

    @property
    def size_in_bits(self) -> int:
        self._update_size_in_bits_from_declaration()
        if self._size_in_bits is None:
            raise ClassiqValueError("Trying to retrieve unknown size of quantum type")
        return self._size_in_bits

    @property
    def has_size_in_bits(self) -> bool:
        self._update_size_in_bits_from_declaration()
        return self._size_in_bits is not None

    def set_size_in_bits(self, val: int) -> None:
        self._size_in_bits = val


class QuantumBit(QuantumType):
    kind: Literal["qbit"]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._size_in_bits = 1

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "qbit")


class QuantumArray(QuantumType):
    length: Optional[Expression]


class QuantumBitvector(QuantumArray):
    kind: Literal["qvec"]

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "qvec")

    def _update_size_in_bits_from_declaration(self) -> None:
        if self.length is not None and self.length.is_evaluated():
            self._size_in_bits = self.length.to_int_value()


class QuantumNumeric(QuantumType):
    size: Optional[Expression] = pydantic.Field()

    _is_signed: bool = pydantic.PrivateAttr(default=False)

    @property
    def size_in_bits_expr(self) -> Optional[Expression]:
        return self.size

    @property
    def is_signed(self) -> bool:
        return self._is_signed

    def set_signed(self, val: bool) -> None:
        self._is_signed = val

    def _update_size_in_bits_from_declaration(self) -> None:
        if self.size is not None and self.size.is_evaluated():
            self._size_in_bits = self.size.to_int_value()


class QuantumInteger(QuantumNumeric):
    kind: Literal["qint"]

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "qint")


class QuantumFixedReal(QuantumNumeric):
    fraction_places: Expression = pydantic.Field()

    kind: Literal["qfixed"]

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "qfixed")


ConcreteQuantumType = Union[
    QuantumBit,
    QuantumBitvector,
    QuantumInteger,
    QuantumFixedReal,
]


def register_info_to_quantum_type(reg_info: RegisterArithmeticInfo) -> QuantumNumeric:
    result: QuantumNumeric
    if reg_info.fraction_places > 0:
        fraction_places = Expression(expr=f"{reg_info.fraction_places}")
        result = QuantumFixedReal(fraction_places=fraction_places)

    else:
        result = QuantumInteger()

    result.set_size_in_bits(reg_info.size)
    result.set_signed(reg_info.is_signed)
    return result


UNRESOLVED_SIZE = 1000


def quantum_var_to_register(name: str, qtype: QuantumType) -> RegisterUserInput:
    signed = qtype.is_signed if isinstance(qtype, QuantumNumeric) else False
    fraction_places = (
        qtype.fraction_places.to_int_value()
        if isinstance(qtype, QuantumFixedReal) and qtype.fraction_places.is_evaluated()
        else 0
    )
    return RegisterUserInput(
        name=name,
        size=qtype.size_in_bits if qtype.has_size_in_bits else UNRESOLVED_SIZE,
        is_signed=signed,
        fraction_places=fraction_places,
    )
