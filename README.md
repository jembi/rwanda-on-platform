# rwanda-on-platform
This repo contains the required config to start up a Hapi FHIR server alongside the OpenHIM and a reverse proxy to be used for Rwanda Platform purposes.

## Prerequisites:
1. Docker
1. An Active Docker Swarm

## Getting Started:
1. Check that you have an active docker swarm running on the respective environment. `docker info | grep Swarm`
1. If no swarm is running, you can start a swarm with `docker swarm init`.
1. Ensure that you have the correct IG URL specified in the respective environment variable file (e.g. `.env.local`). The variable to set is `FHIR_IG_URL`.
1. Run `./get-cli.sh` to download the latest release of the CLI. You can download only the specific CLI for your operating system by providing it as a parameter. (e.g. `./get-cli.sh macos`)
1. Run the relevant deploy script. (e.g. `./deploy-local.sh`)
   
## Reloading the IG:

There are scripts in the root folder of this repo to assist in reloading the IG in HAPI-FHIR.

NB: This process will clear the Hapi-FHIR Postgres database.
### Local:
1. Run `./replace-ig-local.sh` which will run the Jembi Platform twice, the first run will remove the existing Hapi-FHIR and Postgres services, while the second run will recreate the services as well as rerun the importing of the FHIR IG specified in `FHIR_IG_URL`
### QA:
NB: Only a person that has SSH access to the server will be able to run this command.
1. Run `DOCKER_HOST=ssh://ubuntu@fhir.Rwanda Platform.jembi.cloud ./replace-ig-qa.sh` which will run the Jembi Platform twice, the first run will remove the existing Hapi-FHIR and Postgres services, while the second run will recreate the services as well as rerun the importing of the FHIR IG specified in `FHIR_IG_URL`

## Tips:

The `./depoy-{environment}.sh` scripts will default to using the `Linux` binary and running the `init` deploy action. This can be overriden by supplying parameters to the script. The first parameter being the action and the second parameter being the operating system. (e.g. `./deploy-local.sh remove macos` will run the remove command using the MacOS binary)
### Local:
1. The `./deploy-local.sh` and `./replace-ig-local.sh` scripts will make use of Platform profiles which are specified to configure the services for local development purposes exposing the ports of these services and allowing access to the Hapi-FHIR GUI.
### QA:
1. The `./deploy-qa.sh` and `./replace-ig-qa.sh` scripts will make use of Platform profiles which are specified to configure the services for QA purposes, securing the services and disallowing access to the Hapi-FHIR GUI.

## Deploying specific version of fhir

To deploy a specific version of FHIR, use the environment variable FHIR_VERSION. Default value is R4
