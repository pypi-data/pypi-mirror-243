from typing import Dict, Mapping, Union

import pydantic

from classiq.interface.generator.arith.arithmetic import (
    ARITHMETIC_EXPRESSION_RESULT_NAME,
    compute_arithmetic_result_type,
)
from classiq.interface.generator.function_params import IOName
from classiq.interface.model.handle_binding import HandleBinding, SlicedHandleBinding
from classiq.interface.model.quantum_expressions.quantum_expression import (
    QuantumExpressionOperation,
)
from classiq.interface.model.quantum_type import QuantumType


class ArithmeticOperation(QuantumExpressionOperation):
    inplace_result: bool = pydantic.Field(
        description="Determines whether the result variable is initialized",
    )

    def initialize_var_types(self, var_types: Dict[str, QuantumType]) -> None:
        super().initialize_var_types(var_types)
        self._result_type = compute_arithmetic_result_type(self.expr_str, var_types)

    @property
    def wiring_inouts(
        self,
    ) -> Mapping[IOName, Union[SlicedHandleBinding, HandleBinding]]:
        inouts = dict(super().wiring_inouts)
        if self.inplace_result:
            inouts[self.result_name()] = self.result_var
        return inouts

    @property
    def wiring_outputs(self) -> Mapping[IOName, HandleBinding]:
        if self.inplace_result:
            return {}
        return super().wiring_outputs

    @classmethod
    def result_name(cls) -> str:
        return ARITHMETIC_EXPRESSION_RESULT_NAME
