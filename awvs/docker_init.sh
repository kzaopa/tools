#!/usr/bin/env bash

# set -ex

clear
OS="$(uname -s)"
Arch="$(uname -m)"
Tag="$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep tag_name | cut -d '"' -f 4)"

DockerInstall(){
    echo " ╷───────────────────────────╷"
    echo " │    OS ${OS}              │"
    echo " │    Arch ${Arch}             │"
    echo " │    Docker Version: ${Tag} │"
    echo " ╵–––––––––––––––––––––––––––╵"
    case "${OS}" in
        Linux)
            echo " Install Docker for Linux"
            curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
            sudo systemctl enable docker
            sudo systemctl start docker
            sudo usermod -aG docker "$USER"
        ;;
        Darwin)
            echo " Docker Error: Docker Desktop https://www.docker.com/products/docker-desktop"
            if [ "${OS}" == "Darwin" ] && [ "${Arch}" == "arm64" ]; then
                Arch="aarch64"
            fi
        ;;
        *)
        echo " Unknown OS: ${OS}}"
        exit 1
        ;;
    esac
}

DockerComposeInstall(){
    echo " Downloading docker-compose..."
    sudo curl -sLm 10 "https://github.com/docker/compose/releases/download/${Tag}/docker-compose-${OS}-${Arch}" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
}

DockerInstall

DockerComposeInstall