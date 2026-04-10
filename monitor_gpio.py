from periphery import GPIO
import time
import subprocess
import os

button = GPIO("/dev/gpiochip0", 18, "in")
led = GPIO("/dev/gpiochip0", 203, "out")

process = None  # 用于存储运行中的进程对象
is_running = False


def start_app():
    global process, is_running
    print("\n[系统通知] 正在启动 Xinghai Live Caption System...")
    cmd = "/home/pi/Xinghai_live_caption_system/run_app.sh"
    process = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
    is_running = True
    led.write(True)


def stop_app():
    global process, is_running
    print("\n[系统通知] 正在停止系统...")
    if process:
        os.killpg(os.getpgid(process.pid), 9)
        process = None
    is_running = False
    led.write(False)

print("GPIO 监控已启动，等待按键操作...")

try:
    last_state = button.read()
    while True:
        current_state = button.read()

        if current_state != last_state:
            if not current_state:
                if not is_running:
                    start_app()
                else:
                    stop_app()

                # 消抖
                time.sleep(0.5)

            last_state = current_state

        time.sleep(0.05)

except KeyboardInterrupt:
    if is_running:
        stop_app()
finally:
    button.close()
    led.close()