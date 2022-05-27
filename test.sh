#!/bin/sh

echo "Setting up your Mac ❤️..."

# Check for Oh My Zsh and install if we don't have it
if test ! $(which omz); then
  echo "Installing Oh My ZSH"
  /bin/sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/HEAD/tools/install.sh)"
else
  echo "Oh My ZSH is already installed"
fi

# Check for Homebrew and install if we don't have it
if test ! $(which brew); then
  echo "Installing Homebrew"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

  echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >>$HOME/.zprofile
  eval "$(/opt/homebrew/bin/brew shellenv)"
else
  echo "Homebrew is already installed"
fi

# Create symlinks
./symlinks.sh
