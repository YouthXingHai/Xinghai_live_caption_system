from periphery import GPIO
import time
import subprocess
import os

os.system("sudo chmod 666 /dev/tty1")


def log_to_screen(msg):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = "\n[{}] [MONITOR] {}\n".format(timestamp, msg)
    try:
        with open("/dev/tty1", "w") as f:
            f.write(formatted_msg)
    except:
        pass
    print(msg)


try:
    # Pin 4 = Start, Pin 3 = Stop (on gpiochip1)
    btn_start = GPIO("/dev/gpiochip1", 4, "in")
    btn_stop = GPIO("/dev/gpiochip1", 3, "in")
    # LED indicator (on gpiochip0)
    led = GPIO("/dev/gpiochip0", 203, "out")
except Exception as e:
    log_to_screen("GPIO Init Error: {}".format(e))
    exit(1)

process = None

while True:
    try:
        if btn_start.read() == False:
            if not process or process.poll() is not None:
                log_to_screen("START button triggered.")
                cmd = "/home/pi/Xinghai_live_caption_system/run_app.sh"
                # Start the system in a new process group
                process = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
                led.write(True)
            else:
                log_to_screen("System already running.")
            time.sleep(0.5)  # Debounce

        if btn_stop.read() == False:
            log_to_screen("STOP button triggered.")
            if process:
                os.killpg(os.getpgid(process.pid), 9)
                process = None
            led.write(False)
            time.sleep(0.5)  # Debounce

    except Exception as e:
        log_to_screen("Loop Error: {}".format(e))

    time.sleep(0.05)