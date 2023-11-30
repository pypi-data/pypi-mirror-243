import abc
from contextlib import contextmanager
from typing import (
    TYPE_CHECKING,
    Any,
    ForwardRef,
    Generic,
    Literal,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

from sympy import Basic, Symbol
from sympy.printing.pycode import PythonCodePrinter
from typing_extensions import Annotated, ParamSpec, _AnnotatedAlias

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.handle_binding import HandleBinding, SlicedHandleBinding
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_expressions.amplitude_loading_operation import (
    AmplitudeLoadingOperation,
)
from classiq.interface.model.quantum_expressions.arithmetic_operation import (
    ArithmeticOperation,
)
from classiq.interface.model.quantum_type import (
    QuantumBit,
    QuantumBitvector,
    QuantumFixedReal,
    QuantumInteger,
    QuantumType,
)

from classiq.exceptions import ClassiqValueError
from classiq.qmod.qmod_parameter import ArrayBase, QParam, QParamScalar
from classiq.qmod.quantum_callable import QCallable

ILLEGAL_SLICING_STEP_MSG = "Slicing with a step of a quantum variable is not supported"
SLICE_OUT_OF_BOUNDS_MSG = "Slice end index out of bounds"


class FixedPythonCodePrinter(PythonCodePrinter):  # 'xor' is not supported in base class
    _operators = {**PythonCodePrinter._operators, **{"xor": "^"}}
    _default_settings = {
        **PythonCodePrinter._default_settings,
        "fully_qualified_modules": False,
    }


def _python_expr(expr: Basic) -> str:
    return FixedPythonCodePrinter().doprint(expr)


def _is_input_output_typehint(type_hint: Any) -> bool:
    return isinstance(type_hint, _AnnotatedAlias) and isinstance(
        type_hint.__metadata__[0], PortDeclarationDirection
    )


def get_type_hint_expr(type_hint: Any) -> str:
    if isinstance(type_hint, ForwardRef):  # expression in string literal
        return str(type_hint.__forward_arg__)
    if get_origin(type_hint) == Literal:  # explicit numeric literal
        return str(get_args(type_hint)[0])
    else:
        return str(type_hint)  # implicit numeric literal


@contextmanager
def _no_current_expandable():
    current_expandable = QCallable.CURRENT_EXPANDABLE
    QCallable.CURRENT_EXPANDABLE = None
    try:
        yield
    finally:
        QCallable.CURRENT_EXPANDABLE = current_expandable


class QVar:
    def __init__(self, name: str) -> None:
        self._name = name
        if QCallable.CURRENT_EXPANDABLE is not None:
            QCallable.CURRENT_EXPANDABLE.add_local_handle(
                self._name, self.get_qmod_type()
            )

    @abc.abstractmethod
    def get_handle_binding(self) -> HandleBinding:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_qmod_type(self) -> QuantumType:
        raise NotImplementedError()

    @staticmethod
    def from_type_hint(type_hint: Any) -> Optional[Type["QVar"]]:
        if _is_input_output_typehint(type_hint):
            return QVar.from_type_hint(type_hint.__args__[0])
        type_ = get_origin(type_hint) or type_hint
        if issubclass(type_, QVar):
            return type_
        return None

    @classmethod
    @abc.abstractmethod
    def to_qmod_quantum_type(cls, type_hint: Any) -> QuantumType:
        raise NotImplementedError()

    @classmethod
    def port_direction(cls, type_hint: Any) -> PortDeclarationDirection:
        if _is_input_output_typehint(type_hint):
            assert len(type_hint.__metadata__) >= 1
            return type_hint.__metadata__[0]
        assert type_hint == cls or get_origin(type_hint) == cls
        return PortDeclarationDirection.Inout


_Q = TypeVar("_Q", bound=QVar)
Output = Annotated[_Q, PortDeclarationDirection.Output]
Input = Annotated[_Q, PortDeclarationDirection.Input]


class QScalar(QVar, Symbol):
    def _insert_arith_operation(self, expr: Basic, inplace: bool) -> None:
        # Fixme: Arithmetic operations are not yet supported on slices (see CAD-12670)
        if TYPE_CHECKING:
            assert QCallable.CURRENT_EXPANDABLE is not None
        QCallable.CURRENT_EXPANDABLE.append_call_to_body(
            ArithmeticOperation(
                expr_str=_python_expr(expr),
                result_var=self.get_handle_binding(),
                inplace_result=inplace,
            )
        )

    def _insert_amplitude_loading(self, expr: Basic) -> None:
        if TYPE_CHECKING:
            assert QCallable.CURRENT_EXPANDABLE is not None
        QCallable.CURRENT_EXPANDABLE.append_call_to_body(
            AmplitudeLoadingOperation(
                expr_str=_python_expr(expr),
                result_var=self.get_handle_binding(),
            )
        )

    def get_handle_binding(self) -> HandleBinding:
        return HandleBinding(name=self._name)

    def __ior__(self, other: Basic) -> "QScalar":
        self._insert_arith_operation(other, False)
        return self

    def __ixor__(self, other: Basic) -> "QScalar":
        self._insert_arith_operation(other, True)
        return self

    def __imul__(self, other: Basic) -> "QScalar":
        self._insert_amplitude_loading(other)
        return self


class QBit(QScalar):
    @classmethod
    def to_qmod_quantum_type(cls, type_hint: Any) -> QuantumType:
        return QuantumBit()

    def get_qmod_type(self) -> QuantumType:
        return QuantumBit()


class QNum(QScalar):
    pass


_T = TypeVar("_T")


class QInt(Generic[_T], QNum):
    @classmethod
    def to_qmod_quantum_type(cls, type_hint: Any) -> QuantumType:
        size_expr: Optional[Expression] = None
        if get_args(type_hint):
            size_expr = Expression(expr=get_type_hint_expr(get_args(type_hint)[0]))

        return QuantumInteger(size=size_expr)

    def get_qmod_type(self) -> QuantumType:
        return QuantumInteger()


_P = ParamSpec("_P")


class QFixed(Generic[_P], QNum):
    def __new__(cls, name: str, fraction_places: Union[int, QParam[int]]) -> "QFixed":
        instance = Symbol.__new__(cls, name)
        return instance

    def __init__(self, name: str, fraction_places: Union[int, QParam[int]]) -> None:
        self._fraction_places = fraction_places
        super().__init__(name)

    @classmethod
    def to_qmod_quantum_type(cls, type_hint: Any) -> QuantumType:
        fraction_places_str: str
        size_expr: Optional[Expression] = None
        if len(get_args(type_hint)[0]) == 2:
            size_expr = Expression(expr=get_type_hint_expr(get_args(type_hint)[0][0]))
            fraction_places_str = get_args(type_hint)[0][1]
        else:
            fraction_places_str = get_args(type_hint)[0][0]
        fraction_places = Expression(expr=get_type_hint_expr(fraction_places_str))
        return QuantumFixedReal(size=size_expr, fraction_places=fraction_places)

    def get_qmod_type(self) -> QuantumType:
        return QuantumFixedReal(
            fraction_places=Expression(expr=str(self._fraction_places))
        )


class QArray(ArrayBase[_P], QVar):
    def __init__(self, name: str, slice_: Optional[Tuple[int, int]] = None) -> None:
        super().__init__(name)
        self._slice = slice_

    def get_handle_binding(self) -> HandleBinding:
        if self._slice is None:
            return HandleBinding(name=self._name)
        return SlicedHandleBinding(
            name=self._name,
            start=Expression(expr=str(self._slice[0])),
            end=Expression(expr=str(self._slice[1])),
        )

    def __getitem__(self, key: Union[slice, int, QParam]) -> "QArray":
        offset = self._slice[0] if self._slice is not None else 0
        if isinstance(key, slice):
            if key.step is not None:
                raise NotImplementedError(ILLEGAL_SLICING_STEP_MSG)
            new_slice = (offset + key.start, offset + key.stop)
        else:
            new_slice = (offset + key, offset + key + 1)
        if self._slice is not None and new_slice[1] > self._slice[1]:
            raise ClassiqValueError(SLICE_OUT_OF_BOUNDS_MSG)
        # prevent addition to local handles, since this is used for slicing existing local handles
        with _no_current_expandable():
            return QArray(self._name, slice_=new_slice)

    def __len__(self) -> int:
        raise ValueError(
            "len(<var>) is not supported for quantum variables - use <var>.len() instead"
        )

    def len(self) -> "QParamScalar":
        return QParamScalar(name=f"len({self._name})")

    @classmethod
    def to_qmod_quantum_type(cls, type_hint: Any) -> QuantumType:
        length_expr: Optional[Expression] = None
        if len(get_args(type_hint)) == 2:
            length_expr = Expression(expr=get_type_hint_expr(get_args(type_hint)[1]))
        return QuantumBitvector(length=length_expr)

    def get_qmod_type(self) -> QuantumType:
        return QuantumBitvector()


def create_qvar_for_port_decl(port: PortDeclaration) -> QVar:
    # prevent addition to local handles, since this is used for ports
    with _no_current_expandable():
        if _is_single_qbit_vector(port):
            return QBit(port.name)
        elif isinstance(port.quantum_type, QuantumInteger):
            return QInt(port.name)
        elif isinstance(port.quantum_type, QuantumFixedReal):
            return QFixed(
                port.name,
                fraction_places=QParamScalar(port.quantum_type.fraction_places.expr),
            )
        return QArray(port.name)


def _is_single_qbit_vector(port: PortDeclaration) -> bool:
    return (
        isinstance(port.quantum_type, QuantumBit)
        or isinstance(port.quantum_type, QuantumBitvector)
        and port.size is not None
        and port.size.is_evaluated()
        and port.size.to_int_value() == 1
    )
