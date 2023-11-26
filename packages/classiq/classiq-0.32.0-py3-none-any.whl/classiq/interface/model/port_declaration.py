from typing import Any, Mapping

import pydantic

from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.quantum_variable_declaration import (
    QuantumVariableDeclaration,
)

from classiq.exceptions import ClassiqValueError


class PortDeclaration(QuantumVariableDeclaration):
    direction: PortDeclarationDirection

    @pydantic.validator("direction")
    def _direction_validator(
        cls, direction: PortDeclarationDirection, values: Mapping[str, Any]
    ) -> PortDeclarationDirection:
        if direction is PortDeclarationDirection.Output:
            quantum_type = values.get("quantum_type")
            if quantum_type is None:
                raise ClassiqValueError("Port declaration is missing a type")

        return direction
