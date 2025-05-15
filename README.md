# 🚀 GPU Temperature Monitoring and Fan Control

This project provides a Python-based solution for monitoring GPU temperature and controlling server fan speed using `ipmitool` commands. It leverages NVIDIA's NVML library for efficient GPU temperature monitoring.

## ✨ Features
- 🌡️ Monitors GPU temperature in real-time.
- 🌀 Adjusts server fan speed based on GPU temperature thresholds.
- 🛠️ Uses `ipmitool` to control fan speed via IPMI commands.
- ⚡ Lightweight and efficient, with minimal resource usage.

## 📋 Prerequisites
1. 🐍 **Python 3.9 or later**
2. 🖥️ **NVIDIA Drivers** installed on the server.
3. 🛠️ **ipmitool** installed on the server.
4. 📦 **pynvml** Python library for GPU monitoring.

## 📦 Installation

### 🛠️ Clone the Repository
```bash
git clone <repository-url>
cd server-fan-control
```

### 📦 Install Dependencies
Ensure `pynvml` is installed:
```bash
pip install nvidia-ml-py3
```

### 🐳 Docker Setup
Alternatively, you can use Docker to run the application:

1. 🏗️ Build the Docker image:
   ```bash
   docker-compose build
   ```

2. ▶️ Start the container:
   ```bash
   docker-compose up
   ```

## ⚙️ Configuration
Update the following placeholders in the `fan_control.py` file:
- `SERVER_IP`: The IP address of the server.
- `IDRAC_USERNAME`: The username for IPMI access.
- `IDRAC_PASSWORD`: The password for IPMI access.

## 🔍 Parameters Explained

### ⚙️ Configuration Parameters
- `SERVER_IP`: The IP address of the server where IPMI commands will be executed.
- `IDRAC_USERNAME`: The username for accessing the iDRAC interface of the server.
- `IDRAC_PASSWORD`: The password for accessing the iDRAC interface of the server.
- `CHECK_INTERVAL`: The time interval (in seconds) between each GPU temperature check and fan speed adjustment.

### 🌡️ Fan Speed Thresholds
- `TEMP_THRESHOLD_HIGH`: The GPU temperature (in °C) above which the fan speed is set to 100%.
- `TEMP_THRESHOLD_LOW`: The GPU temperature (in °C) below which the fan speed is set to 21%.
- `FAN_SPEED_LOW`: The fan speed percentage (in hexadecimal) when the GPU temperature is below `TEMP_THRESHOLD_LOW` (default: 21%).
- `FAN_SPEED_HIGH`: The fan speed percentage (in hexadecimal) when the GPU temperature exceeds `TEMP_THRESHOLD_HIGH` (default: 50%).

### 🖥️ GPU Monitoring
- The script uses NVIDIA's NVML library to monitor GPU temperatures.
- `nvmlDeviceGetCount()`: Retrieves the total number of GPUs available on the server.
- `nvmlDeviceGetHandleByIndex(index)`: Gets the handle for a GPU at the specified index.
- `nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)`: Retrieves the temperature of the GPU associated with the given handle.

## 🛠️ How It Works
1. The script initializes NVIDIA's NVML library to monitor GPU temperature.
2. It enables manual fan control using `ipmitool`.
3. Based on the GPU temperature:
   - 🌡️ If the temperature exceeds `TEMP_THRESHOLD_HIGH` (default: 70°C), the fan speed is set to 100%.
   - ❄️ If the temperature drops below `TEMP_THRESHOLD_LOW` (default: 45°C), the fan speed is set to 20%.
   - ⚖️ Otherwise, the fan speed remains unchanged.

## ⚠️ Constraints
This Docker container only works on Dell PowerEdge servers that support IPMI commands, specifically:
- 🖥️ Dell PowerEdge R720
- 🔧 iDRAC firmware version < 9 (e.g., firmware 3.30.30.30 or earlier)

## 📂 File Structure
- `fan_control.py`: The main Python script for monitoring and controlling fan speed.
- `Dockerfile`: Docker configuration for running the script in a container.
- `docker-compose.yml`: Docker Compose configuration for easy deployment.

## ▶️ Usage
### 🖥️ Running Locally
1. Update the configuration in `fan_control.py`.
2. Run the script:
   ```bash
   python3 fan_control.py
   ```

### 🐳 Running with Docker
1. Build and start the container:
   ```bash
   docker-compose up --build
   ```

2. The script will automatically monitor GPU temperature and adjust fan speed as needed.

## 📝 Notes
- Ensure the server has IPMI enabled and accessible.
- The script assumes the first GPU (index 0) is being monitored. Update the code if multiple GPUs need to be monitored.

## 📜 License
This project is licensed under the MIT License.

## 🛠️ Detailed Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd server-fan-control
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the `fan_control.py` file with your server details:
   - `SERVER_IP`: The IP address of the server.
   - `IDRAC_USERNAME`: The username for IPMI access.
   - `IDRAC_PASSWORD`: The password for IPMI access.

4. Run the script:
   ```bash
   python3 fan_control.py
   ```

## 🛠️ Example Configurations

### Example `fan_control.py` Configuration
```python
SERVER_IP = "192.168.1.100"
IDRAC_USERNAME = "admin"
IDRAC_PASSWORD = "password"
CHECK_INTERVAL = 10
TEMP_THRESHOLD_HIGH = 70
TEMP_THRESHOLD_LOW = 45
FAN_SPEED_LOW = 0x15
FAN_SPEED_HIGH = 0x32
```

## 🛠️ Troubleshooting Tips

1. **IPMI Command Not Found**:
   - Ensure `ipmitool` is installed on your system.
   - Install it using:
     ```bash
     sudo apt install ipmitool
     ```

2. **NVIDIA Driver Issues**:
   - Ensure the NVIDIA drivers are installed and the `nvidia-smi` command works.

3. **Permission Denied**:
   - Run the script with appropriate permissions or as a user with access to IPMI commands.

4. **Fan Speed Not Changing**:
   - Verify the server supports manual fan control via IPMI.
   - Check the server's iDRAC firmware version.

## 🛠️ Contribution Guidelines

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push your changes to your fork:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request to the `main` branch of this repository.

Thank you for contributing!
