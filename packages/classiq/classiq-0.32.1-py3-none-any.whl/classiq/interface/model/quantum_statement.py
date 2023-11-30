from typing import Mapping, Union

from pydantic import BaseModel

from classiq.interface.generator.function_params import IOName
from classiq.interface.model.handle_binding import HandleBinding, SlicedHandleBinding


class QuantumStatement(BaseModel):
    pass


class QuantumOperation(QuantumStatement):
    @property
    def wiring_inputs(self) -> Mapping[IOName, HandleBinding]:
        return dict()

    @property
    def wiring_inouts(
        self,
    ) -> Mapping[IOName, Union[SlicedHandleBinding, HandleBinding]]:
        return dict()

    @property
    def wiring_outputs(self) -> Mapping[IOName, HandleBinding]:
        return dict()
