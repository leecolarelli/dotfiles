#!/bin/sh

echo "Creating symlinks..."

# Removes .zshrc from $HOME (if it exists) and symlinks the .zshrc file from the dotfiles
rm -rf $HOME/.zshrc
ln -s $HOME/Projects/dotfiles/.zshrc $HOME/.zshrc

# Removes .gitconfig from $HOME (if it exists) and symlinks the .gitconfig file from the dotfiles
rm -rf $HOME/.gitconfig
ln -s $HOME/Projects/dotfiles/.gitconfig $HOME/.gitconfig

# Removes .config/ghostty/config from $HOME (if it exists)
# and symlinks the .config/ghostty/config file from the dotfiles
rm -rf $HOME/.config/ghostty/config
mkdir -p $HOME/.config/ghostty
ln -s $HOME/Projects/dotfiles/.config/ghostty/config $HOME/.config/ghostty/config

echo "Symlinks created..."
