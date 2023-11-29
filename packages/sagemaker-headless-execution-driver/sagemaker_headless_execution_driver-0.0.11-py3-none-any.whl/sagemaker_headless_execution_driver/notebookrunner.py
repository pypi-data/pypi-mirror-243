# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import os
import json
import sys
import traceback
import papermill
from papermill.translators import (
    papermill_translators,
    PythonTranslator,
    ScalaTranslator,
)
from papermill.engines import papermill_engines
from .sm_engine import SageMakerNotebookClientEngine
import signal
import nbformat
from jupyter_client.kernelspec import KernelSpecManager


class PaperMillNotebookRunner:
    sm_engine_name = "sagemaker_engine"

    def __init__(self):
        self._register_for_sparkanalytics_image()
        signal.signal(signal.SIGINT, self.exit_handler)
        signal.signal(signal.SIGTERM, self.exit_handler)
        papermill_engines.register(
            PaperMillNotebookRunner.sm_engine_name, SageMakerNotebookClientEngine
        )

    def run_notebook(self):
        """
        Run the notebook based on the inputs specified by environment variables. The papermill is used to execute the notebook.
        """
        output_notebook = "dummy_path"
        try:
            # return key error when required env var is missing.
            output_notebook = os.environ["SM_PAPERMILL_OUTPUT"]
            notebook_path = os.environ["SM_PAPERMILL_INPUT"]
            kernel_name = os.environ["SM_KERNEL_NAME"]
            params_path = os.environ["SM_PAPERMILL_PARAMS_PATH"]

            if not os.path.exists(notebook_path):
                raise FileNotFoundError(notebook_path)

            with open(params_path) as f:
                params = json.load(f)

            notebook_dir = os.path.dirname(notebook_path)
            notebook_file = os.path.basename(notebook_path)
            os.chdir(notebook_dir)

            # if language is passed as None, papermill uses the one from notebook metadata
            # this is used to address the notebook without language metadata
            language = None
            if not NotebookExecutionLanguageUtils.has_language_info(notebook_path):
                language = NotebookExecutionLanguageUtils.get_language_from_kernel(
                    kernel_name
                )

            print(
                f"Use Kernel {kernel_name} to execute {notebook_file} with output to {output_notebook}. Params: {params}"
            )

            papermill.execute_notebook(
                notebook_file,
                output_notebook,
                parameters=params,
                kernel_name=kernel_name,
                language=language,
                engine_name=PaperMillNotebookRunner.sm_engine_name,
            )
            print("Execution complete")
        except Exception as e:
            trc = traceback.format_exc()
            error_msg = f"Exception during processing notebook: {str(e)}\n{trc}"
            print(
                error_msg,
                file=sys.stderr,
            )
            self._write_failure_info(error_msg)

            sys.exit(1)
        finally:
            if not os.path.exists(output_notebook):
                print("No output notebook was generated")
            else:
                print("Output notebook was generated")

    def _write_failure_info(self, error_msg):
        file = os.environ["SM_PAPERMILL_FAILURE_FILE"]
        with open(file, "a") as f:
            f.write("Error with executing notebook\n")
            f.write(error_msg)

    def _register_for_sparkanalytics_image(self):
        """
        PaperMill has list of supported kernels/languages pre-registered. The SageMaker SparkAnalytics has kernel
        names not supported by PaperMill by default. The custom kernel/language should be manually registered.
        """
        translatorMapping = {
            "conda-env-sm_glue_is-glue_pyspark": PythonTranslator,
            "conda-env-sm_glue_is-glue_spark": ScalaTranslator,
            "conda-env-sm_sparkmagic-pysparkkernel": PythonTranslator,
            "conda-env-sm_sparkmagic-sparkkernel": ScalaTranslator,
        }

        for kernel, translator in translatorMapping.items():
            papermill_translators.register(kernel, translator)

    def exit_handler(self, *args):
        print(
            "[exit_handler] Got signal to interrupt the papermill execution. Exit the papermill process."
        )
        self._write_failure_info("Notebook execution is interrupted.")
        if SageMakerNotebookClientEngine.notebook_client != None:
            SageMakerNotebookClientEngine.notebook_client.kc.shutdown()


class NotebookExecutionLanguageUtils:
    @classmethod
    def has_language_info(cls, input_notebook):
        """
        Check if the language_info.name exists in the metadata.
        """
        nb = nbformat.read(input_notebook, nbformat.NO_CONVERT)
        if (
            not nb.hasattr("metadata")
            or not nb.metadata.hasattr("language_info")
            or not nb.metadata.language_info.hasattr("name")
            or nb.metadata.language_info.name == ""
        ):
            return False
        else:
            return True

    @classmethod
    def get_language_from_kernel(cls, kernel):
        """
        Return the language from the kernel spec.
        :return: language from the kernel spec. If the no spec found, raise jupyter_client.kernelspec.NoSuchKernel error.
        """
        spec = KernelSpecManager().get_kernel_spec(kernel)
        return spec.language


if __name__ == "__main__":
    PaperMillNotebookRunner().run_notebook()
