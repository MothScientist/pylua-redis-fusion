#!/bin/sh

COLOR_RESET="\033[0m" # color reset
COLOR_GREEN="\033[32m"
COLOR_RED="\033[31m"
COLOR_CYAN="\033[36m"

echo "${COLOR_CYAN}SwiftPipRedis${COLOR_RESET}"

echo "${COLOR_GREEN}Git clone${COLOR_RESET}"
if ! git clone https://github.com/MothScientist/SwiftPipRedis.git; then
    echo "${COLOR_RED}Error installing SwiftPipRedis${COLOR_RESET}"
    exit 1
fi

if [ "$1" = "--requirements-install" ]; then
    echo "${COLOR_GREEN}Upgrade pip${COLOR_RESET}"
    if ! pip install --upgrade pip; then
        echo "${COLOR_RED}Error upgrading pip${COLOR_RESET}"
        exit 1
    fi

    echo "${COLOR_GREEN}Install requirements.txt${COLOR_RESET}"
    if ! pip install -r requirements.txt; then
        echo "${COLOR_RED}Error installing requirements.txt${COLOR_RESET}"
        exit 1
    fi

    echo "${COLOR_GREEN}Updating requirements.txt${COLOR_RESET}"
    if ! pip freeze > requirements.txt; then
        echo "${COLOR_RED}Error updating requirements.txt${COLOR_RESET}"
        exit 1
    fi
fi

echo "${COLOR_CYAN}The environment has been successfully configured!${COLOR_RESET}"