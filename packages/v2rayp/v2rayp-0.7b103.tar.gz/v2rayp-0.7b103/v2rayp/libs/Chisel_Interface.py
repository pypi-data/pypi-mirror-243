import multiprocessing
import os
import subprocess
import sys
import threading
import time
from threading import Thread

try:
    sys.path.append("D:\\Codes\\V2rayP\\v2rayp")
except:
    pass
from libs.in_win import config_path, inside_windows


class Chisel_Interface:
    local_socket = ""

    def __init__(self, listen_PORT, Chisel_Address, Chisel_port, v2ray_port):
        self.listen_PORT = listen_PORT  # pyprox listening to 127.0.0.1:listen_PORT
        self.Chisel_Address = Chisel_Address
        self.Chisel_port = Chisel_port
        self.v2ray_port = v2ray_port

        self.isconnected = False
        self.mainThread = threading.Thread(target=self.start_tunnel, daemon=True)
        self.mainThread.start()

        self.chisel_connection_check()

    def chisel_connection_check(self):
        cnt = 0
        while not self.isconnected:
            print("Waiting for chisel...")
            if cnt >= 5:
                print("Chisel error not connecting!")
                self.stop()
                return False
            else:
                cnt += 1
            time.sleep(1)
        print("Chisel connected...")
        return True

    def start_tunnel(self):
        if inside_windows():
            cmd = f"{config_path()}\\bin\\chisel.exe client http://{self.Chisel_Address}:{self.Chisel_port} 127.0.0.1:{self.listen_PORT}:127.0.0.1:{self.v2ray_port}"
        else:
            cmd = f"chmod +x {config_path()}/bin/chisel && {config_path()}/bin/chisel client http://{self.Chisel_Address}:{self.Chisel_port} 127.0.0.1:{self.listen_PORT}:127.0.0.1:{self.v2ray_port}"
        print(f"chisel command: {cmd}")
        self.run_read_v2ray(cmd)

    def run_read_v2ray(self, cmd):
        self.enable_loops = True
        print("thread_run_read_v2ray is ran")

        print("cmd before: " + cmd)

        self.chisel_process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        print("next line")
        while self.enable_loops:
            line = self.chisel_process.stderr.readline().strip().decode("utf-8")
            if "Connected" in line:
                self.isconnected = True
                print(line)
                return

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
                os.popen("taskkill /f /im chisel*").read()
        except:
            print("error closing..")

        # try:
        #     self.mainThread.kill()
        #     self.mainThread.terminate()

        # except:
        #     pass

        print(f"Subprocess {self.mainThread.name} alive: {self.mainThread.is_alive}")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    try:
        listen_PORT = int(sys.argv[2])  # pyprox listening to 127.0.0.1:listen_PORT
        Chisel_Address = sys.argv[1]
        Chisel_port = int(sys.argv[3])
        v2ray_port = int(sys.argv[4])
        Chisel_Interface(listen_PORT, Chisel_Address, Chisel_port, v2ray_port)
    except:
        listen_PORT = 2500
        Chisel_Address = "boz.imconnect.site"
        Chisel_port = 8880
        v2ray_port = 2096
        Chisel_Interface(listen_PORT, Chisel_Address, Chisel_port, v2ray_port)
    while True:
        time.sleep(10)
        ##########################################################
        #########################################################
