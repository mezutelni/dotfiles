#!/usr/bin/env bash

set -euxo pipefail

pacman_list="$HOME/.config/pacman.list"

pacman -Qqe > $pacman_list

commit_msg="Auto pacman.list push at $(date +'%Y-%m-%d %H:%M:%S')"

dotfiles add "$pacman_list"
dotfiles commit -m"$commit_msg" 

