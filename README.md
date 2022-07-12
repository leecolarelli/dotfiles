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
- Did you update [mackup](https://github.com/lra/mackup) to the latest version
  and run `mackup backup`?

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

Then we need to clone this dotfiles repository into our user folder.

`git clone https://github.com/leecolarelli/dotfiles.git ~/.dotfiles`

### 3. Run Installation Script

Now we can run the main installation script...

```zsh
~/.dotfiles/install.sh
```

### 4. Restore Mackup settings

Restore your mac settings by running `mackup restore`

### 5. Restart your computer

Restart your computer to finalize the process

