CONFIG=${XDG_CONFIG_HOME:-$HOME/.config}
cd $CONFIG/polybar/
pkill -9 polybar
polybar topbar &>/dev/null
