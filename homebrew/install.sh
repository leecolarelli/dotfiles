#!/bin/sh
#
# Install Homebrew

# Check for Homebrew
if ! type "brew" > /dev/null;
then
  echo "Installing Homebrew for you."

  # Install the correct homebrew for each OS type
  if test "$(uname)" = "Darwin"
  then
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  elif test "$(expr substr $(uname -s) 1 5)" = "Linux"
  then
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install)"
  fi

elif type "brew" > /dev/null;
then
  echo "Homebrew is already installed."

fi
