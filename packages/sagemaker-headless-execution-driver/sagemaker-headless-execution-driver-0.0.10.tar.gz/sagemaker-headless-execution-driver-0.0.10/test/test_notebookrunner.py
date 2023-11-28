# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import unittest
import io
import os
from unittest.mock import patch, MagicMock
from sagemaker_headless_execution_driver.notebookrunner import PaperMillNotebookRunner
import contextlib

papermill_execution_failure_info_file = "/tmp/test_failure"
env_happy_case = {
    "SM_PAPERMILL_OUTPUT": "/tmp/output.ipynb",
    "SM_PAPERMILL_INPUT": "/tmp/input.ipynb",
    "SM_KERNEL_NAME": "python3",
    "SM_PAPERMILL_PARAMS_PATH": "/tmp/abc.json",
    "SM_PAPERMILL_FAILURE_FILE": papermill_execution_failure_info_file,
}
env_missing_output = {
    "SM_PAPERMILL_INPUT": "input",
    "SM_KERNEL_NAME": "kernel",
    "SM_PAPERMILL_PARAMS_PATH": "params_path",
    "SM_PAPERMILL_FAILURE_FILE": papermill_execution_failure_info_file,
}

env_missing_input = {
    "SM_PAPERMILL_OUTPUT": "output",
    "SM_KERNEL_NAME": "kernel",
    "SM_PAPERMILL_PARAMS_PATH": "params_path",
    "SM_PAPERMILL_FAILURE_FILE": papermill_execution_failure_info_file,
}

env_missing_kernel = {
    "SM_PAPERMILL_OUTPUT": "output",
    "SM_PAPERMILL_INPUT": "input",
    "SM_PAPERMILL_PARAMS_PATH": "params_path",
    "SM_PAPERMILL_FAILURE_FILE": papermill_execution_failure_info_file,
}

env_missing_params_path = {
    "SM_PAPERMILL_OUTPUT": "output",
    "SM_PAPERMILL_INPUT": "input",
    "SM_KERNEL_NAME": "kernel",
    "SM_PAPERMILL_FAILURE_FILE": papermill_execution_failure_info_file,
}

env_non_existing_input_file = {
    "SM_PAPERMILL_OUTPUT": "/tmp/output.ipynb",
    "SM_PAPERMILL_INPUT": "/non-existing/folder/input.ipynb",
    "SM_KERNEL_NAME": "python3",
    "SM_PAPERMILL_PARAMS_PATH": "/tmp/abc.json",
    "SM_PAPERMILL_FAILURE_FILE": papermill_execution_failure_info_file,
}


class TestPaperMillNotebookRunner(unittest.TestCase):
    @unittest.mock.patch.dict(os.environ, env_missing_output)
    def test_env_missing_output(self):
        self.do_test_for_missing_env_key(env_key_name="SM_PAPERMILL_OUTPUT")

    @unittest.mock.patch.dict(os.environ, env_missing_input)
    def test_env_missing_input(self):
        self.do_test_for_missing_env_key(env_key_name="SM_PAPERMILL_INPUT")

    @unittest.mock.patch.dict(os.environ, env_missing_kernel)
    def test_env_missing_kernel(self):
        self.do_test_for_missing_env_key(env_key_name="SM_KERNEL_NAME")

    @unittest.mock.patch.dict(os.environ, env_missing_params_path)
    def test_env_missing_params_path(self):
        self.do_test_for_missing_env_key(env_key_name="SM_PAPERMILL_PARAMS_PATH")

    @unittest.mock.patch.dict(os.environ, env_happy_case)
    @patch(
        "sagemaker_headless_execution_driver.notebookrunner.NotebookExecutionLanguageUtils.has_language_info"
    )
    @patch("os.path.exists")
    @patch(
        "sagemaker_headless_execution_driver.notebookrunner.papermill.execute_notebook"
    )
    @patch("sagemaker_headless_execution_driver.notebookrunner.json.load")
    @patch("builtins.open")
    def test_happy_case(
        self,
        mock_open,
        mock_json_load,
        mock_papermill,
        mock_exists,
        mock_has_language_info,
    ):
        mock_json_load.return_value = {"test": "test"}
        mock_open.return_value = MagicMock()
        mock_exists.return_value = True
        mock_has_language_info.return_value = True

        PaperMillNotebookRunner().run_notebook()

        mock_papermill.assert_called_with(
            "input.ipynb",
            "/tmp/output.ipynb",
            parameters={"test": "test"},
            kernel_name="python3",
            language=None,
            engine_name="sagemaker_engine",
        )

        mock_has_language_info.assert_called_with("/tmp/input.ipynb")

    @unittest.mock.patch.dict(os.environ, env_happy_case)
    @patch(
        "sagemaker_headless_execution_driver.notebookrunner.NotebookExecutionLanguageUtils.get_language_from_kernel"
    )
    @patch(
        "sagemaker_headless_execution_driver.notebookrunner.NotebookExecutionLanguageUtils.has_language_info"
    )
    @patch("os.path.exists")
    @patch(
        "sagemaker_headless_execution_driver.notebookrunner.papermill.execute_notebook"
    )
    @patch("sagemaker_headless_execution_driver.notebookrunner.json.load")
    @patch("builtins.open")
    def test_happy_case_with_no_language(
        self,
        mock_open,
        mock_json_load,
        mock_papermill,
        mock_exists,
        mock_has_language_info,
        mock_get_language_from_kernel,
    ):
        mock_json_load.return_value = {"test": "test"}
        mock_open.return_value = MagicMock()
        mock_exists.return_value = True
        mock_has_language_info.return_value = False
        mock_get_language_from_kernel.return_value = "language_from_kernelspec"

        PaperMillNotebookRunner().run_notebook()

        mock_papermill.assert_called_with(
            "input.ipynb",
            "/tmp/output.ipynb",
            parameters={"test": "test"},
            kernel_name="python3",
            language="language_from_kernelspec",
            engine_name="sagemaker_engine",
        )

        mock_has_language_info.assert_called_with("/tmp/input.ipynb")
        mock_get_language_from_kernel.assert_called_with("python3")

    @unittest.mock.patch.dict(os.environ, env_happy_case)
    @patch(
        "sagemaker_headless_execution_driver.notebookrunner.NotebookExecutionLanguageUtils.get_language_from_kernel"
    )
    @patch(
        "sagemaker_headless_execution_driver.notebookrunner.NotebookExecutionLanguageUtils.has_language_info"
    )
    @patch("os.path.exists")
    @patch(
        "sagemaker_headless_execution_driver.notebookrunner.papermill.execute_notebook"
    )
    @patch("sagemaker_headless_execution_driver.notebookrunner.json.load")
    @patch("builtins.open")
    def test_happy_case_with_no_language_and_kernel_not_found(
        self,
        mock_open,
        mock_json_load,
        mock_papermill,
        mock_exists,
        mock_has_language_info,
        mock_get_language_from_kernel,
    ):
        mock_json_load.return_value = {"test": "test"}
        mock_open.return_value = MagicMock()
        mock_exists.return_value = True
        mock_has_language_info.return_value = False
        mock_get_language_from_kernel.side_effect = Exception(
            "My runtime exception while getting language"
        )

        sys_error_msg = io.StringIO()
        with self.assertRaises(SystemExit) as exit_info, contextlib.redirect_stderr(
            sys_error_msg
        ):
            PaperMillNotebookRunner().run_notebook()

        assert (
            sys_error_msg.getvalue().find("My runtime exception while getting language")
            > -1
        ), f"Did not catch expected exception."
        self.assertEqual(exit_info.exception.code, 1)

        mock_has_language_info.assert_called_with("/tmp/input.ipynb")
        mock_get_language_from_kernel.assert_called_with("python3")

    @unittest.mock.patch.dict(os.environ, env_happy_case)
    @patch("os.path.exists")
    @patch("sagemaker_headless_execution_driver.notebookrunner.json.load")
    @patch("builtins.open")
    def test_failure_of_loading_params_file(
        self, mock_open, mock_json_load, mock_exists
    ):
        mock_json_load.side_effect = ValueError("My runtime error")
        mock_open.return_value = MagicMock()
        mock_exists.return_value = True

        sys_error_msg = io.StringIO()
        with self.assertRaises(SystemExit) as exit_info, contextlib.redirect_stderr(
            sys_error_msg
        ):
            PaperMillNotebookRunner().run_notebook()

        assert (
            sys_error_msg.getvalue().find("My runtime error") > -1
        ), f"Did not catch expected exception."
        self.assertEqual(exit_info.exception.code, 1)

    @unittest.mock.patch.dict(os.environ, env_non_existing_input_file)
    def test_failure_of_loading_non_existing_input_file(self):
        sys_error_msg = io.StringIO()
        with self.assertRaises(SystemExit) as exit_info, contextlib.redirect_stderr(
            sys_error_msg
        ):
            PaperMillNotebookRunner().run_notebook()

        assert (
            sys_error_msg.getvalue().find("/non-existing/folder/input.ipynb") > -1
        ), f"Did not catch expected exception of file not found."

        self.assertEqual(exit_info.exception.code, 1)

    @unittest.mock.patch.dict(os.environ, env_happy_case)
    @patch(
        "sagemaker_headless_execution_driver.notebookrunner.NotebookExecutionLanguageUtils.has_language_info"
    )
    @patch("os.path.exists")
    @patch(
        "sagemaker_headless_execution_driver.notebookrunner.papermill.execute_notebook"
    )
    @patch("sagemaker_headless_execution_driver.notebookrunner.json.load")
    @patch("builtins.open")
    def test_failure_of_papermill_execution(
        self,
        mock_open,
        mock_json_load,
        mock_papermill,
        mock_exists,
        mock_has_language_info,
    ):
        mock_json_load.return_value = {"test": "test"}
        mock_open.return_value = MagicMock()
        mock_papermill.side_effect = Exception("My runtime exception")
        mock_exists.return_value = True
        mock_has_language_info.return_value = True

        sys_error_msg = io.StringIO()
        with self.assertRaises(SystemExit) as exit_info, contextlib.redirect_stderr(
            sys_error_msg
        ):
            PaperMillNotebookRunner().run_notebook()

        assert (
            sys_error_msg.getvalue().find("My runtime exception") > -1
        ), f"Did not catch expected exception."
        self.assertEqual(exit_info.exception.code, 1)

    @unittest.mock.patch.dict(os.environ, env_happy_case)
    @patch(
        "sagemaker_headless_execution_driver.notebookrunner.NotebookExecutionLanguageUtils.has_language_info"
    )
    @patch("os.path.exists")
    @patch(
        "sagemaker_headless_execution_driver.notebookrunner.papermill.execute_notebook"
    )
    @patch("sagemaker_headless_execution_driver.notebookrunner.json.load")
    @patch("builtins.open")
    def test_failure_of_papermill_execution(
        self,
        mock_open,
        mock_json_load,
        mock_papermill,
        mock_exists,
        mock_has_language_info,
    ):
        mock_json_load.return_value = {"test": "test"}
        mock_open.return_value = MagicMock()
        mock_papermill.side_effect = Exception("My runtime exception")
        mock_exists.return_value = True
        mock_has_language_info.return_value = True

        sys_error_msg = io.StringIO()
        with self.assertRaises(SystemExit) as exit_info, contextlib.redirect_stderr(
            sys_error_msg
        ):
            PaperMillNotebookRunner().run_notebook()

        assert (
            sys_error_msg.getvalue().find("My runtime exception") > -1
        ), f"Did not catch expected exception."
        self.assertEqual(exit_info.exception.code, 1)

    def do_test_for_missing_env_key(self, env_key_name):
        sys_error_msg = io.StringIO()
        with self.assertRaises(SystemExit) as exit_info, contextlib.redirect_stderr(
            sys_error_msg
        ):
            PaperMillNotebookRunner().run_notebook()

        self.assertEqual(exit_info.exception.code, 1)
        assert (
            sys_error_msg.getvalue().find(env_key_name) > -1
        ), f"error message is not as expected to include {env_key_name}"
