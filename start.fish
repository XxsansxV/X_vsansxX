#!/usr/bin/env fish
# 
# runs discord bot with systemd inhibit and without having to source

source .venv/bin/activate.fish

systemd-inhibit --what=idle:sleep --why="X_vsansxX Discord Bot" python ./bot.py
