#!/bin/sh
rasa train --config skills/global/zh/config.yml --domain skills --data skills --num-threads 12