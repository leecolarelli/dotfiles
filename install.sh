#!/bin/sh

if test "$(uname)" = "Darwin"
then
    echo "Setting up your Mac..."
elif test "$(expr substr $(uname -s) 1 5)" = "Linux"
then
    echo "Setting up your Linux OS..."
fi

# Set up symlinks
source makesymlinks.sh

# Install homebrew
source homebrew/install.sh

# Install brew applications
source homebrew/brew.sh

exit 0