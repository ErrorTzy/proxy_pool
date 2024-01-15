#!/usr/bin/env bash
${PWD}/.venv/bin/python3 proxyPool.py server &
${PWD}/.venv/bin/python3 proxyPool.py schedule
