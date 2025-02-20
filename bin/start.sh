#!/bin/bash

gunicorn gray.wsgi --log-file -

daphne --bind 127.0.0.1 -p 8001 gray.asgi:application