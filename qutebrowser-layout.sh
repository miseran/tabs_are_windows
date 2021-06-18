#!/bin/bash

# Only open layout on empty WS
workspace=$(i3-msg -t get_workspaces \
				| jq -r '.[] | if .focused then .name else empty end')
children=$(i3-msg -t get_tree \
		| jq '.nodes[].nodes[].nodes[] | 
				if .type == "workspace" and .name == "'"$workspace"'" then 
					.nodes | length
				else 
					empty 
				end')

if ((children == 0)); then
	i3-msg append_layout "$XDG_DATA_HOME/i3/layouts/qutebrowser-layout.json"
fi

qutebrowser "$@"
