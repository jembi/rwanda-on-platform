#!/bin/bash

action="${1:-init}"
operating_system=${2:-linux}
valid_actions=("init" "i" "destroy" "remove" "r" "down" "d" "up" "u")

# shellcheck disable=SC2076
if [[ ! " ${valid_actions[*]} " =~ " ${action} " ]]; then
  echo "Invalid action has been specified."
  echo "Usage: deploy-qa.sh {action} [linux|macos|windows]"
  exit 0
fi

case ${operating_system} in
linux)
  echo "Running with the Linux CLI binary"
  ./instant-linux package "$action" --profile=qa --concurrency=10 "${@:3}"
  exit 0
  ;;
macos)
  echo "Running with the MacOS CLI binary"
  ./instant-macos package "$action" --profile=qa --concurrency=10 "${@:3}"
  exit 0
  ;;
windows)
  echo "Running with the Windows CLI binary"
  ./instant.exe package "$action" --profile=qa --concurrency=10 "${@:3}"
  exit 0
  ;;
--help)
  echo "Usage: deploy-qa.sh {action} [linux|macos|windows]"
  exit 0
  ;;
esac

echo "Incorrect parameters, usage: deploy-qa.sh {action} [linux|macos|windows]"
