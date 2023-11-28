#!/bin/bash

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

# Following redirection only works for bash.
LOCAL_LOG_FOLDER="/tmp"
exec > >(tee ${LOCAL_LOG_FOLDER}/sagemaker_job_execution.log) 2>&1
trap 'exit_code=$?; exit_hook ${exit_code}' EXIT
trap 'terminate_hook' SIGTERM

exit_hook()
{
  set +x
  exit_code=$1

  # for user to troubleshoot without needs to access cloudwatch - /opt/ml/output/data/sagemaker_job_execution.log
  cp ${LOCAL_LOG_FOLDER}/sagemaker_job_execution.log ${TRAINING_OUTPUT_PATH}

  if [ "$exit_code" -ne 0 ]
  then
    output_flags=$(check_outputs "${TRAINING_OUTPUT_PATH}/${SM_INPUT_NOTEBOOK_NAME}" "$SM_PAPERMILL_OUTPUT" \
                                 "${TRAINING_OUTPUT_PATH}/sagemaker_job_execution.log" )

    # generate the training failure output file for failed step - /opt/ml/output/failure
    echo "[SM-${output_flags}] Error with $SM_EXEC_STEP" > ${TRAINING_FAILURE_PATH}
    sed "0,/$SM_EXEC_STEP/d;/^+ /d" ${LOCAL_LOG_FOLDER}/sagemaker_job_execution.log >>${TRAINING_FAILURE_PATH}
  fi
}

check_outputs()
{
  flags=""
  while (($#)); do
    if [ -f "${1}" ]
    then
        flags="${flags}1"
    else
        flags="${flags}0"
    fi
    shift
  done
  echo $flags
}

terminate_hook()
{
  echo "Invoke terminate_hook"
  if [ ! -z "${papermill_process}" ]
  then
    kill -SIGTERM ${papermill_process} 2>/dev/null
    sleep 30
  fi
}

set -ex
TRAINING_OUTPUT_PATH="/opt/ml/output/data"
TRAINING_FAILURE_PATH="/opt/ml/output/failure"
SM_EXECUTION_INPUT_PATH="${SM_EXECUTION_INPUT_PATH:=/opt/ml/input/data/sagemaker_headless_execution}"
SM_EXECUTION_SYSTEM_PATH="${SM_EXECUTION_SYSTEM_PATH:=/opt/ml/input/data/sagemaker_headless_execution_system}"
export SM_PAPERMILL_INPUT=${SM_EXECUTION_INPUT_PATH}/${SM_INPUT_NOTEBOOK_NAME:? "ERROR - Input notebook name is not specified."}

mkdir -p $TRAINING_OUTPUT_PATH

# ----cp the input notebook to output----
SM_EXEC_STEP="Prepare the input notebook"
if [ -f "${SM_PAPERMILL_INPUT}" ]
then
    cp "${SM_PAPERMILL_INPUT}" "$TRAINING_OUTPUT_PATH"
else
  echo "Cannot find input notebook: ${SM_PAPERMILL_INPUT}"
  exit 1
fi

# ----check job input definition version----
if [ "${SM_JOB_DEF_VERSION}" != "1.0"  ]
then
  SM_EXEC_STEP="checking sagemaker job definition version"
  echo "Cannot handle SageMaker job definition version: ${SM_JOB_DEF_VERSION}" >&2
  exit 1
fi

# ----find the python executable----
SM_EXEC_STEP="detecting python runtime"
if [ ! -z "${SM_HEADLESS_EXECUTION_PATH}" ] && [ -x ${SM_HEADLESS_EXECUTION_PATH}/python ]
then
  PYTHON_EXECUTABLE="${SM_HEADLESS_EXECUTION_PATH}/python"
else
  PYTHON_EXECUTABLE=$(which python)
fi

echo "Python executable: ${PYTHON_EXECUTABLE}"
DEFAULT_PYTHON_VERSION=$(${PYTHON_EXECUTABLE} -c 'import sys; version=sys.version_info[:3]; print("{0}.{1}".format(*version))')

# ----simulate the Studio EFS mount path----
if [ "${SM_SKIP_EFS_SIMULATION}" = "true" ]; then
  echo "EFS Simulation is skipped."
else
  SM_EXEC_STEP="creating symbol link to simulate the EFS mounting path"
  if [ "${SM_EFS_MOUNT_PATH}" = "/root" ]; then
    mv /root/ /root_backup
    ln -s "${SM_EXECUTION_INPUT_PATH}" /root
    cp -R /root_backup/. /root
  else
    mkdir -p "$(dirname "$SM_EFS_MOUNT_PATH")"
    ln -s "${SM_EXECUTION_INPUT_PATH}" "${SM_EFS_MOUNT_PATH}"
    chown -R "${SM_EFS_MOUNT_UID}" "${SM_EXECUTION_INPUT_PATH}"
    chgrp -R "${SM_EFS_MOUNT_GID}" "${SM_EXECUTION_INPUT_PATH}"
  fi
fi

# simulate the jupyterlab server mounting point when container is running as root
if [[ $(id -u) -eq 0 ]]
then
    [ -d "/home/sagemaker-user" ] || ln -s "${SM_EXECUTION_INPUT_PATH}" "/home/sagemaker-user"
fi

# short-term fix to disable use_auto_viz for SparkMagic %%sql hang issue.
# https://github.com/jupyter-incubator/sparkmagic/issues/833
sparkmagic_config_file="/etc/sparkmagic/config.json"
if [ -e "${sparkmagic_config_file}" ]; then
  ${PYTHON_EXECUTABLE} -c "import json; json_file = '${sparkmagic_config_file}'; data = json.load(open(json_file)); data['use_auto_viz'] = False; json.dump(data, open(json_file, 'w'), indent=4)"
fi

# ----run the init script(s)----
SM_EXEC_STEP="running LCC script as init-script"
cd ${SM_EXECUTION_INPUT_PATH}
# run lcc script in sub shell script and env variables from lcc are not available later in notebook execution.
if [ ! -z "${SM_LCC_INIT_SCRIPT}" ]; then
  sh "${SM_EXECUTION_INPUT_PATH}/${SM_LCC_INIT_SCRIPT}"
else
  echo "No lcc-init-script is specified."
fi

# Source the init-script at last so that user has a chance to override and env variables from init-script are
# available later in notebook execution.
SM_EXEC_STEP="running init script"
if [ ! -z "${SM_INIT_SCRIPT}" ]; then
  . "${SM_EXECUTION_INPUT_PATH}/${SM_INIT_SCRIPT}"
else
  echo "No init-script is specified."
fi

# ----run the customer_input----
SM_EXEC_STEP="executing notebook"
export SM_PAPERMILL_PARAMS_PATH="/opt/ml/input/config/hyperparameters.json"
export SM_PAPERMILL_OUTPUT=${TRAINING_OUTPUT_PATH}/${SM_OUTPUT_NOTEBOOK_NAME:? "ERROR - Output notebook name is not specified."}
export SM_PAPERMILL_FAILURE_FILE=$TRAINING_FAILURE_PATH

# Fix the output notebook path containing the timestamp from pipeline variables:
# (1) replace ':' with '-' and only allow '.' for file extension. This is an internal contract.
export SM_PAPERMILL_OUTPUT=$(echo $SM_PAPERMILL_OUTPUT | sed 's|\.|-|g; s|:|-|g; s|-*ipynb$|.ipynb|g;')

${PYTHON_EXECUTABLE} -m sagemaker_headless_execution_driver.notebookrunner&
papermill_process=$!
wait ${papermill_process}
echo "Notebook execution is complete"
