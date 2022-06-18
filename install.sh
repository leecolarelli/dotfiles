#!/bin/sh

echo "Setting up your Mac ❤️..."

# Check for Oh My Zsh and install if we don't have it
if ! [ -d ~/.oh-my-zsh ]; then
  echo "Installing Oh My ZSH"
  /bin/sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/HEAD/tools/install.sh)"
else
  echo "Oh My ZSH is already installed"
fi

# Check for Homebrew and install if we don't have it
if test ! $(which brew); then
  echo "Installing Homebrew"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
else
  echo "Homebrew is already installed"
fi

# Create symlinks
./symlinks.sh

# Update Homebrew recipes
brew update

# Install all the dependencies with bundle (See Brewfile)
brew tap homebrew/bundle
# brew tap homebrew/cask-drivers
brew bundle --file $HOME/.dotfiles/Brewfile

# Set default MySQL root password and auth type.
brew services restart mysql
mysql -u root -e "ALTER USER root@localhost IDENTIFIED WITH mysql_native_password BY 'password'; FLUSH PRIVILEGES;"

# Check for NVM and install if we don't have it
if ! [ -d ~/.nvm ]; then
  echo "Installing NVM"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh)"
else
  echo "NVM is already installed"
fi

# Install PHP extensions with PECL
pecl install redis xdebug

# Install global Composer packages
composer global require laravel/installer laravel/valet beyondcode/expose

# Install Laravel Valet	
$HOME/.composer/vendor/bin/valet install

# Create a Sites directory
mkdir $HOME/Sites

# Clone Github repositories	(not currently used)
# ./clone.sh

# Reload .zshrc
source ~/.zshrc

# Set macOS preferences
# We will run this last because this will reload the shell
source .macos

exit 0
