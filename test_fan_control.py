import unittest
from unittest.mock import patch, MagicMock
from fan_control import get_gpu_temperatures, FanController


class TestFanControl(unittest.TestCase):
    @patch("fan_control.nvmlDeviceGetCount", return_value=2)
    @patch("fan_control.nvmlDeviceGetTemperature", side_effect=[50, 60])
    @patch("fan_control.nvmlDeviceGetHandleByIndex")
    def test_get_gpu_temperatures(self, mock_handle, mock_temp, mock_count):
        temperatures = get_gpu_temperatures()
        self.assertEqual(temperatures, [50, 60])

    @patch("subprocess.run")
    def test_set_fan_speed(self, mock_subprocess):
        mock_subprocess.return_value = MagicMock(returncode=0)
        fan_controller = FanController()
        fan_controller.set_fan_speed(0x32)  # Set to 50%
        self.assertEqual(fan_controller.current_fan_speed, 0x32)
        mock_subprocess.assert_called_once()

    @patch("subprocess.run")
    def test_enable_manual_fan_control(self, mock_subprocess):
        mock_subprocess.return_value = MagicMock(returncode=0)
        fan_controller = FanController()
        fan_controller.enable_manual_fan_control()
        mock_subprocess.assert_called_once()


if __name__ == "__main__":
    unittest.main()
