# Copyright 2023 Agnostiq Inc.

"""
Define the custom Pennylane device that interacts with Covalent's Quantum Executors.
"""

from typing import Sequence

from pennylane import QubitDevice
from pennylane import numpy as np
from pennylane.devices.default_qubit import DefaultQubit

from ..middleware.core import middleware


class QEDevice(QubitDevice):

    """
    The purpose of this device is to redirect circuit execution through Covalent's
    Quantum Executors and to enable asynchronous execution.

    All QElectrons (which are QNodes) implicitly use this device.
    """

    name = "QEDevice"
    short_name = "qelectron_device"
    pennylane_requires = ">=0.31.0"
    version = "0.0.1"
    author = "aq"

    operations = DefaultQubit.operations
    observables = DefaultQubit.observables

    def __init__(
        self,
        wires=1,
        shots=None,
        *,
        r_dtype=np.float64,  # pylint: disable=no-member
        c_dtype=np.complex128,  # pylint: disable=no-member
        analytic=None,
        executors=None,
        qelectron_info=None,
    ):
        super().__init__(wires, shots, r_dtype=r_dtype, c_dtype=c_dtype, analytic=analytic)

        self._async_run = False
        self._batch_id = None
        self.executors = executors
        self.qelectron_info = qelectron_info

        # This will be set when the QNodeQE is called with args and kwargs.
        self.qnode_specs = None

    def batch_execute(self, circuits):
        """
        Submits circuits to QElectron middleware for execution on chosen backend(s).
        Retrieves and returns results, or returns a dummy result if running asynchronously.
        """

        # Async submit all circuits to middleware.
        batch_id = middleware.run_circuits_async(
            circuits, self.executors, self.qelectron_info, self.qnode_specs
        )

        # Relevant when `run_later` is used to run the circuit.
        # We will retrieve the result later using the future object and the batch_id.
        if self._async_run:
            self._batch_id = batch_id

            # Return a (recognizable) dummy result
            res = [self._asarray([-123.456] * c.output_dim) for c in circuits]
            if isinstance(self.qelectron_info.device_shots, Sequence):
                # Replicate the list for shot vector case.
                return [[res]] * len(self.qelectron_info.device_shots)
            return res

        # Otherwise, get the results from the middleware
        results = middleware.get_results(batch_id)

        return results

    def apply(self, *args, **kwargs):
        # Dummy implementation of abstractmethod on `QubitDevice`
        pass

    @classmethod
    def capabilities(cls):
        capabilities = super().capabilities().copy()
        capabilities.update(supports_broadcasting=True)
        return capabilities
