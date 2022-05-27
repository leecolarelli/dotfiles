#!/bin/sh

echo "Creating symlinks..."

# Removes .zshrc from $HOME (if it exists) and symlinks the .zshrc file from the .dotfiles
rm -rf $HOME/.zshrc
ln -s $HOME/.dotfiles/.zshrc $HOME/.zshrc

# Removes .gitignore from $HOME (if it exists) and symlinks the .gitignore_global file from the .dotfiles
rm -rf $HOME/.gitignore
ln -s $HOME/.dotfiles/.gitignore_global $HOME/.gitignore

# Removes .gitconfig from $HOME (if it exists) and symlinks the .gitconfig file from the .dotfiles
rm -rf $HOME/.gitconfig
ln -s $HOME/.dotfiles/.gitconfig $HOME/.gitconfig

# Removes .mackup.cfg from $HOME (if it exists) and symlinks the .mackup.cfg file from the .dotfiles
rm -rf $HOME/.mackup.cfg
ln -s $HOME/.dotfiles/.mackup.cfg $HOME/.mackup.cfg

echo "Symlinks created..."