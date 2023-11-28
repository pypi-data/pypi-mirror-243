# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from papermill.engines import Engine
from papermill.utils import merge_kwargs, remove_args
from papermill.log import logger
from papermill.clientwrap import PapermillNotebookClient


class SageMakerNotebookClientEngine(Engine):
    """
    Introduce this custom engine to expose notebook client so that shutdown method of kernel client can be called for
    resource cleanup.This class is not needed when papermill supports exposing notebook client formally.
    """

    notebook_client = None

    @classmethod
    def execute_managed_notebook(
        cls,
        nb_man,
        kernel_name,
        log_output=False,
        stdout_file=None,
        stderr_file=None,
        start_timeout=60,
        execution_timeout=None,
        **kwargs,
    ):
        safe_kwargs = remove_args(["timeout", "startup_timeout"], **kwargs)

        # Nicely handle preprocessor arguments prioritizing values set by engine
        final_kwargs = merge_kwargs(
            safe_kwargs,
            timeout=execution_timeout if execution_timeout else kwargs.get("timeout"),
            startup_timeout=start_timeout,
            kernel_name=kernel_name,
            log=logger,
            log_output=log_output,
            stdout_file=stdout_file,
            stderr_file=stderr_file,
        )

        SageMakerNotebookClientEngine.notebook_client = PapermillNotebookClient(
            nb_man, **final_kwargs
        )
        return SageMakerNotebookClientEngine.notebook_client.execute()
