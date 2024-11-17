# ----------------------------- Generic --------------------------

function Kubectl { kubectl @args }
Set-Alias -Name k -Value Kubectl

function Kubectl-Get { kubectl get @args }
Set-Alias -Name kg -Value Kubectl-Get

function Kubectl-GetAll { kubectl get --all-namespaces all @args }
Set-Alias -Name kga -Value Kubectl-GetAll

function Kubectl-Describe { kubectl describe @args }
Set-Alias -Name kd -Value Kubectl-Describe

function Kubectl-ApplyFile { kubectl apply -f @args }
Set-Alias -Name kaf -Value Kubectl-ApplyFile

function Kubectl-Exec { kubectl exec -it @args }
Set-Alias -Name kex -Value Kubectl-Exec

function Kubectl-ApiResources { kubectl api-resources @args }
Set-Alias -Name kar -Value Kubectl-ApiResources

function Kubectl-Explain { kubectl explain @args }
Set-Alias -Name ke -Value Kubectl-Explain

# ----------------------------- Context --------------------------

function Kubectl-Config-GetContexts { kubectl config get-contexts @args }
Set-Alias -Name kcl -Value Kubectl-Config-GetContexts

function Kubectl-Config-CurrentContext { kubectl config current-context @args }
Set-Alias -Name kcc -Value Kubectl-Config-CurrentContext

# ----------------------------- Logs --------------------------

function Kubectl-Logs { kubectl logs @args }
Set-Alias -Name kl -Value Kubectl-Logs

function Kubectl-LogsFollow { kubectl logs --follow @args }
Set-Alias -Name klf -Value Kubectl-LogsFollow

# ----------------------------- Custom Functions --------------------------

function kcx {
    # Get a list of available Kubernetes contexts
    $contexts = kubectl config get-contexts -o name

    # Check if there are any contexts available
    if ($contexts.Length -eq 0) {
        Write-Output "No Kubernetes contexts found."
        return
    }

    # Display available contexts
    Write-Output "Available Kubernetes Contexts:"
    $contexts

    # Use fzf to select a context
    $selected_context = $contexts | fzf

    # Check if a context was selected
    if ($null -eq $selected_context) {
        Write-Output "No context selected."
        return
    }

    # Use the selected context
    kubectl config use-context $selected_context
    Write-Output "The '$selected_context' context is now active."
}
