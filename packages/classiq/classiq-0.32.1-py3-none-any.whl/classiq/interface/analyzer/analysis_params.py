from typing import Dict, List, Optional

import numpy
import pydantic
from pydantic import Field

from classiq.interface.backend.quantum_backend_providers import AnalyzerProviderVendor
from classiq.interface.chemistry.ground_state_problem import MoleculeProblem
from classiq.interface.executor.optimizer_preferences import OptimizerPreferences
from classiq.interface.generator.hardware.hardware_data import SynthesisHardwareData
from classiq.interface.generator.model.preferences.preferences import Preferences
from classiq.interface.hardware import Provider
from classiq.interface.helpers.custom_pydantic_types import PydanticNonEmptyString

MAX_KB_OF_FILE = 500
MAX_FILE_LENGTH = MAX_KB_OF_FILE * 1024


class AnalysisParams(pydantic.BaseModel):
    qasm: PydanticNonEmptyString = Field(..., max_length=MAX_FILE_LENGTH)


class HardwareListParams(pydantic.BaseModel):
    devices: Optional[List[PydanticNonEmptyString]] = pydantic.Field(
        default=None, description="Devices"
    )
    providers: List[Provider]
    from_ide: bool = Field(default=False)

    @pydantic.validator("providers", always=True)
    def set_default_providers(
        cls, providers: Optional[List[AnalyzerProviderVendor]]
    ) -> List[AnalyzerProviderVendor]:
        if providers is None:
            providers = list(AnalyzerProviderVendor)
        return providers


class AnalysisOptionalDevicesParams(HardwareListParams):
    qubit_count: int = pydantic.Field(
        default=..., description="number of qubits in the data"
    )


class AnalysisHardwareTranspilationParams(pydantic.BaseModel):
    hardware_data: Optional[SynthesisHardwareData]
    model_preferences: Preferences


class AnalysisHardwareListParams(AnalysisParams, HardwareListParams):
    transpilation_params: AnalysisHardwareTranspilationParams


class ResourceEstimatorParams(pydantic.BaseModel):
    circuit_id: str
    error_budget: float
    physical_error_rate: float


class HardwareParams(pydantic.BaseModel):
    device: PydanticNonEmptyString = pydantic.Field(default=None, description="Devices")
    provider: AnalyzerProviderVendor


class AnalysisHardwareParams(AnalysisParams, HardwareParams):
    pass


class CircuitAnalysisHardwareParams(AnalysisParams):
    provider: Provider
    device: PydanticNonEmptyString


class AnalysisRBParams(pydantic.BaseModel):
    hardware: str
    counts: List[Dict[str, int]]
    num_clifford: List[int]


class ChemistryGenerationParams(pydantic.BaseModel):
    class Config:
        title = "Chemistry"

    molecule: MoleculeProblem = pydantic.Field(
        title="Molecule Problem",
        default=...,
        description="The molecule to generate the VQE ansatz for",
    )
    optimizer_preferences: OptimizerPreferences = pydantic.Field(
        default=..., description="Execution options for the classical Optimizer"
    )

    def initial_point(self) -> Optional[numpy.ndarray]:
        if self.optimizer_preferences.initial_point is not None:
            return numpy.ndarray(
                self.optimizer_preferences.initial_point  # type: ignore
            )
        else:
            return None
