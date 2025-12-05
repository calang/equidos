#!usr/bin/env bash

# add these lines to your .bashrc to auto-run on terminal start

# # initialize with local file, if present
# wd=$(pwd)
# if [ -f .bashrc -a "$wd" != "$HOME" ]
# then
#     # read -p "** Local .bashrc found; use as initializer [y|N]? " Y
#     # [ "$Y" == "y" ] && . .bashrc
#     echo "** Warning: local $wd/.bashrc found, used as initializer."
#     . .bashrc
# # else
# #     echo "no init"
# fi

# Below, the actual initialization


# load .env variables
. .env

# export .env variables
for var in $(grep = .env | grep -v '^#' | cut -d = -f 1)
do
    export $var
done

export CONDA_ENV_NAME=$(head -1 env.yml | cut -d ' ' -f 2)

conda activate $CONDA_ENV_NAME

# set CUDA and TF variables (duplicating Makefile definitions, for now)
# export CUDA_DIR=${CONDA_PREFIX}
# export XLA_FLAGS="--xla_gpu_cuda_data_dir=${CUDA_DIR}"
# export TF_ENABLE_ONEDNN_OPTS=0
# export TF_SETENV="export CUDA_DIR=${CUDA_DIR} XLA_FLAGS=${XLA_FLAGS} TF_ENABLE_ONEDNN_OPTS=${TF_ENABLE_ONEDNN_OPTS}"

