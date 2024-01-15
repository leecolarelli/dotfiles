# Lee's dotfiles

These are my personal dotfiles. Use anything you want but try to know what
things do first :)

## Backup Checklist

- Did you commit and push any changes/branches to your git repositories?
- Did you copy your .env files to a safe place if they are not casual?
- Did you copy your IDE settings? (e.g. PhpStorm)
- Did you backup local databases you need?
- Did you remember to save all important documents from non-cloud directories?
- Did you save all of your work from apps which aren't synced through cloud?

## Installation

### 1. Update macOS to the latest version and install xcode

To get started we first need a local copy of the dotfiles repository.

First run the code below as we need the latest Xcode Command Line Tools
installed, as it provides us with `git`.

```
sudo softwareupdate -i -a
xcode-select --install
```

### 2. Clone Dotfiles Repository

Then we need to clone this dotfiles repository into our Sites folder.

`git clone https://github.com/leecolarelli/dotfiles.git ~/Sites/dotfiles`

### 3. Run Installation Script

Now we can run the main installation script...

```zsh
~/Sites/dotfiles/install.sh
```

### 4. Restart your computer

Restart your computer to finalize the process

