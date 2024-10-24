#!/bin/bash
cd code
gunicorn app:server -b 0.0.0.0:8050