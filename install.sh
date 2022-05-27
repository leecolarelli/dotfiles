#!/bin/sh

echo "Setting up your Mac ❤️..."

# Check for Oh My Zsh and install if we don't have it
if test ! $(which omz); then
  /bin/sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/HEAD/tools/install.sh)"
fi

# Check for Homebrew and install if we don't have it
if test ! $(which brew); then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

  echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> $HOME/.zprofile
  eval "$(/opt/homebrew/bin/brew shellenv)"
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
if test ! $(which nvm); then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh)"
fi

# Install PHP extensions with PECL
pecl install imagick redis xdebug

# Install global Composer packages
/usr/local/bin/composer global require laravel/installer laravel/valet beyondcode/expose

# Create a Sites directory
mkdir $HOME/Sites

# Clone Github repositories	(not currently used)
# ./clone.sh

# Install Pure theme
# Did not work on m1 globally anymore
#npm install --global pure-prompt
git clone https://github.com/sindresorhus/pure.git "$HOME/.dotfiles/plugins/pure"

# Set macOS preferences
# We will run this last because this will reload the shell
source .macos

exit 0