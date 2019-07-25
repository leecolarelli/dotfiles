#!/bin/sh
#
# # Update Homebrew recipes
brew update

# Install all our dependencies with bundle (See Brewfile)
brew tap homebrew/bundle
brew bundle --file="homebrew/Brewfile"