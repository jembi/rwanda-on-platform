#!/bin/bash

declare ACTION=""
declare MODE=""
declare COMPOSE_FILE_PATH=""
declare UTILS_PATH=""
declare STACK="rwanda-custom-mapping-mediator"

function init_vars() {
  ACTION=$1
  MODE=$2

  COMPOSE_FILE_PATH=$(
    cd "$(dirname "${BASH_SOURCE[0]}")" || exit
    pwd -P
  )

  UTILS_PATH="${COMPOSE_FILE_PATH}/../../utils"

  readonly ACTION
  readonly MODE
  readonly COMPOSE_FILE_PATH
  readonly UTILS_PATH
  readonly STACK
}

# shellcheck disable=SC1091
function import_sources() {
  source "${UTILS_PATH}/docker-utils.sh"
  source "${UTILS_PATH}/log.sh"
}

function build_local_image() {
  if docker image inspect $STACK >/dev/null 2>&1; then
    log info "Image exists locally. Using built $STACK image"
  else
    log info "Image does not exist locally. Building custom $STACK image"

    docker build -t $STACK -f "${COMPOSE_FILE_PATH}/Dockerfile" $COMPOSE_FILE_PATH
  fi
}

function initialize_package() {
  local package_dev_compose_filename=""

  (
    docker::deploy_service $STACK "${COMPOSE_FILE_PATH}" docker-compose.yml
  ) || {
    log error "Failed to deploy package"
    exit 1
  }
}

main() {
  init_vars "$@"
  import_sources
  build_local_image

  if [[ "${ACTION}" == "init" ]] || [[ "${ACTION}" == "up" ]]; then
    log info "Running package in Single node mode"

    initialize_package
  elif [[ "${ACTION}" == "down" ]]; then
    log info "Scaling down package"

    docker::scale_services $STACK 0
  elif [[ "${ACTION}" == "destroy" ]]; then
    log info "Destroying package"

    # destroy_package
    docker::stack_destroy $STACK
  else
    log error "Valid options are: init, up, down, or destroy"
  fi
}

main "$@"
