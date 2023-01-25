#-----------------------------------------------------------------------------------#
#	*START* Base
#-----------------------------------------------------------------------------------#

# Reload bash
alias reload_bash=". ~/.dotfiles/.zshrc"

# Be gentle
alias please="sudo"

#-----------------------------------------------------------------------------------#
#	*END* Base
#-----------------------------------------------------------------------------------#


#-----------------------------------------------------------------------------------#
#	*START* Navigation
#-----------------------------------------------------------------------------------#

# Easier navigation: .., ..., ~ and -
alias ..="cd .."
alias cd..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias .....="cd ../../../.."

#-----------------------------------------------------------------------------------#
#	*END* Navigation
#-----------------------------------------------------------------------------------#


#-----------------------------------------------------------------------------------#
#	*START* GOTO
#-----------------------------------------------------------------------------------#

alias home="cd ~/"
alias gotodotfiles="cd ~/.dotfiles"
alias gotosites="cd ~/Sites"

alias subldotfiles="subl ~/.dotfiles"

#-----------------------------------------------------------------------------------#
#	*END* GOTO
#-----------------------------------------------------------------------------------#


#-----------------------------------------------------------------------------------#
#	*START* Mac MySQL
#-----------------------------------------------------------------------------------#

alias killmysql='killall -9 mysqld'

#-----------------------------------------------------------------------------------#
#	*END* Mac MySQL
#-----------------------------------------------------------------------------------#


#-----------------------------------------------------------------------------------#
#	*START* GIT
#-----------------------------------------------------------------------------------#
alias g='git'
alias gs='git status'
alias nope="git reset --hard && git clean -df"
alias gaa='git add --all'
alias glog="git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

alias gac="git add -A && git commit -m"
alias gpc="git push origin HEAD"
#-----------------------------------------------------------------------------------#
#	*END* GIT
#-----------------------------------------------------------------------------------#


#-----------------------------------------------------------------------------------#
#	*START* PHP
#-----------------------------------------------------------------------------------#

alias art='php artisan'
alias mfs='php artisan migrate:fresh --seed'
alias artclearall='php artisan cache:clear && php artisan view:clear && php artisan config:clear'
alias phpstan='vendor/bin/phpstan'
alias phpunit='vendor/bin/phpunit'
alias pint='vendor/bin/pint'
alias clearlog='truncate -s 0 $PWD/storage/logs/laravel.log'
alias clearlogs='truncate -s 0 $PWD/storage/logs/*.log'


#-----------------------------------------------------------------------------------#
#	*END* PHP
#-----------------------------------------------------------------------------------#


#-----------------------------------------------------------------------------------#
#	*START* HOSTS
#-----------------------------------------------------------------------------------#

alias hosts='sudo subl /etc/hosts'
alias vhosts='sudo subl /etc/apache2/extra/httpd-vhosts.conf'

#-----------------------------------------------------------------------------------#
#	*END* HOSTS
#-----------------------------------------------------------------------------------#


#-----------------------------------------------------------------------------------#
#	*START* NETWORK
#-----------------------------------------------------------------------------------#

# IP addresses
alias ip_intern="ipconfig getifaddr en0"
alias ip_extern="curl ipecho.net/plain; echo"


# Enhanced WHOIS lookups
alias whois="whois -h whois-servers.net"

#-----------------------------------------------------------------------------------#
#	*END* NETWORK
#-----------------------------------------------------------------------------------#


#-----------------------------------------------------------------------------------#
#	*START* Search & List
#-----------------------------------------------------------------------------------#

# Detect which `ls` flavor is in use
if ls --color > /dev/null 2>&1; then # GNU `ls`
	colorflag="--color"
else # OS X `ls`
	colorflag="-G"
fi

# List all files colorized in long format
alias l="ls -laF"

# List all files colorized in long format, including dot files
alias la="ls -la ${colorflag}"


# List only directories
alias lsd='ls -l | grep "^d"'

# Always use color output for `ls`
if [[ "$OSTYPE" =~ ^darwin ]]; then
	alias ls="command ls -G"
else
	alias ls="command ls --color"
	export LS_COLORS='no=00:fi=00:di=01;34:ln=01;36:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arj=01;31:*.taz=01;31:*.lzh=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.gz=01;31:*.bz2=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.avi=01;35:*.fli=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.ogg=01;35:*.mp3=01;35:*.wav=01;35:'
fi


#-----------------------------------------------------------------------------------#
#	*END* Search & List
#-----------------------------------------------------------------------------------#


#-----------------------------------------------------------------------------------#
#	*START* FILE HANDLING
#-----------------------------------------------------------------------------------#

# Recursively delete `.DS_Store` files
alias cleanup="find . -name '*.DS_Store' -type f -ls -delete"

# File size
alias fs="stat -f \"%z bytes\""

# Empty the Trash on all mounted volumes and the main HDD
alias emptytrash="sudo rm -rfv /Volumes/*/.Trashes; rm -rfv ~/.Trash"

# Show/hide hidden files in Finder
alias show="defaults write com.apple.finder AppleShowAllFiles -bool true && killall Finder"
alias hide="defaults write com.apple.finder AppleShowAllFiles -bool false && killall Finder"


nd ()
{
    mkdir -p -- "$1" &&
      cd -P -- "$1"
}

#-----------------------------------------------------------------------------------#
#	*END* FILE HANDLING
#-----------------------------------------------------------------------------------#


#-----------------------------------------------------------------------------------#
#	*START* SPECIALS
#-----------------------------------------------------------------------------------#

# Hide/show all desktop icons (useful when presenting)
alias hidedesktop="defaults write com.apple.finder CreateDesktop -bool false && killall Finder"
alias showdesktop="defaults write com.apple.finder CreateDesktop -bool true && killall Finder"

#-----------------------------------------------------------------------------------#
#	*END* SPECIALS
#-----------------------------------------------------------------------------------#