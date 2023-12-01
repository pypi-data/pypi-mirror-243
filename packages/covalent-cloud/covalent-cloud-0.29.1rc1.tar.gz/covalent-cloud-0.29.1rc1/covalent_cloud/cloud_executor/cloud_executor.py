# Copyright 2023 Agnostiq Inc.


import json
import re
from dataclasses import asdict
from datetime import timedelta
from typing import Optional, Union

import arrow
from pydantic import field_validator
from pydantic.dataclasses import dataclass
from pydantic.json import pydantic_encoder

executor_plugin_name = "cloud"

unit_multipliers = {"GB": 1024, "GiB": 954, "MB": 1}


@dataclass
class CloudExecutor:
    """
    CloudExecutor represents a configuration for executing a Covalent workflow on the Covalent Cloud.
    This class allows users to configure the resources (such as the number of CPUs, memory, GPUs, and GPU type) and the software environment for a Covalent workflow that will be executed on the Covalent Cloud. The time limit for the workflow execution can also be set.

    Attributes:

        num_cpus (int, optional): Number of CPUs to be used for the workflow. Defaults to 1.
        memory (int, optional): Amount of memory (in MB) to be used for the workflow. Defaults to 1024.
        num_gpus (int, optional): Number of GPUs to be used for the workflow. Defaults to 0.
        gpu_type (str, optional): Type of GPU to be used for the workflow. Defaults to an empty string.
        env (str, optional): Name of the software environment to be used for the workflow. Defaults to "default".
        time_limit (Union[int, timedelta], optional): Time limit for the workflow execution, in seconds or as a timedelta. Defaults to 1800s (30 mins). Alternatively can take human readable string in format 'in <number> <unit(s)>'

    Examples:

        # create a CloudExecutor with default resource configuration
        # executor = CloudExecutor()

        # create a custom CloudExecutor with specified resources and environment
        # executor = CloudExecutor(
        #     num_cpus=4,
        #     memory=2048,
        #     num_gpus=1,
        #     gpu_type="NVIDIA-Tesla-V100",
        #     env="my_custom_env",
        #     time_limit="in 30 minutes"  # 30 minutes
        # )

        import covalent as ct
        from covalent_cloud import CloudExecutor

        cloud_executor1 = CloudExecutor(num_cpus=1, memory=1024)
        cloud_executor2 = CloudExecutor(num_cpus=2, memory=2048)
        cloud_executor3 = CloudExecutor(num_cpus=1, memory=512)

        # Define manageable tasks as electrons with different cloud executors
        @ct.electron(executor=cloud_executor1)
        def add(x, y):
            return x + y

        @ct.electron(executor=cloud_executor2)
        def multiply(x, y):
            return x * y

        @ct.electron(executor=cloud_executor3)
        def divide(x, y):
            return x / y

        # Define the workflow as a lattice
        @ct.lattice
        def workflow(x, y):
            r1 = add(x, y)
            r2 = [multiply(r1, y) for _ in range(4)]
            r3 = [divide(x, value) for value in r2]
            return r3

        # Import the Covalent Cloud module
        import covalent_cloud as ctc

        # Dispatch the workflow to the Covalent Cloud
        dispatch_id = ctc.dispatch(workflow)(1, 2)
        result = ctc.get_result(dispatch_id, wait=True)
        print(result)
    """

    num_cpus: int = 1
    memory: Union[int, str] = 1024
    num_gpus: int = 0
    gpu_type: str = ""
    env: str = "default"
    time_limit: Union[int, timedelta, str] = 60 * 30
    volume_id: Optional[int] = None

    @property
    def short_name(self) -> str:
        """
        Property which returns the short name
        of the executor used by Covalent for identification.

        Args:
            None

        Returns:
            The short name of the executor

        """

        return executor_plugin_name

    # Validators:
    @field_validator("num_cpus", "memory", "time_limit")
    @classmethod
    def gt_than_zero(cls, v: int) -> int:
        """
        Validator which ensures that the value is greater than 0.

        Args:
            v: The value to validate

        Returns:
            The validated value

        """

        if v <= 0:
            raise ValueError(f"{v} must be greater than 0")
        return v

    @field_validator("memory", mode="before")
    @classmethod
    def memory_to_int(cls, v: Union[int, str]) -> int:
        """
        Validator which converts the memory value to an integer.

        Args:
            v: The value to validate

        Returns:
            The validated value

        """

        if isinstance(v, str):

            # grab the number and the unit
            match = re.match(r"(\d+)\s*([A-Za-z]+)", v)
            if match:
                memory_value, unit = match.groups()
            else:
                raise ValueError("Invalid memory string format")

            # convert to MB (int)
            try:
                memory_value = int(memory_value)
                unit = unit.strip()
                v = int(memory_value * unit_multipliers[unit])
            except ValueError as e:
                raise ValueError(f"Invalid memory value: {v}.") from e
        return v

    @field_validator("time_limit", mode="before")
    @classmethod
    def time_limit_to_int(cls, v: Union[int, timedelta, str]) -> int:
        """
        Validator which converts the time limit value to seconds.

        Args:
            v: The value to validate

        Returns:
            The validated value

        """

        if isinstance(v, timedelta):
            v = v.total_seconds()
        elif isinstance(v, str):
            try:
                now = arrow.utcnow()

                later = now.dehumanize(v)

                # arrow dehumanize method calculates time relative to another time
                difference = later - now

                v = difference.total_seconds()
            except Exception as e:
                raise ValueError(
                    f"Invalid time limit: {v}. Please provide a valid time limit with proper grammar."
                ) from e
        return v

    # Model methods:
    def to_json(self) -> str:
        """
        Return a JSON-serialized string representation of this object.

        Args:
            None

        Returns:
            The JSON-serialized string representation of this object.

        """

        return json.dumps(self, default=pydantic_encoder)

    def to_dict(self) -> dict:
        """
        Return a JSON-serializable dictionary representation of this object.

        Args:
            None

        Returns:
            The JSON-serializable dictionary representation of this object.
        """

        return {
            "type": str(self.__class__),
            "short_name": self.short_name,
            "attributes": asdict(self),
        }
