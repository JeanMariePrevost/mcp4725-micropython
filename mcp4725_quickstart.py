"""
MCP4725 DAC Quickstart Guide
---------------------------
This example demonstrates all the main features of the MCP4725 DAC driver.
It shows basic operations, EEPROM usage, and compatibility functions.

Hardware Setup:
--------------
- Connect MCP4725 to Raspberry Pi Pico:
  * VDD -> 3.3V, VSYS for 5V, or any other supply voltage
  * GND -> GND
  * SDA -> GP0 (Pin 1) (Or any other I2C SDA pin)
  * SCL -> GP1 (Pin 2) (Or any other I2C SCL pin)
  * OUT -> Load positive
  * GND -> Load negative
"""

import time

from machine import I2C, Pin

from mcp4725 import MCP4725

# Initialize I2C and DAC
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
dac = MCP4725(i2c, vcc=3.3)  # Here using 3.3V as reference voltage

# ======================
# Setting the DAC output
# ======================

# Set DAC using raw value (0-4095)
dac.set_value(2048)  # 2048 is 50% of 4095

# Set DAC using voltage helper function
# NOTE: Depends on reference VCC value that was given
# Since we set reference VCC to 3.3V, this will result in int(1.2 / 3.3 * 4095) = 1489 raw value
# If VCC was 5V, this would result in int(1.2 / 5 * 4095) = 983 raw value
dac.set_voltage(1.2)

# Set DAC using normalized value (0.0 to 1.0)
dac.set_value_norm(0.75)  # 75% of 4095 = 3071

# ======================
# Reading the DAC value
# ======================

# Read current values
raw_value = dac.get_value()  # 3071
voltage = dac.get_voltage()  # 2.475
normalized_value = dac.get_value_norm()  # 0.75

# ======================
# EEPROM operations
# ======================

# Reading current EEPROM value
eeprom_value = dac.get_eeprom()  # E.g. 2048

# Setting EEPROM value
dac.set_eeprom_value(1024)  # Will now boot at 25% of VCC

# ======================
# Compatibility modes
# ======================
# Use these if you have issues with the standard functions

# 8-bit mode (0-255)
dac.set_value_8bit(128)  # 50% of 255

# Legacy 8-bit mode (2-byte write)
dac.set_value_8bit_legacy(191)  # 75% of 255
