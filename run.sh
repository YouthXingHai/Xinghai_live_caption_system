#!/bin/bash

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_DIR"

LOG_FILE="$PROJECT_DIR/app.log"

echo "-----------------------------------" >> $LOG_FILE
echo "[$(date)] Startup sequence initiated..." >> $LOG_FILE

if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment 'venv' not found!" | tee -a $LOG_FILE
    exit 1
fi


source venv/bin/activate

echo "tarting Uvicorn service..." | tee -a $LOG_FILE

exec python -m uvicorn server.main:app --reload --host 0.0.0.0 2>&1 | tee -a $LOG_FILE /dev/tty1