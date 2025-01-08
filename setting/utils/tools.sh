#!/bin/bash
function check_config(){
	CONF=$1
	FLAG=$(ls ${CONF} 2>/dev/null)
	if [[ -z $FLAG ]];then 
		printd "Couldn't find configuration (${CONF})" Cy; 
		exit
	fi
}
function check_jq(){
	# Install pre-requirement
	if [[ -z $(which jq) ]];then
		printd "Installing jq for parsing JSON configuration .... " Cy
		# sudo apt-get install jq -yqq
		BASEDIR=$(dirname $0)
		chmod u+x ${BASEDIR}/tools/install-jq.sh
		${BASEDIR}/tools/install-jq.sh

		if [[ -z $(which jq) ]];then
			printd "Install jq failed" R
			exit 1
		fi
	fi
}



function update_nginx_listen_port() {
    local config_path=$1
    local new_port=$2

    if [ ! -f "$config_path" ]; then
        echo "Nginx configuration file not found at $config_path"
        return 1
    fi

    sed -i "s/listen [0-9]\+;/listen $new_port;/" "$config_path"

    if grep -q "listen $new_port;" "$config_path"; then
        echo "Updated 'listen' port to $new_port in $config_path"
        return 0
    else
        echo "Failed to update 'listen' port in $config_path"
        return 1
    fi
}

function update_compose_env() {
	local args=("$@")
	local file=$1

	if [[ $# -lt 2 ]]; then usage; fi
	
	for ((i=1; i<${#args[@]}; i++)); do
		
		local pair=(${args[i]//=/ })
		pair[1]="${pair[1]//\//\\/}"
		sed -Ei "s/(.*${pair[0]}=).*/\1${pair[1]}/g" $file
		echo "Replacing: ${pair[0]} with ${pair[1]}" 

	done
}
function update_docker_compose_port() {
    local file_path="$1"       # file path
    local service_name="$2"  # service name
    local new_port="$3"        # new out ports


    local last_line="Null"
    local find_server_indent=0
    local find_component_indent=0
    local service_indent=0
    local component_indent=0
    local in_service=0
    local in_ports_line=0
    local success_flag=0
    local tmp_file
    tmp_file="$(mktemp)"

    while IFS= read -r line || [[ -n $line ]]; do
        # echo "$line"
        local indent="${line%%[^[:space:]]*}"
        local current_indent=${#indent}
        local output_line="$line"

        if [[ $find_server_indent -eq 0 || $find_component_indent -eq 0 ]]; then
            if [[ "$find_server_indent" -eq 1 ]]; then
                component_indent=$current_indent
                find_component_indent=1
            fi

            if [[ "$last_line" == *"networks"* ]]; then
                service_indent=$current_indent
                find_server_indent=1
            fi
            
        else
            if [[ "$in_service" -eq 0 ]]; then
                if [[ "$service_indent" -eq "$current_indent" ]]; then
                    cleaned_name=$(echo "$line" | sed 's/[^[:alnum:]_]//g')
                    # echo $cleaned_name
                    if [[ "$cleaned_name" == "$service_name" ]]; then 
                        in_service=1
                        # echo "Find target services: $line "
                    fi
                fi
            elif [[ "$in_ports_line" -eq 0 ]]; then
                if [[ "$component_indent" -eq "$current_indent" ]]; then
                    cleaned_name=$(echo "$line" | sed 's/[^[:alnum:]]//g')
                    
                    if [[ "$cleaned_name" == "ports" ]]; then 
                        
                        in_ports_line=1
                        # echo "Find location of ports: $line "
                    fi
                fi
            else
                if [[ "$line" =~ ^([[:space:]]*)-[[:space:]]*\"?([0-9]+):([0-9]+)\"?(.*)$ ]]; then

                    local leading_spaces="${BASH_REMATCH[1]}"
                    local left_port="${BASH_REMATCH[2]}"
                    local right_port="${BASH_REMATCH[3]}"
                    local trailing_part="${BASH_REMATCH[4]}"


                    local new_line="${leading_spaces}- \"${new_port}:${right_port}\"${trailing_part}"
                    output_line="$new_line"
                    success_flag=1

                fi
                
                in_service=0
                in_ports_line=0

            fi

        fi
        echo "$output_line" >> "$tmp_file"
        last_line=$line

        
    done < "$file_path"
    
    mv "$tmp_file" "$file_path"
    chmod 777 "$file_path"
    if [[ "$success_flag" -eq 0 ]]; then
        echo "Failed update $service_name with new port : $new_port"
    else
        echo "Success update $service_name with new port : $new_port"
    fi
}


