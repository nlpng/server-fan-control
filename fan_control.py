import subprocess
import time
import re

# Configuration
SERVER_IP = "SERVERS_IP_HERE"
IDRAC_USERNAME = "IDRAC_USERNAME"
IDRAC_PASSWORD = "IDRAC_PASSWORD_HERE"
CHECK_INTERVAL = 10  # seconds

# Fan speed thresholds
TEMP_THRESHOLD_HIGH = 70  # Increase fan speed above this temperature
TEMP_THRESHOLD_LOW = 45  # Decrease fan speed below this temperature
FAN_SPEED_LOW = 0x14  # 20%
FAN_SPEED_HIGH = 0x64  # 100%

def get_gpu_temperature():
    """Get the GPU temperature using nvidia-smi."""
    try:
        result = subprocess.run(["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Error querying GPU temperature: {result.stderr}")
            return None

        # Extract temperature from the output
        temp_match = re.search(r"\d+", result.stdout)
        if temp_match:
            return int(temp_match.group(0))
        else:
            print("Failed to parse GPU temperature.")
            return None
    except FileNotFoundError:
        print("nvidia-smi command not found. Make sure NVIDIA drivers are installed.")
        return None

class FanController:
    def __init__(self):
        self.current_fan_speed = None

    def set_fan_speed(self, speed):
        """Set the fan speed using ipmitool."""
        if self.current_fan_speed == speed:
            print(f"Fan speed is already set to {speed}%. No action taken.")
            return

        try:
            command = [
                "ipmitool", "-I", "lanplus", "-H", SERVER_IP, "-U", IDRAC_USERNAME, "-P", IDRAC_PASSWORD,
                "raw", "0x30", "0x30", "0x02", "0xff", f"0x{speed:02x}"
            ]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print(f"Error setting fan speed: {result.stderr}")
            else:
                self.current_fan_speed = speed
        except FileNotFoundError:
            print("ipmitool command not found. Make sure ipmitool is installed.")

    def enable_manual_fan_control(self):
        """Enable manual fan control using ipmitool."""
        try:
            command = [
                "ipmitool", "-I", "lanplus", "-H", SERVER_IP, "-U", IDRAC_USERNAME, "-P", IDRAC_PASSWORD,
                "raw", "0x30", "0x30", "0x01", "0x00"
            ]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print(f"Error enabling manual fan control: {result.stderr}")
        except FileNotFoundError:
            print("ipmitool command not found. Make sure ipmitool is installed.")

def main():
    fan_controller = FanController()

    print("Enabling manual fan control...")
    fan_controller.enable_manual_fan_control()

    while True:
        temperature = get_gpu_temperature()
        if temperature is not None:
            print(f"Current GPU temperature: {temperature}°C")

            if temperature > TEMP_THRESHOLD_HIGH:
                print("Temperature is high. Setting fan speed to 100%.")
                fan_controller.set_fan_speed(FAN_SPEED_HIGH)
            elif temperature < TEMP_THRESHOLD_LOW:
                print("Temperature is low. Setting fan speed to 20%.")
                fan_controller.set_fan_speed(FAN_SPEED_LOW)
            else:
                print("Temperature is within acceptable range. No change to fan speed.")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
