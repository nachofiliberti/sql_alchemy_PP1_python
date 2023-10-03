#!/bin/bash

#run your first command (e.g., flask db init)
flask db init

# run your second command (e.g., another command)
flask db migrate -m "initial migration"

#run your third command (e.g., yet another command)
flask db upgrade

# start your flask application
gunicorn app:app --bind 0.0.0.0:5005