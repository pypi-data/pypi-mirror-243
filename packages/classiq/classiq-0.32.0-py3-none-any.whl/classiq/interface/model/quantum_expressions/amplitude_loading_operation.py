from typing import Dict, Mapping, Union

import pydantic

from classiq.interface.generator.amplitude_loading import (
    AMPLITUDE_IO_NAME,
    TARGET_OUTPUT_NAME,
)
from classiq.interface.generator.function_params import IOName
from classiq.interface.model.handle_binding import HandleBinding, SlicedHandleBinding
from classiq.interface.model.quantum_expressions.quantum_expression import (
    QuantumExpressionOperation,
)
from classiq.interface.model.quantum_type import (
    QuantumBit,
    QuantumFixedReal,
    QuantumType,
)

from classiq.exceptions import ClassiqValueError

MULTI_VARS_UNSUPPORTED_ERROR = (
    "Amplitude Loading with more than one input variable is unsupported."
)

VAR_DOMAIN_ILLEGAL = (
    "Amplitude Loading input variable should be a fixed-point number between 0 and 1"
)


class AmplitudeLoadingOperation(QuantumExpressionOperation):
    _result_type: QuantumType = pydantic.PrivateAttr(default_factory=QuantumBit)

    @property
    def wiring_inouts(
        self,
    ) -> Mapping[IOName, Union[SlicedHandleBinding, HandleBinding]]:
        assert len(self.var_handles) > 0
        return {AMPLITUDE_IO_NAME: self.var_handles[0]}

    def initialize_var_types(self, var_types: Dict[str, QuantumType]) -> None:
        if len(var_types) != 1:
            raise ClassiqValueError(MULTI_VARS_UNSUPPORTED_ERROR)
        var_type = var_types[self.var_handles[0].name]
        if not (
            isinstance(var_type, QuantumFixedReal)
            and var_type.fraction_places.to_int_value() == var_type.size_in_bits
        ):
            raise ClassiqValueError(VAR_DOMAIN_ILLEGAL)
        super().initialize_var_types(var_types)

    @classmethod
    def result_name(cls) -> str:
        return TARGET_OUTPUT_NAME
