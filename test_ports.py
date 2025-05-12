import pytest
import serial
from unittest.mock import patch, MagicMock
from yolorinma import available_port

def test_available_port_success():
    with patch('serial.Serial', return_value=MagicMock()) as mock_serial:
        assert available_port('COM3') is True
        mock_serial.assert_called_once_with('COM3')

def test_available_port_failure():
    with patch('serial.Serial', side_effect=serial.SerialException):
        assert available_port('COM999') is False
