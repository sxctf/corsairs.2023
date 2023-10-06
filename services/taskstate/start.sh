#!/bin/bash
gunicorn -w 3 -b 0.0.0.0:7000 --log-level=info app:app