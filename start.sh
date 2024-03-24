#!/bin/bash

# Remove backslashes from the PORT variable
PORT_STR=${PORT//\\/}

# Start your application with the corrected port
gunicorn --bind 0.0.0.0:$PORT_STR app:app
