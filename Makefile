# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#

# new model
model:
	@echo "checking for existing $(MODEL_NAME) directory"
	@if [ -d $(MODEL_NAME) ]; \
		then echo "model already exists"; \
		else ( ./create_model_template.sh --model $(MODEL_NAME)) \
	fi
