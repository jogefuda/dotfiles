#!/bin/sh
card=alsa_output.pci-0000_00_1b.0.analog-stereo

status=$(pactl list sinks 2>/dev/null | awk -v card=$card '
	/^Sink/ {
		if (cf==1) exit;
		getline; getline;
		if ($2==card) cf=1;
	}
	cf && /^\tPort/ {
		pf = 1; i = 0; next;
	}
	cf && /^\tActive Port/{
		pf = 0;
		activePort=$3;
	}
	cf && pf {
		ports = ports substr($1, 0, index($1, ":")-1) " ";
	}
	END {
		print activePort"#"ports;
	}
')

declare -a ports
active_port=${status%#*}
ports=(${status#*#})

arr_index () {
	declare -a arr
	local arr=(${@:2})
	for i in "${!arr[@]}"; do
		[[ "$1" == ${arr[i]} ]] && echo "$i"
	done
}
# current port index
idx=$(arr_index $active_port ${ports[@]})
# card ports count
len=${#ports[@]}
next=$(((idx+1) % 2))
pactl set-sink-port $card ${ports[next]}
