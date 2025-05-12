import subprocess
import time
import re
from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetTemperature, nvmlShutdown, NVML_TEMPERATURE_GPU

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

# Initialize NVML at the start of the program
nvmlInit()

def get_gpu_temperature():
    """Get the GPU temperature using NVIDIA's NVML library."""
    try:
        handle = nvmlDeviceGetHandleByIndex(0)  # Assuming the first GPU (index 0)
        temperature = nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)
        return temperature
    except Exception as e:
        print(f"Error querying GPU temperature: {e}")
        return None

# Ensure NVML is properly shut down when the program exits
import atexit
atexit.register(nvmlShutdown)

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
