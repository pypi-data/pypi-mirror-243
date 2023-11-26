import multiprocessing
import os
import subprocess
import sys
import threading
import time
from threading import Thread

sys.path.append("D:\\Codes\\V2rayP\\v2rayp\\libs")

from in_win import config_path, inside_windows

# from .in_win import config_path, inside_windows


class Chisel_Interface:
    local_socket = ""

    def __init__(
        self,
        listen_PORT,
        Cloudflare_IP,
        Cloudflare_port,
    ):
        self.listen_PORT = listen_PORT  # pyprox listening to 127.0.0.1:listen_PORT
        self.Cloudflare_IP = Cloudflare_IP
        self.Cloudflare_port = Cloudflare_port

        self.mainThread = threading.Thread(target=self.start_tunnel)
        self.mainThread.daemon = True
        self.mainThread.start()

    def start_tunnel(self):
        print("Hello")
        if inside_windows():
            cmd = f"{config_path()}\\bin\\chisel.exe client http://boz.imconnect.site:8080 127.0.0.1:{self.listen_PORT}:127.0.0.1:{self.Cloudflare_port}"
        else:
            cmd = f"chmod +x {config_path()}/bin/xray && {config_path()}/bin/chisel client http://boz.imconnect.site:8080 127.0.0.1:5050:127.0.0.1:2096"
        self.thread_run_read_v2ray(cmd)

    def thread_run_read_v2ray(self, cmd):
        self.enable_loops = True
        print("thread_run_read_v2ray is ran")

        err_cnt = 0

        print("cmd before: " + cmd)

        # tasklist = ""
        # while "xray" not in tasklist:
        self.chisel_process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        # tasklist = os.popen("tasklist").read()

        print("next line")
        while self.enable_loops:
            line = self.chisel_process.stderr.readline().strip().decode("utf-8")
            if len(line) < 3:
                time.sleep(0.1)
                continue
            print(line)

    def stop(self):
        print("**Stop Chisel is called***")
        self.loop = False
        self.enable_loops = False
        # self.local_socket.setblocking(False)
        try:
            if inside_windows:
                os.popen("taskkill /f /im *chisel*")
        except:
            print("error closing..")
        # GFW_thread_id = self.mainThread.ident
        # ctypes.pythonapi.PyThreadState_SetAsyncExc(
        #     GFW_thread_id, ctypes.py_object(SystemExit)
        # )
        # self.mainThread.join(1)

        try:
            self.mainThread.kill()
            self.mainThread.terminate()

        except:
            pass
        # self.mainThread.join()
        print(f"Subprocess {self.mainThread.name} alive: {self.mainThread.is_alive}")
        # self.mainThread.join(2)


# Start the tunne
if __name__ == "__main__":
    multiprocessing.freeze_support()
    try:
        listen_PORT = int(sys.argv[2])  # pyprox listening to 127.0.0.1:listen_PORT
        Cloudflare_IP = sys.argv[1]
        Cloudflare_port = int(sys.argv[3])
        Chisel_Interface(listen_PORT, Cloudflare_IP, Cloudflare_port)
    except:
        listen_PORT = 5050
        Cloudflare_IP = ""
        Cloudflare_port = 2096
        Chisel_Interface(listen_PORT, Cloudflare_IP, Cloudflare_port)
    while True:
        time.sleep(10)
        ##########################################################
        #########################################################
