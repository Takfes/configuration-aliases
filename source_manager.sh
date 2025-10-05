#!/bin/bash

ALIASES_DIR=$CONFIG_PATH/aliases
SCRIPTS_DIR=$CONFIG_PATH/scripts

source $ALIASES_DIR/.aliases
source $SCRIPTS_DIR/setup_anaconda.sh
source $SCRIPTS_DIR/setup_ohmyzsh.sh
source $SCRIPTS_DIR/setup_p10k.sh
