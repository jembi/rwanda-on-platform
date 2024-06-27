local cwd=$(dirname ${BASH_SOURCE[0]})
source "$cwd/../importer.sh"

local stack="${OPENHIM_MAPPING_MEDIATOR_STACKNAME:-openhim-mapping-mediator}"
local target=$(basename "$cwd")
importer::deploy_importer $stack $target "docker-compose.config.yml"
