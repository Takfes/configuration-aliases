# oh-my-zsh Documentation

## Resources
* [oh-my-zsh github](https://github.com/ohmyzsh/ohmyzsh)
* [oh-my-zsh website](https://ohmyz.sh/)
* [oh-my-zsh themes](https://github.com/ohmyzsh/ohmyzsh/wiki/Themes)
* [oh-my-zsh plugins](https://github.com/ohmyzsh/ohmyzsh/wiki/Plugins)

## Example Configuration (`.zshrc`)
```bash
export ZSH="$HOME/.oh-my-zsh"
# if using powerlevel10k, enable `setup_p10k.sh` through the `source_manager.sh` file
ZSH_THEME="powerlevel10k/powerlevel10k" # requires p10k installation
plugins=(zsh-autosuggestions zsh-syntax-highlighting)
mytimer source $ZSH/oh-my-zsh.sh
```