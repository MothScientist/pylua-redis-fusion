#!/bin/sh

COLOR_RESET="\033[0m" # color reset
COLOR_GREEN="\033[32m"
COLOR_RED="\033[31m"
COLOR_CYAN="\033[36m"

echo "${COLOR_CYAN}SwiftPipRedis${COLOR_RESET}"

echo "${COLOR_GREEN}Git clone${COLOR_RESET}"
git clone https://github.com/MothScientist/SwiftPipRedis.git

echo "${COLOR_GREEN}Install Lua 5.4${COLOR_RESET}"
sudo add-apt-repository ppa:kevinhwang91/lua -y
sudo apt update
sudo apt install -y lua5.4

# shellcheck disable=SC2181
if [ $? -ne 0 ]; then
    echo "${COLOR_RED}Error installing Lua 5.4${COLOR_RESET}"
    exit 1
fi

if [ "$1" = "--requirements-install" ]; then
    echo "${COLOR_GREEN}Upgrade pip${COLOR_RESET}"
    pip install --upgrade pip

    # shellcheck disable=SC2181
    if [ $? -ne 0 ]; then
        echo "${COLOR_RED}Error upgrading pip${COLOR_RESET}"
        exit 1
    fi

    echo "${COLOR_GREEN}Install requirements.txt${COLOR_RESET}"
    pip install -r requirements.txt

    # shellcheck disable=SC2181
    if [ $? -ne 0 ]; then
        echo "${COLOR_RED}Error installing requirements.txt${COLOR_RESET}"
        exit 1
    fi
fi

echo "${COLOR_CYAN}The environment has been successfully configured!${COLOR_RESET}"