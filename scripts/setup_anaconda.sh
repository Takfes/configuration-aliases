#!/bin/bash

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/Users/takis/miniforge3/bin/conda' 'shell.zsh' 'hook' 2>/dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/Users/takis/miniforge3/etc/profile.d/conda.sh" ]; then
        . "/Users/takis/miniforge3/etc/profile.d/conda.sh"
    else
        export PATH="/Users/takis/miniforge3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
export PATH="/opt/homebrew/opt/cbc/bin:$PATH"

. "$HOME/.local/bin/env"
