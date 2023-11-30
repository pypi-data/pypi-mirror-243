# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This file defines the run utils.
"""

from typing import Union

from .constants import UNKNOWN_VALUE
from ..model_selector.constants import RunDetailsConstants


def calculate_per_node_process_count() -> Union[int, str]:
    """Calculate the process count from run properties."""
    try:
        from azureml.core import Run
        run_details = Run.get_context().get_details()
        total_process_count = run_details[
            RunDetailsConstants.RUN_DEFINITION][
            RunDetailsConstants.PYTORCH_DISTRIBUTION][
            RunDetailsConstants.PROCESS_COUNT]
        node_count = run_details[RunDetailsConstants.RUN_DEFINITION][RunDetailsConstants.NODE_COUNT]
        return total_process_count // node_count
    except Exception:
        return UNKNOWN_VALUE
