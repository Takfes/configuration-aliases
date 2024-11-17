
# PROMPT - STARTSHIP
$ENV:STARSHIP_CONFIG = "$HOME\.starship\starship.toml"
$ENV:STARSHIP_DISTRO = "者 xcad"
Invoke-Expression (&starship init powershell)

# # PROMPT - OH-MY-POSH
# (@(& 'C:/Users/FessasP/AppData/Local/Programs/oh-my-posh/bin/oh-my-posh.exe' init pwsh --config='C:\Users\FessasP\.oh-my-posh-themes\cloud-context.omp.json' --print) -join "`n") | Invoke-Expression
# (@(& 'C:/Users/FessasP/AppData/Local/Programs/oh-my-posh/bin/oh-my-posh.exe' init pwsh --config='C:\Users\FessasP\.oh-my-posh-themes\jblab_2021.omp.json' --print) -join "`n") | Invoke-Expression

# SOURCE ALIAS FILES
. "C:\Users\FessasP\AliasGit.ps1"
. "C:\Users\FessasP\AliasKube.ps1"

# AUTOFILL WITH PSReadLine
Set-PSReadLineOption -PredictionSource History
Set-PSReadLineOption -PredictionViewStyle ListView

# ALIASES
function sck { Set-Location -Path 'C:\Users\FessasP\Desktop\school' }

function src {
    . $PROFILE
    Write-Output "Loading ... C:\Users\FessasP\OneDrive - Titan Cement Company SA\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
}

function qwe {
    . $PROFILE
    Clear-Host
}

