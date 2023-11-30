"""Analyzer module, implementing facilities for analyzing circuits using Classiq platform."""
import json
import webbrowser
from importlib.util import find_spec
from typing import Any, Dict, List, Optional, Sequence, Union
from urllib.parse import urljoin

import plotly.graph_objects as go

from classiq.interface.analyzer import analysis_params
from classiq.interface.backend.quantum_backend_providers import AnalyzerProviderVendor
from classiq.interface.generator import generated_circuit as generator_result

from classiq._internals import client
from classiq._internals.api_wrapper import ApiWrapper
from classiq._internals.async_utils import Asyncify
from classiq.analyzer.analyzer_utilities import (
    AnalyzerUtilities,
    DeviceName,
    HardwareGraphs,
    ProviderAvailableDevices,
    ProviderNameEnum,
)
from classiq.analyzer.url_utils import circuit_page_uri, client_ide_base_url
from classiq.exceptions import ClassiqAnalyzerError

find_ipywidgets = find_spec("ipywidgets")
VBox = Any

if find_ipywidgets is not None:
    from ipywidgets import VBox  # type: ignore[import, no-redef]

    from classiq._analyzer_extras.interactive_hardware import InteractiveHardware


class Analyzer(AnalyzerUtilities, metaclass=Asyncify):
    """Analyzer is the wrapper object for all analysis capabilities."""

    def __init__(self, circuit: generator_result.GeneratedCircuit) -> None:
        """Init self.

        Args:
            circuit (): The circuit to be analyzed.
        """
        if circuit.qasm is None:
            raise ClassiqAnalyzerError(
                "Analysis requires a circuit with valid QASM code"
            )
        self._params: analysis_params.AnalysisParams = analysis_params.AnalysisParams(
            qasm=circuit.qasm
        )
        self.circuit: generator_result.GeneratedCircuit = circuit
        self.hardware_comparison_table: Optional[go.Figure] = None
        self.available_devices: ProviderAvailableDevices = dict()
        self.hardware_graphs: HardwareGraphs = dict()

        self.transpilation_params = analysis_params.AnalysisHardwareTranspilationParams(
            hardware_data=self.circuit.hardware_data,
            model_preferences=self.circuit.model.preferences,
        )

    async def analyzer_app_async(self) -> None:
        """Opens the analyzer app with synthesis interactive results.

        Returns:
            None.
        """
        result = await ApiWrapper.call_analyzer_app(self.circuit)
        webbrowser.open_new_tab(
            urljoin(
                client_ide_base_url(),
                circuit_page_uri(
                    circuit_id=result.id, circuit_version=self.circuit.version
                ),
            )
        )

    async def get_available_devices_async(
        self, providers: Optional[List[ProviderNameEnum]] = None
    ) -> Dict[ProviderNameEnum, List[DeviceName]]:
        """Returns dict of the available devices by the providers. only devices
        with sufficient number of qubits are returns

        Args: providers (): List of providers (string or `AnalyzerProviderVendor`).
        if None, the table include all the available hardware.

        Returns:
            available devices (): dict of the available devices (Dict[str,List[str]]).
        """
        if providers is None:
            providers = list(AnalyzerProviderVendor)
        await self.request_available_devices_async(providers=providers)
        return {
            provider: self._filter_devices_by_qubits_count(provider)
            for provider in providers
        }

    async def plot_hardware_connectivity_async(
        self,
        provider: Optional[ProviderNameEnum] = None,
        device: Optional[DeviceName] = None,
    ) -> VBox:
        """plot the hardware_connectivity graph. It is required to required  install the
        analyzer_sdk extra.

        Args:
            provider (): provider name (optional - string or `AnalyzerProviderVendor`).
            device (): device name (optional - string).
        Returns:
         hardware_connectivity_graph (): interactive graph.
        """

        self._validate_analyzer_extra()
        interactive_hardware = InteractiveHardware(
            circuit=self.circuit,
            params=self._params,
            available_devices=self.available_devices,
            hardware_graphs=self.hardware_graphs,
        )
        await interactive_hardware.enable_interactivity_async()
        if provider is not None:
            interactive_hardware.providers_combobox.value = provider
            if device is not None:
                interactive_hardware.devices_combobox.value = device

        return interactive_hardware.show_interactive_graph()

    async def get_hardware_comparison_table_async(
        self,
        providers: Optional[Sequence[Union[str, AnalyzerProviderVendor]]] = None,
        devices: Optional[List[str]] = None,
    ) -> None:
        """create a comparison table between the transpiled circuits result on different hardware.
        The  comparison table included the depth, multi qubit gates count,and total gates count of the circuits.

        Args: providers (): List of providers (string or `AnalyzerProviderVendor`). if None, the table include all
        the available hardware.
        devices (): List of devices (string). if None, the table include all the available devices of the selected
        providers.
        Returns: None.
        """
        if providers is None:
            providers = list(AnalyzerProviderVendor)
        params = analysis_params.AnalysisHardwareListParams(
            qasm=self._params.qasm,
            providers=providers,
            devices=devices,
            transpilation_params=self.transpilation_params,
        )
        result = await ApiWrapper.call_table_graphs_task(params=params)
        self.hardware_comparison_table = go.Figure(json.loads(result.details))

    async def plot_hardware_comparison_table_async(
        self,
        providers: Optional[List[Union[str, AnalyzerProviderVendor]]] = None,
        devices: Optional[List[str]] = None,
    ) -> None:
        """plot the comparison table. if it has not been created it, it first creates the table using all the
        available hardware.

        Returns:
            None.
        """
        await self._hardware_comparison_condition_async(
            providers=providers, devices=devices
        )
        self.hardware_comparison_table.show()  # type: ignore[union-attr]

    async def _hardware_comparison_condition_async(
        self,
        providers: Optional[Sequence[Union[str, AnalyzerProviderVendor]]] = None,
        devices: Optional[List[str]] = None,
    ) -> None:
        if (
            providers is not None
            or devices is not None
            or self.hardware_comparison_table is None
        ):
            await self.get_hardware_comparison_table_async(
                providers=providers, devices=devices
            )

    @staticmethod
    def _open_route(path: str) -> None:
        backend_uri = client.client().get_backend_uri()
        webbrowser.open_new_tab(f"{backend_uri}{path}")

    @staticmethod
    def _validate_analyzer_extra() -> None:
        if find_ipywidgets is None:
            raise ClassiqAnalyzerError(
                "To use this method, please install the `analyzer sdk`. Run the  \
                following line: - pip install classiq[analyzer_sdk]"
            )
