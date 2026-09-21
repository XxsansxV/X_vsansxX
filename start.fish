#!/usr/bin/env fish
# 
# runs discord bot with systemd inhibit

systemd-inhibit --what=idle:sleep --why="X_vsansxX Discord Bot" python ./bot.py
