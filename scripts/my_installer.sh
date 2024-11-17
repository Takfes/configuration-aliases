#!/bin/bash

# Configuration
EXECUTION_VERBOSE=true                         # Verbose output for script execution
PACKAGE_MISSING_VERBOSE=true                   # Verbose output for missing tools
PACKAGE_MISSING_SHOW_INSTALLATION_COMMAND=true # Show installation command for missing tools
PACKAGE_MISSING_TRY_INSTALL=false              # Install missing tools
PACKAGE_MISSING_INDIVIDUAL_CONFIRMATION=true   # Confirm installation of each missing tool
PACKAGE_EXIST_VERBOSE=true                     # Inform user package exists
PACKAGE_EXIST_VERSION_VERBOSE=false            # Show version of installed tools

# Tools to check
TOOLS=(
    "brew"
    "git"
    "ssh"
    "curl"
    "wget"
    "zsh"
    "kitty"
    "warp"
    "code"
    "nvim"
    "docker"
    "docker-compose"
    "lazygit"
    "lazydocker"
    "minikube"
    "kubectl"
    "npm"
    "anaconda"
    "miniconda"
    "uv"
    "pip"
    "pyenv"
    "poetry"
    "dvc"
    "oh-my-zsh"
    "fzf"
    "fd"
    "exa"
    "eza"
    "bat"
    "zoxide"
    "ranger"
    "tmux"
    "yabai"
    "skhd"
)

# Function to install a tool on macOS
install_tool() {
    local tool="$1"
    local success=true
    local cmd=""

    case "$tool" in
    brew)
        cmd="/bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        ;;
    oh-my-zsh)
        cmd="sh -c \"\$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)\""
        ;;
    miniconda | anaconda)
        cmd="curl -fsSL https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o miniconda.sh && bash miniconda.sh -b -p \$HOME/miniconda"
        ;;
    warp)
        cmd="brew install --cask warp"
        ;;
    code)
        cmd="brew install --cask visual-studio-code"
        ;;
    kitty)
        cmd="brew install --cask kitty"
        ;;
    *)
        cmd="brew install $tool"
        ;;
    esac

    if [ "$PACKAGE_MISSING_SHOW_INSTALLATION_COMMAND" = true ]; then
        echo "🤔 Installation command for $tool: $cmd"
    fi

    if [ "$PACKAGE_MISSING_TRY_INSTALL" = true ]; then
        if [ "$PACKAGE_MISSING_INDIVIDUAL_CONFIRMATION" = true ]; then
            echo "❓ Do you want to install $tool? (y/n)"
            read -r confirmation
            if [[ "$confirmation" != "y" && "$confirmation" != "Y" ]]; then
                echo "⏭️  Skipping installation of $tool."
                return
            fi
        fi

        echo "🤞 Attempting to install $tool..."
        eval "$cmd" || success=false

        if [ "$success" = true ]; then
            echo "🎉 Successfully installed $tool."
        else
            echo "😓 Failed to install $tool."
        fi
    fi
}

# Function to get the version of a tool
get_version() {
    local tool="$1"
    case "$tool" in
    oh-my-zsh)
        echo "oh-my-zsh: Installed (version not applicable)"
        ;;
    brew | fzf | git | docker | npm | kubectl | tmux | nvim | python | pip | poetry)
        "$tool" --version 2>/dev/null | head -n 1
        ;;
    code)
        code --version 2>/dev/null | head -n 1
        ;;
    *)
        "$tool" -v 2>/dev/null || "$tool" --version 2>/dev/null || echo "Version not available for $tool"
        ;;
    esac
}

# Main script logic
for tool in "${TOOLS[@]}"; do
    if [ "$EXECUTION_VERBOSE" = true ]; then
        echo "🔍 Now checking tool: $tool"
    fi

    if command -v "$tool" >/dev/null; then
        # Tool exists
        if [ "$PACKAGE_EXIST_VERBOSE" = true ]; then
            echo "✅ $tool is installed."
        fi
        if [ "$PACKAGE_EXIST_VERSION_VERBOSE" = true ]; then
            version=$(get_version "$tool")
            echo "$version"
        fi
    else
        # Tool is missing
        if [ "$PACKAGE_MISSING_VERBOSE" = true ]; then
            echo "❌ $tool is not installed."
        fi
        install_tool "$tool"
    fi
    echo "------------------------------------------------"
    echo ""
done
