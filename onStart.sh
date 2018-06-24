#!/bin/bash

# Script to run on every reboot of ubuntu 
echo "Starting rasa server..."
cd /home/ubuntu/VoiceOS
tmux new -s "rasa-server" -d
tmux send-keys -t "rasa-server" "python3 -m rasa_nlu.train -c config_spacy.json" C-m
tmux send-keys -t "rasa-server" "python3 -m rasa_nlu.server" C-m

# tmux a -t rasa-server
echo "Rasa server started in tmux"

exit 0