# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import unittest
from unittest.mock import patch, MagicMock
from sagemaker_headless_execution_driver.notebookrunner import (
    NotebookExecutionLanguageUtils,
)
import json


class TestNotebookExecutionLanguageUtils(unittest.TestCase):
    @patch("sagemaker_headless_execution_driver.notebookrunner.KernelSpecManager")
    def test_get_language_from_kernel(self, mock_kernelspck_manager_cls):
        mock_kernelspck_manager = MagicMock()
        mock_kernelspck_manager_cls.return_value = mock_kernelspck_manager

        mock_kernelspec = MagicMock()
        mock_kernelspck_manager.get_kernel_spec.return_value = mock_kernelspec
        mock_kernelspec.language = "python_lang"

        lang = NotebookExecutionLanguageUtils.get_language_from_kernel("python3")
        assert lang == "python_lang"
        mock_kernelspck_manager.get_kernel_spec.assert_called_with("python3")

    @patch("sagemaker_headless_execution_driver.notebookrunner.nbformat")
    def test_has_language_info_as_false_due_to_blank_lang(self, mock_nbformat):
        self._do_test_for_has_language(mock_nbformat, "", False)

    @patch("sagemaker_headless_execution_driver.notebookrunner.nbformat")
    def test_has_language_info_as_true(self, mock_nbformat):
        self._do_test_for_has_language(mock_nbformat, "python", True)

    @patch("sagemaker_headless_execution_driver.notebookrunner.nbformat")
    def test_no_metadata(self, mock_nbformat):
        mock_nb_node = MagicMock()
        mock_nb_node.hasattr.return_value = False

        mock_nbformat.read.return_value = mock_nb_node
        mock_nbformat.NO_CONVERT = 1000

        has_lang_info = NotebookExecutionLanguageUtils.has_language_info(
            "notebook.ipynb"
        )
        assert has_lang_info == False

        mock_nbformat.read.assert_called_with("notebook.ipynb", 1000)
        mock_nb_node.hasattr.assert_called_with("metadata")

    @patch("sagemaker_headless_execution_driver.notebookrunner.nbformat")
    def test_no_language_info(self, mock_nbformat):
        mock_nb_node = MagicMock()
        mock_metadata_node = MagicMock()

        mock_nb_node.metadata = mock_metadata_node
        mock_metadata_node.hasattr.return_value = False

        mock_nbformat.read.return_value = mock_nb_node
        mock_nbformat.NO_CONVERT = 1000

        has_lang_info = NotebookExecutionLanguageUtils.has_language_info(
            "notebook.ipynb"
        )
        assert has_lang_info == False

        mock_nbformat.read.assert_called_with("notebook.ipynb", 1000)
        mock_nb_node.hasattr.assert_called_with("metadata")
        mock_metadata_node.hasattr.assert_called_with("language_info")

    @patch("sagemaker_headless_execution_driver.notebookrunner.nbformat")
    def test_no_language_info_name(self, mock_nbformat):
        mock_nb_node = MagicMock()
        mock_metadata_node = MagicMock()
        mock_lang_info_node = MagicMock()

        mock_nb_node.metadata = mock_metadata_node
        mock_metadata_node.language_info = mock_lang_info_node

        mock_lang_info_node.hasattr.return_value = False

        mock_nbformat.read.return_value = mock_nb_node
        mock_nbformat.NO_CONVERT = 1000

        has_lang_info = NotebookExecutionLanguageUtils.has_language_info(
            "notebook.ipynb"
        )
        assert has_lang_info == False

        mock_nbformat.read.assert_called_with("notebook.ipynb", 1000)
        mock_nb_node.hasattr.assert_called_with("metadata")
        mock_metadata_node.hasattr.assert_called_with("language_info")
        mock_lang_info_node.hasattr.assert_called_with("name")

    def _do_test_for_has_language(self, mock_nbformat, lang, expect_result):
        mock_nb_node = MagicMock()
        mock_metadata_node = MagicMock()
        mock_lang_info_node = MagicMock()

        mock_nb_node.metadata = mock_metadata_node
        mock_metadata_node.language_info = mock_lang_info_node
        mock_metadata_node.language_info.name = lang

        mock_nbformat.read.return_value = mock_nb_node
        mock_nbformat.NO_CONVERT = 1000

        has_lang_info = NotebookExecutionLanguageUtils.has_language_info(
            "notebook.ipynb"
        )
        assert has_lang_info == expect_result

        mock_nbformat.read.assert_called_with("notebook.ipynb", 1000)
