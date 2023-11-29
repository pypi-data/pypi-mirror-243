# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import unittest
import subprocess
import os
import sagemaker_headless_execution_driver

from unittest.mock import patch, Mock, call, MagicMock
import sagemaker_headless_execution_driver.headless_execution as execution_driver

SCRIPT_PATH = os.path.join(
    os.path.dirname(sagemaker_headless_execution_driver.__file__),
    "scripts",
    "headless_execution.sh",
)


class TestHeadlessExecution(unittest.TestCase):
    @patch("os.execvp")
    @patch(
        "os.path.exists", return_value=True
    )  # Mock os.path.exists to always return True
    @patch("os.getuid")
    @patch("sagemaker_headless_execution_driver.headless_execution.subprocess.run")
    def test_permissions_adjusted(
        self, mock_run, mock_getuid, mock_exists, mock_execvp
    ):
        mock_getuid.return_value = 100  # Non-root user UID

        # Mock the return value for subprocess.run
        mock_completed_process = MagicMock()
        mock_completed_process.stdout = "Mocked stdout"
        mock_run.return_value = mock_completed_process
        execution_driver.main()
        calls = [
            call(["sudo", "chown", "-R", "1000:100", "/opt/ml/input/data"], check=True),
            call(
                [
                    "sudo",
                    "chmod",
                    "-R",
                    "777",
                    "/opt/ml/input",
                    "/opt/ml/output",
                    "/tmp",
                ],
                check=True,
            ),
        ]
        mock_run.assert_has_calls(calls, any_order=True)
        mock_execvp.assert_called_with("/bin/bash", ["/bin/bash", SCRIPT_PATH])

    @patch("os.execvp")
    @patch("os.getuid")
    def test_permissions_not_adjusted(self, mock_getuid, mock_execvp):
        mock_getuid.return_value = 0  # Root user UID
        execution_driver.main()
        mock_execvp.assert_called_with("/bin/bash", ["/bin/bash", SCRIPT_PATH])

    @patch("os.execvp")
    @patch("os.getuid", return_value=0)  # Mocking to return root UID
    def test_script_executed(self, mock_getuid, mock_execvp):
        execution_driver.main()
        mock_execvp.assert_called_with("/bin/bash", ["/bin/bash", SCRIPT_PATH])

    @patch("os.execvp", side_effect=Exception("Mocked Exception"))
    def test_script_execution_failure(self, mock_execvp):
        with self.assertRaises(Exception):
            execution_driver.main()


if __name__ == "__main__":
    unittest.main()
