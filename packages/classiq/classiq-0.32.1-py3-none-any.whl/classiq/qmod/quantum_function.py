import functools
from typing import Any, Callable, Dict, List, Optional, Tuple, get_origin

from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.generator.model.constraints import Constraints
from classiq.interface.generator.model.preferences.preferences import Preferences
from classiq.interface.model.model import Model, SerializedModel
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)

from classiq.exceptions import ClassiqError
from classiq.qmod.declaration_inferrer import infer_func_decl
from classiq.qmod.model_state_container import ModelStateContainer
from classiq.qmod.qmod_parameter import QParam
from classiq.qmod.qmod_variable import QVar
from classiq.qmod.quantum_callable import QCallable
from classiq.qmod.quantum_expandable import QExpandable, QTerminalCallable
from classiq.qmod.utilities import mangle_keyword, unmangle_keyword


def _validate_no_gen_params(annotations: Dict[str, Any]) -> None:
    if not all(
        name == "return"
        or get_origin(annotation) in {QParam, QCallable}
        or QVar.from_type_hint(annotation) is not None
        for name, annotation in annotations.items()
    ):
        raise ClassiqError(f"{QFunc.__name__} with generative parameters not supported")


def _lookup_qfunc(name: str) -> Optional[QuantumFunctionDeclaration]:
    # FIXME: to be generalized to existing user-defined functions
    return QuantumFunctionDeclaration.BUILTIN_FUNCTION_DECLARATIONS.get(name)


def create_model(
    entry_point: "QFunc",
    constraints: Optional[Constraints] = None,
    execution_preferences: Optional[ExecutionPreferences] = None,
    preferences: Optional[Preferences] = None,
) -> SerializedModel:
    return entry_point.create_model(
        constraints, execution_preferences, preferences
    ).get_model()


class QFunc(QExpandable):
    def __init__(self, py_callable: Callable) -> None:
        _validate_no_gen_params(py_callable.__annotations__)
        super().__init__(py_callable)
        functools.update_wrapper(self, py_callable)

    @property
    def func_decl(self) -> QuantumFunctionDeclaration:
        return ModelStateContainer.NATIVE_DEFS.get(
            self._py_callable.__name__, infer_func_decl(self._py_callable)
        )

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        super().__call__(*args, **kwargs)
        self._add_native_func_def()

    def create_model(
        self,
        constraints: Optional[Constraints] = None,
        execution_preferences: Optional[ExecutionPreferences] = None,
        preferences: Optional[Preferences] = None,
    ) -> Model:
        ModelStateContainer.TYPE_DECLS = dict()
        ModelStateContainer.NATIVE_DEFS = dict()
        self._add_native_func_def()
        model_extra_settings: List[Tuple[str, Any]] = [
            ("constraints", constraints),
            ("execution_preferences", execution_preferences),
            ("preferences", preferences),
        ]
        return Model(
            functions=list(ModelStateContainer.NATIVE_DEFS.values()),
            types=list(ModelStateContainer.TYPE_DECLS.values()),
            **{key: value for key, value in model_extra_settings if value},
        )

    def _add_native_func_def(self) -> None:
        if self.func_decl.name in ModelStateContainer.NATIVE_DEFS:
            return
        self.expand()
        ModelStateContainer.NATIVE_DEFS[self.func_decl.name] = NativeFunctionDefinition(
            **self.func_decl.__dict__, local_handles=self.local_handles, body=self.body
        )


class ExternalQFunc(QTerminalCallable):
    def __init__(self, py_callable: Callable) -> None:
        decl = _lookup_qfunc(unmangle_keyword(py_callable.__name__))
        if decl is None:
            raise ValueError(f"Definition of {py_callable.__name__!r} not found")

        py_callable.__annotations__.pop("return", None)
        if py_callable.__annotations__.keys() != {
            mangle_keyword(arg.name) for arg in decl.get_positional_arg_decls()
        }:
            raise ValueError(
                f"Parameter type hints for {py_callable.__name__!r} do not match imported declaration"
            )
        super().__init__(decl)
        functools.update_wrapper(self, py_callable)
