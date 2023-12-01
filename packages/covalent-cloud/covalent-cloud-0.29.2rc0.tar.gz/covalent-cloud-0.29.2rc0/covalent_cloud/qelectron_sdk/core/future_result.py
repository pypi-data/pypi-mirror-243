# Copyright 2023 Agnostiq Inc.

"""
Define the future result, an object that enables async execution of QElectron QNodes.
"""

import warnings
from typing import Any, Optional

import pennylane as qml
from pennylane.tape import QuantumTape

from ..middleware.core import middleware
from .qresult_utils import re_execute


class QNodeFutureResult:
    """
    A class that stores the `batch_id` of a batch of circuits submitted to the
    middleware. The `result` method can then be called to retrieve the results.

    Attributes:
        device: The Pennylane device used by the original QNode.
        interface: The interface of the original QNode.
        diff_method: The differentiation method of the original QNode.
        qfunc_output: The return value (measurement definition) of the original QNode.
    """

    def __init__(
        self,
        batch_id: str,
        interface: str,
        original_qnode: qml.QNode,
        original_tape: QuantumTape,
    ):
        """
        Initialize a `QNodeFutureResult` instance.

        Args:
            batch_id: A UUID that identifies a batch of circuits submitted to
                the middleware.
        """
        self.batch_id = batch_id
        self.interface = interface  # NOT necessarily the original QNode's interface

        # Required for batch_transforms and correct output typing.
        self.device = original_qnode.device
        self.qnode = original_qnode
        self.tape = original_tape

        self.args: tuple = ()
        self.kwargs: dict = {}

        self._temp_result = None
        self._result = None

    def __call__(self, args, kwargs, temp_result: Any) -> "QNodeFutureResult":
        """
        Store the arguments and keyword arguments of the original QNode call.
        """
        self.args = args
        self.kwargs = kwargs

        # Use this to preserve gradients where possible.
        self._temp_result = temp_result

        return self

    def result(self) -> Any:
        """
        Retrieve the results for the given `batch_id` from middleware. This method
        is blocking until the results are available.

        Returns:
            The results of the circuit execution.
        """

        if self._result is None:
            # Get raw results from the middleware.
            results = middleware.get_results(self.batch_id)

            # Required correct gradient post-processing in some cases.
            if self.interface == "autograd":
                self._result = results
                res = results[0]

            if self.interface != "numpy":
                interface = self.interface  # re-execute with any non-numpy interface
                res = results[0]  # re-execute with this result

            elif self.qnode.interface is None:
                interface = None
                res = results[0]

            elif self.qnode.interface == "auto":
                interface = "auto"
                res = results

            else:
                # Skip re-execution.
                self._result = results
                return results

            args, kwargs = self.args, self.kwargs
            result = re_execute(res, self.qnode, self.tape)(interface, *args, **kwargs)
            self._result = self._result_with_grad(result, interface)

        return self._result

    def _result_with_grad(
        self,
        result: Any,
        interface: Optional[str]
    ) -> Any:
        """
        If possible, swap result data into the temporary result object
        to preserve gradients.
        """
        if self._temp_result is None:
            return result

        if interface == "torch":
            self._temp_result.data = result.data
            return self._temp_result

        warnings.warn(
            "Asynchronous QElectron calls do not yet preserve gradients for "
            f"the '{interface}' interface."
        )

        return result
