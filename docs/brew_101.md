
# Homebrew: Common Commands

A quick reference for managing packages and casks with [Homebrew](https://brew.sh).

## Listing Packages

- **All installed packages:**  
    ```sh
    brew list
    ```
- **Installed formulae only:**  
    ```sh
    brew list --formula
    ```
- **Installed casks only:**  
    ```sh
    brew list --cask
    ```
- **Show versions of installed packages:**  
    ```sh
    brew list --versions
    ```

## Updating & Upgrading

- **Update Homebrew and formulae:**  
    ```sh
    brew update
    ```
- **Upgrade all packages:**  
    ```sh
    brew upgrade
    ```
- **Upgrade casks only:**  
    ```sh
    brew upgrade --cask
    ```

## Uninstalling

- **Uninstall a formula:**  
    ```sh
    brew uninstall <package>
    ```
- **Uninstall a cask:**  
    ```sh
    brew uninstall --cask <appname>
    ```

## Taps Management

- **List tapped repositories:**  
    ```sh
    brew tap
    ```
- **Add a tap:**  
    ```sh
    brew tap <user/repo>
    ```
- **Remove a tap:**  
    ```sh
    brew untap <user/repo>
    ```

## Outdated Packages

- **List outdated formulae:**  
    ```sh
    brew outdated
    ```
- **List outdated casks:**  
    ```sh
    brew outdated --cask
    ```

