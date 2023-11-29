# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import subprocess
import os
import sagemaker_headless_execution_driver


def main():
    # Detect if the user is root or non-root
    current_uid = os.getuid()

    # Adjust permissions if User is not root-user
    if current_uid != 0:
        # Define directories
        data_dir = "/opt/ml/input/data"
        input_dir = "/opt/ml/input"
        output_dir = "/opt/ml/output"
        tmp_dir = "/tmp"
        # Use subprocess to run chown and chmod commands
        try:
            # Only attempt chown if directory exists
            if os.path.exists(data_dir):
                subprocess.run(
                    ["sudo", "chown", "-R", "1000:100", data_dir], check=True
                )

            # Only attempt chmod if directories exist
            dirs_to_modify = [
                d for d in [input_dir, output_dir, tmp_dir] if os.path.exists(d)
            ]
            if dirs_to_modify:
                subprocess.run(
                    ["sudo", "chmod", "-R", "777"] + dirs_to_modify,
                    check=True,
                )

        except subprocess.CalledProcessError as e:
            print(f"Error while changing permissions: {e}")
            raise

    # Path to the headless_execution.sh script
    script_path = os.path.join(
        os.path.dirname(sagemaker_headless_execution_driver.__file__),
        "scripts",
        "headless_execution.sh",
    )

    # Use os.execvp to replace the current process with the bash script
    try:
        os.execvp("/bin/bash", ["/bin/bash", script_path])
    except Exception as e:
        if "No such file or directory" in str(e):
            print(
                "Error: The required shell script was not found in the expected location."
            )
            print(f"Expected location: {script_path}")
            print(
                "Please ensure the shell script exists in the specified location or check your package installation."
            )
        else:
            print(f"Error executing headless_execution.sh: {e}")
        raise


if __name__ == "__main__":
    main()
