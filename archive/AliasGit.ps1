# ----------------------------- Git Aliases --------------------------

function Git-Status { git status @args }
Set-Alias -Name gs -Value Git-Status

function Git-Checkout-Fzf {
    $branch = git branch | fzf
    if ($null -ne $branch) {
        $branch = $branch.Trim()
        git checkout $branch
    } else {
        Write-Output "No branch selected."
    }
}
Set-Alias -Name gf -Value Git-Checkout-Fzf


# function Git-Push { git push @args }
# Set-Alias -Name gps -Value Git-Push

function Git-Pull { git pull @args }
Set-Alias -Name gpl -Value Git-Pull

function Git-Switch { git switch @args }
Set-Alias -Name gsw -Value Git-Switch

function Git-Checkout-NewBranch { git checkout -b @args }
Set-Alias -Name gcb -Value Git-Checkout-NewBranch

function Git-Branch-All { git branch -a @args }
Set-Alias -Name gba -Value Git-Branch-All

function Git-Branch-Remote { git branch -r @args }
Set-Alias -Name gbr -Value Git-Branch-Remote

function Git-Branch-List { git branch --list @args }
Set-Alias -Name gbl -Value Git-Branch-List
