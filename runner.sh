#!/bin/bash
now=$(date +"%T")
echo "Current time : $now"

script_full_path="${BASH_SOURCE}"
script_name=`basename "$0"`
script_name_len=${#script_name}
current_path=${script_full_path: :-$script_name_len}

echo "script name $script_name"
echo "script name len $script_name_len"
echo "script full path $script_full_path"
echo "current path $current_path"

export PYTHONPATH="$current_path/py"
$current_path/venv/bin/python "$current_path/py/protocols/iec_104/iec_104_client.py" > "$current_path/bash_out.txt"
