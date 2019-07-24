# Lee's dotfiles

These are my personal dotfiles. Use anything you want but try to know what things do first :)

I aim to have dotfiles which are usable on both MacOS and Linux.

## Installation

### MacOS

For installation on a new MacOS machine first run the code below as we need the latest Xcode Command Line Tools installed, as it provides us with `git` and `make`.

```
sudo softwareupdate -i -a
xcode-select --install
```

I like to keep all my repositories and projects in a ~/projects folder so on a new installation...

`mkdir -p ~/projects`

Then we need to clone this dotfiles repository into the projects folder.

`git clone https://github.com/leecolarelli/dotfiles.git ~/projects/dotfiles`

Now we can set up symlinks between the home directory and the dotfiles repository using the makesymlinks.sh file. The `source` command is used to run the .sh file.

```
cd ~/projects/dotfiles
source makesymlinks.sh
```
