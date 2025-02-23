#!/bin/bash

daphne --bind 127.0.0.1 -p 8000 gray.asgi:application

# gunicorn gray.wsgi --log-file -