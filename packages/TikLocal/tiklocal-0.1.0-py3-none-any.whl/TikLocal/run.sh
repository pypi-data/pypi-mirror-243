#!/bin/bash
#
gunicorn -w 2 app:app
