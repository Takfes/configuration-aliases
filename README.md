<p align="center">
    <img src="static/logo.svg" alt="Project Logo" width="480"/>
</p>

# ALIAS MANAGEMENT

## WHAT IS THIS?
A centralized, portable alias management system for consistent shell environments across different systems. See [repo_toc](docs/repo_toc.md) for a detailed repository walkthrough.

## WHY DOES IT MATTER?
- **Consistency**: Maintain the same set of aliases across multiple systems (e.g., work
- **Version Control**: Keep track of changes and history of alias configurations

## HOW IT WORKS?
- **🎯 The Hub**: All alias files live in one version-controlled repository (your single source of truth)
- **🔗 The Bridge**: Link your shell configuration (`.zshrc` or `.bashrc`) to The Hub by adding sourcing lines that connect to the centralized path

## HOW TO INSTALL?
### Determine Your Active Shell
```bash
echo $SHELL # <-- This shows the current shell path>
$SHELL --version # <-- This shows the current shell version>
cat /etc/shells # <-- This shows all available shells on your system>
```

### Locate Shell Configuration Files
```bash
ls -la ~/.zshrc # <-- For Zsh users
ls -la ~/.bashrc # <-- For Bash users
```

### Enable the **Bridge** in Your Shell Config
Add the following lines to your shell configuration file (`~/.zshrc` or `~/.bashrc`), replacing `<path-to-the-hub-repository>` with the actual path to your centralized alias repository.
```bash
echo "======================================================="
echo "⛩️ Entered Bridge in $0"
# WHERE THE CONFIG aka "HUB" LIVES - VERSION CONTROLLED REPO WITH CONFIGURATION
# DO NOT CHANGE THE VARIABLE NAME "CONFIG_PATH"
CONFIG_PATH="<path-to-the-hub-repository>"
# THE ACTUAL FILE TO SOURCE - THIS CONTAINS THE LIST OF ALIAS FILES TO LOAD
CONFIG_FILE="$CONFIG_PATH/source_manager.sh"
echo "🚀 Forwarding to the Hub at $CONFIG_FILE"
source "$CONFIG_FILE"
echo "======================================================="
```

### Flow Diagram
```plaintext
Shell Startup
   ↓
.zshrc / .bashrc
   ↓
Bridge Block
   ↓
source_manager.sh
   ↓
Loop: source each alias file in ALIASES_DIR
   ↓
Aliases/functions loaded in shell
```