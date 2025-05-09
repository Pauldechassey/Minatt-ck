#!/bin/bash

for ui_file in *.ui; do
    if [[ -f "$ui_file" ]]; then
        base_name=$(basename "$ui_file" .ui)
        output_file="ui_${base_name}.py"
        pyside6-uic "$ui_file" -o "$output_file"
        echo "Converted: $ui_file -> $output_file"
    fi
done
