# Lee's dotfiles

These are my personal dotfiles. Use anything you want but try to know what things do first :)

I aim to have dotfiles which are usable on both MacOS and Linux, as I use both. Therefore, several places test for MacOS or Linux and install options based on the operating system.

## Installation

### Clone Dotfiles Repository

To get started we first need a local copy of the dotfiles repository.

If we are on MacOS then we need to access git to be able to clone the repository.

Therefore, for installation on a new MacOS machine first run the code below as we need the latest Xcode Command Line Tools installed, as it provides us with `git` and `make`.

```
sudo softwareupdate -i -a
xcode-select --install
```

I like to keep all my repositories and projects in a ~/projects folder so on a new installation...

`mkdir -p ~/projects`

Then we need to clone this dotfiles repository into the projects folder.

`git clone https://github.com/leecolarelli/dotfiles.git ~/projects/dotfiles`

### Installation Script

Now we can run the main install script...

```
cd ~/projects/dotfiles
source install.sh
```

#### Symlinks

The installation script sets up symlinks between the home directory and the dotfiles repository by calling the makesymlinks.sh file. The `source` command is used to run the .sh file.

`source makesymlinks.sh`

#### Homebrew

The installation script then installs homebrew by running...

`source homebrew/install.sh`

It then installs applications using `brew.sh` and `Brewfile`...

`source homebrew/brew.sh`

