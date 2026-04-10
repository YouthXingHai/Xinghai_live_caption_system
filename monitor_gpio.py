from periphery import GPIO
import time
import subprocess
import os

os.system("sudo chmod 666 /dev/tty1")

def log_to_screen(msg):
    formatted_msg = "\n[LOG] {}\n".format(msg)
    try:
        with open("/dev/tty1", "w") as f:
            f.write(formatted_msg)
    except:
        pass
    print(msg)

try:
    btn_toggle = GPIO("/dev/gpiochip1", 4, "in")  # Pin 4: 开关切换
    btn_shutdown = GPIO("/dev/gpiochip1", 3, "in")  # Pin 3: 长按关机
    led = GPIO("/dev/gpiochip0", 203, "out")
    log_to_screen("System Ready. P4:Toggle | P3:Hold2sOFF")
except Exception as e:
    log_to_screen("GPIO Error!")
    exit(1)

process = None
shutdown_press_time = None

while True:
    try:
        if btn_toggle.read() == False:
            if process is None or process.poll() is not None:
                log_to_screen("ACTION: STARTING...")
                cmd = "/home/pi/Xinghai_live_caption_system/run.sh"
                process = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
                led.write(True)
            else:
                log_to_screen("ACTION: STOPPING...")
                os.killpg(os.getpgid(process.pid), 9)
                process = None
                led.write(False)
            time.sleep(1.0)  # 消抖

        if btn_shutdown.read() == False:
            if shutdown_press_time is None:
                # 刚按下，记录当前时间
                shutdown_press_time = time.time()
            else:
                # 已经按住，计算持续时间
                elapsed = time.time() - shutdown_press_time
                if elapsed >= 2.0:
                    log_to_screen("ACTION: SHUTDOWN NOW")
                    led.write(False)
                    time.sleep(1)
                    os.system("sudo shutdown -h now")
        else:
            # 松开按钮，重置计时器
            shutdown_press_time = None

    except Exception as e:
        # 截取错误信息前20位避免乱码
        log_to_screen("Error: {}".format(str(e)[:20]))

    time.sleep(0.1)  # 扫描频率 10Hz