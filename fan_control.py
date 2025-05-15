import subprocess
import time
import signal
import sys
from pynvml import (
    nvmlInit,
    nvmlDeviceGetHandleByIndex,
    nvmlDeviceGetTemperature,
    nvmlShutdown,
    NVML_TEMPERATURE_GPU,
    nvmlDeviceGetCount,
)
import atexit

# Configuration
SERVER_IP = "SERVERS_IP_HERE"
IDRAC_USERNAME = "IDRAC_USERNAME"
IDRAC_PASSWORD = "IDRAC_PASSWORD_HERE"
CHECK_INTERVAL = 10  # seconds

# Fan speed thresholds
TEMP_THRESHOLD_HIGH = 70  # Increase fan speed above this temperature
TEMP_THRESHOLD_LOW = 45  # Decrease fan speed below this temperature
FAN_SPEED_LOW = 0x15  # 21%
FAN_SPEED_HIGH = 0x32  # 50%

# Initialize NVML at the start of the program
nvmlInit()

# Ensure NVML is properly shut down when the program exits
atexit.register(nvmlShutdown)


def signal_handler(sig, frame):
    print("Shutting down gracefully...")
    nvmlShutdown()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def get_gpu_temperatures():
    """Get the GPU temperatures for all available GPUs using NVIDIA's NVML library."""
    try:
        gpu_temperatures = []
        device_count = nvmlDeviceGetCount()  # Get the total number of GPUs
        for i in range(device_count):
            handle = nvmlDeviceGetHandleByIndex(i)
            temperature = nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)
            gpu_temperatures.append(temperature)
        return gpu_temperatures
    except Exception as e:
        print(f"Error querying GPU temperatures: {e}")
        return []


class FanController:
    def __init__(self):
        self.current_fan_speed = None
        self.hysteresis_offset = 5  # Hysteresis offset in degrees Celsius

    def set_fan_speed(self, speed):
        """Set the fan speed using ipmitool."""
        if self.current_fan_speed == speed:
            return

        try:
            command = [
                "ipmitool",
                "-I",
                "lanplus",
                "-H",
                SERVER_IP,
                "-U",
                IDRAC_USERNAME,
                "-P",
                IDRAC_PASSWORD,
                "raw",
                "0x30",
                "0x30",
                "0x02",
                "0xff",
                f"0x{speed:02x}",
            ]
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
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
                "ipmitool",
                "-I",
                "lanplus",
                "-H",
                SERVER_IP,
                "-U",
                IDRAC_USERNAME,
                "-P",
                IDRAC_PASSWORD,
                "raw",
                "0x30",
                "0x30",
                "0x01",
                "0x00",
            ]
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if result.returncode != 0:
                print(f"Error enabling manual fan control: {result.stderr}")
        except FileNotFoundError:
            print("ipmitool command not found. Make sure ipmitool is installed.")


def main():
    fan_controller = FanController()

    fan_controller.enable_manual_fan_control()

    while True:
        try:
            temperatures = get_gpu_temperatures()
            if temperatures:
                # Use the maximum temperature across all GPUs for fan control
                max_temp = max(temperatures)
                if max_temp > TEMP_THRESHOLD_HIGH + fan_controller.hysteresis_offset:
                    fan_controller.set_fan_speed(FAN_SPEED_HIGH)
                elif max_temp < TEMP_THRESHOLD_LOW - fan_controller.hysteresis_offset:
                    fan_controller.set_fan_speed(FAN_SPEED_LOW)
        except Exception as e:
            print(f"Error in main loop: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
