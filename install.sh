#!/bin/sh

echo "Setting up your Mac ❤️..."

# Check for Oh My Zsh and install if we don't have it
#if ! [ -d ~/.oh-my-zsh ]; then
#  echo "Installing Oh My ZSH"
#  /bin/sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/HEAD/tools/install.sh)"
#else
#  echo "Oh My ZSH is already installed"
#fi

# Check for Homebrew and install if we don't have it
if test ! $(which brew); then
  echo "Installing Homebrew"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
  echo "Homebrew is already installed"
fi

# Create a Projects directory
mkdir $HOME/Projects

# Create symlinks
source $HOME/Projects/dotfiles/symlinks.sh

# Update Homebrew recipes
brew update

# Install all the dependencies with bundle (See Brewfile)
brew tap homebrew/bundle
# brew tap homebrew/cask-drivers
brew bundle --file $HOME/Projects/dotfiles/Brewfile

# Set default MySQL root password and auth type. (not using in favour of dbngin app)
# brew services restart mysql
# mysql -u root -e "ALTER USER root@localhost IDENTIFIED WITH mysql_native_password BY 'password'; FLUSH PRIVILEGES;"

# Check for NVM and install if we don't have it
if ! [ -d ~/.nvm ]; then
  echo "Installing NVM"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh)"
else
  echo "NVM is already installed"
fi

# Install PHP extensions with PECL
# pecl install redis xdebug
pecl install xdebug

# Install global Composer packages
# composer global require laravel/installer laravel/valet beyondcode/expose roave/security-advisories:dev-latest
# composer global require laravel/installer laravel/valet beyondcode/expose
composer global require laravel/installer beyondcode/expose

# Install Laravel Valet
# $HOME/.composer/vendor/bin/valet install

# Clone Github repositories	(not currently used)
# source clone.sh

# Reload .zshrc
source ~/.zshrc

echo "Finished setting up your Mac ❤️. Continue to install macOS preferences and reload the shell..."

# Set macOS preferences
# We will run this last because this will reload the shell
source ~/Projects/dotfiles/.macos

exit 0
