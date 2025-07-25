import subprocess
import os
import shutil

# Locate the openvpn binary dynamically
openvpn_path = shutil.which("openvpn")

if openvpn_path is None:
    print("Error: openvpn not found. Is it installed?")
    exit(1)

class SimpleVPN:
    """
    A simple VPN manager using OpenVPN.
    """

    def __init__(self, config_path, log_file="/tmp/openvpn.log"):
        self.config_path = config_path
        self.pid_file = "/tmp/openvpn.pid"
        self.log_file = log_file

    def start(self):
        """
        Start the VPN connection using the provided config file.
        Logs stdout/stderr to a file.
        """
        if not os.path.isfile(self.config_path) or not self.config_path.endswith(".ovpn"):
            print("Invalid config file. Please provide a valid .ovpn file.")
            return
        cmd = [openvpn_path, "--config", self.config_path]
        try:
            with open(self.log_file, "w") as log:
                process = subprocess.Popen(cmd, stdout=log, stderr=log, text=True)
                with open(self.pid_file, "w") as f:
                    f.write(str(process.pid))
            print(f"VPN started with PID {process.pid}. Log: {self.log_file}")
        except Exception as e:
            print(f"Error starting VPN: {e}")

    def stop(self):
        """
        Stop the running OpenVPN process using the PID file.
        """
        if os.path.isfile(self.pid_file):
            try:
                with open(self.pid_file, "r") as f:
                    pid = int(f.read())
                cmd = ["kill", str(pid)]
                subprocess.run(cmd, check=True)
                os.remove(self.pid_file)
                print(f"VPN process {pid} stopped.")
            except Exception as e:
                print(f"Error stopping VPN: {e}")
        else:
            print("No PID file found. Trying pkill as fallback.")
            cmd = ["pkill", "openvpn"]
            try:
                subprocess.run(cmd, check=True)
                print("VPN stopped (pkill fallback).")
            except subprocess.CalledProcessError as e:
                print(f"Error stopping VPN: {e}")

    def status(self, clean=False):
        """
        Check if the VPN process is running.
        If ghost PID detected and clean=True, remove the PID file.
        """
        if os.path.isfile(self.pid_file):
            try:
                with open(self.pid_file, "r") as f:
                    pid = int(f.read())
                if os.path.exists(f"/proc/{pid}"):
                    print(f"VPN is running (PID {pid}).")
                else:
                    print("VPN PID file exists, but process is not running.")
                    if clean:
                        os.remove(self.pid_file)
                        print("Stale PID file removed.")
            except Exception as e:
                print(f"Error checking VPN status: {e}")
        else:
            print("VPN is not running.")

# Allow import without running CLI logic
def main():
    import sys
    if len(sys.argv) < 3 and (len(sys.argv) < 2 or sys.argv[1] != "status"):
        print("Usage: python3 VPN.py <start|stop|status> <config_path> [--clean]")
        exit(1)

    action = sys.argv[1]
    config = sys.argv[2] if len(sys.argv) > 2 else None
    clean_flag = "--clean" in sys.argv
    vpn = SimpleVPN(config) if config else SimpleVPN("/dev/null")

    if action == "start":
        vpn.start()
    elif action == "stop":
        vpn.stop()
    elif action == "status":
        vpn.status(clean=clean_flag)
    else:
        print("Unknown action. Use 'start', 'stop', or 'status'.")

if __name__ == "__main__":
    main()
