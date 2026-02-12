# Description

# variable definitions, available to all rules
REPO_ROOT := $(shell git rev-parse --show-toplevel)  # root directory of this git repo
BRANCH := $(shell git branch --show-current)
# BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
# Notes:
# all env variables are available
# = uses recursive substitution
# :=  uses immediate substitution

# ENV_NAME is second word, separated by one space, in file env.yml
ENV_NAME := $(shell head -1 env.yml | cut -d ' ' -f 2)

# Enable GPU support for TensorFlow and PyTorch
# CUDA_DIR uses the active conda environment prefix
CUDA_DIR := ${CONDA_PREFIX}
XLA_FLAGS := --xla_gpu_cuda_data_dir=${CUDA_DIR}
LD_LIBRARY_PATH := ${CUDA_DIR}/lib:${LD_LIBRARY_PATH}
TF_ENABLE_ONEDNN_OPTS := 0
TF_SETENV := export CUDA_DIR=${CUDA_DIR} XLA_FLAGS="${XLA_FLAGS}" LD_LIBRARY_PATH="${LD_LIBRARY_PATH}" TF_ENABLE_ONEDNN_OPTS=${TF_ENABLE_ONEDNN_OPTS}


# target: help - Display callable targets.
help:
	@echo "Usage:  make <target>"
	@echo "  where <target> may be"
	@echo
	@egrep -h "^# target:" [Mm]akefile | sed -e 's/^# target: //'

# target: show-vars - show defined variables
show-vars:
	@echo "REPO_ROOT=${REPO_ROOT}"
	@echo "BRANCH=${BRANCH}"
	@echo "ENV_NAME=${ENV_NAME}"
	@echo "CUDA_DIR=${CUDA_DIR}"
	@echo "XLA_FLAGS=${XLA_FLAGS}"
	@echo "LD_LIBRARY_PATH=${LD_LIBRARY_PATH}"
	@echo "TF_ENABLE_ONEDNN_OPTS=${TF_ENABLE_ONEDNN_OPTS}"
	@echo "TF_SETENV=${TF_SETENV}"

# target: update-env - update conda environment based on latest content of environment.yml file
update-env:
	$(TF_SETENV); conda env update -f env.yml --prune

# target: rm-env - update conda environment based on latest content of environment.yml file
rm-env:
	conda env remove -n ${ENV_NAME}

# # target: requirements - install/update python required packages
# requirements:	ALWAYS
# 	pip install --upgrade -r requirements.txt

# target: coding-standards - coding instructions for agents
coding-standards:	../common/coding-standards/python
	cp -R ../common/coding-standards/python .

# target: horsefacebase - create data/horsefacebase directory from TunHorseDB2015
data/horsefacebase:	data/TunHorseDB2015 src/scripts/xbasefaces.py
	python src/scripts/xbasefaces.py

# target: horsefacecrop - create data/horsefacecrop directory from data/horsefacebase
data/horsefacecrop:	data/horsefacebase src/scripts/xcropfaces.py
	python src/scripts/xcropfaces.py 2>&1 | tee src/scripts/xcropfaces.log

# ============================================================
# ResNet50-47 Experiment (TunHorseDB2015G - all face angles)
# ============================================================

# target: resnet50-47-prep-data - split TunHorseDB2015G into training, validation and test sets
resnet50-47-prep-data:	data/THGtraining data/THGvalidation data/THGtest

data/THGtraining data/THGvalidation data/THGtest &: data/TunHorseDB2015G experiments/ResNet50-47/prep_data.py
	python experiments/ResNet50-47/prep_data.py

# target: resnet50-47-models - train ResNet50-47 model and produce best_model.pth and final_model.pth
resnet50-47-models:	experiments/ResNet50-47/models/best_model.pth experiments/ResNet50-47/models/final_model.pth

experiments/ResNet50-47/models/best_model.pth experiments/ResNet50-47/models/final_model.pth &: data/THGtraining data/THGvalidation data/THGtest experiments/ResNet50-47/train_model.py
	experiments/ResNet50-47/train_model.py --epochs 20

# target: resnet50-47-training-history - plot training history of ResNet50-47 model
resnet50-47-training-history:	experiments/ResNet50-47/training_history.png

experiments/ResNet50-47/training_history.png &: experiments/ResNet50-47/models/best_model.pth experiments/ResNet50-47/models/final_model.pth experiments/ResNet50-47/visualize_training.py
	./experiments/ResNet50-47/visualize_training.py --save-plot experiments/ResNet50-47/training_history.png

# target: resnet50-47-test-results - run test script and produce test_results.csv for ResNet50-47
resnet50-47-test-results:	experiments/ResNet50-47/test_results.csv

experiments/ResNet50-47/test_results.csv:	experiments/ResNet50-47/models/best_model.pth experiments/ResNet50-47/test_model.py
	./experiments/ResNet50-47/test_model.py --model experiments/ResNet50-47/models/best_model.pth --output experiments/ResNet50-47/test_results.csv

# ============================================================
# ResNet50-47F Experiment (TunHorseDB2015F - front faces only)
# ============================================================

# target: resnet50-47f-prep-data - split TunHorseDB2015F into training, validation and test sets
resnet50-47f-prep-data:	data/THFtraining data/THFvalidation data/THFtest

data/THFtraining data/THFvalidation data/THFtest &: data/TunHorseDB2015F experiments/ResNet50-47F/prep_data.py
	python experiments/ResNet50-47F/prep_data.py

# target: resnet50-47f-models - train ResNet50-47F model and produce best_model.pth and final_model.pth
resnet50-47f-models:	experiments/ResNet50-47F/models/best_model.pth experiments/ResNet50-47F/models/final_model.pth

experiments/ResNet50-47F/models/best_model.pth experiments/ResNet50-47F/models/final_model.pth &: data/THFtraining data/THFvalidation data/THFtest experiments/ResNet50-47F/train_model.py
	experiments/ResNet50-47F/train_model.py --epochs 20

# target: resnet50-47f-training-history - plot training history of ResNet50-47F model
resnet50-47f-training-history:	experiments/ResNet50-47F/training_history.png

experiments/ResNet50-47F/training_history.png &: experiments/ResNet50-47F/models/best_model.pth experiments/ResNet50-47F/models/final_model.pth experiments/ResNet50-47F/visualize_training.py
	./experiments/ResNet50-47F/visualize_training.py --save-plot experiments/ResNet50-47F/training_history.png

# target: resnet50-47f-test-results - run test script and produce test_results.csv for ResNet50-47F
resnet50-47f-test-results:	experiments/ResNet50-47F/test_results.csv

experiments/ResNet50-47F/test_results.csv:	experiments/ResNet50-47F/models/best_model.pth experiments/ResNet50-47F/test_model.py
	./experiments/ResNet50-47F/test_model.py --model experiments/ResNet50-47F/models/best_model.pth --output experiments/ResNet50-47F/test_results.csv

# ============================================================
# Utilities
# ============================================================

# target: jupl - start jupiter lab server
jupl:	ALWAYS
	@${TF_SETENV}; jupyter lab &


# target push - sample docker image push, asking for passwords
# push: TEMPUSR := $(shell mktemp)
# push:
#	@$$SHELL -i -c 'read -p "username: " user;  echo -n $${user} >$(TEMPUSR)'
#	@$$SHELL -i -c 'read -s -p "password: " user;  echo -n $${user} >$(TEMPUSR)1'
#	@docker login -u $$(cat $(TEMPUSR)) -p $$(cat $(TEMPUSR)1) amr-registry.caas.intel.com
#	docker image push ${APP_IMAGE}
#	@rm $(TEMPUSR)*

# 	@rm $(TEMPUSR)*

# ignore files with any of these names
# so that the rules with those as target are always executed
.PHONY: ALWAYS

# always do/refresh ALWAYS target
ALWAYS:
