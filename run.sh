#!/bin/bash

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_DIR"

LOG_FILE="$PROJECT_DIR/app.log"

echo "-----------------------------------" >> $LOG_FILE
echo "[$(date)] 启动开始..." >> $LOG_FILE

if [ ! -d "venv" ]; then
    echo "错误: 未发现虚拟环境 venv 文件夹！" | tee -a $LOG_FILE
    exit 1
fi


source venv/bin/activate

echo "正在启动Xinghai Live Caption System..." | tee -a $LOG_FILE

exec python -m uvicorn server.main:app --reload --host 0.0.0.0 >> $LOG_FILE 2>&1 | tee /dev/tty1