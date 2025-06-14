"""
MCP4725 DAC Driver for Raspberry Pi Pico

License: MIT
Copyright (c) 2025 Jean-Marie Prévost
GitHub: https://github.com/JeanMariePrevost/mcp4725

Basic Usage:
------------
# Initialize I2C and DAC
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
dac = MCP4725(i2c, vcc=3.3)

# Example of ways to set the DAC to 50% of our 3.3V VCC
dac.set_value(2048) # By raw DAC value (0-4095)
dac.set_voltage(1.65)  # By voltage
dac.set_value_norm(0.5) # 50% or 3.3V
"""


class MCP4725:
    def __init__(self, i2c, address: int = 0x60, vcc: float = 3.3) -> None:
        """
        Initialize MCP4725 DAC.
        :param i2c: Initialized machine.I2C instance
        :param address: I2C address (default 0x60)
        :param vcc: Supply voltage (default 3.3V) (Only used as a reference for set_voltage and get_voltage)
        """
        self.i2c = i2c
        self.address = address
        self.vcc = vcc

    # ======================
    # BASIC OPERATIONS
    # ======================

    def set_value(self, value: int) -> None:
        """
        Set raw DAC output value (12 bit integer, 0-4095)
        Fast mode, does not write EEPROM.
        :param value: 12-bit integer (0-4095)
        """
        value = max(0, min(4095, int(value)))
        buf = bytearray(3)
        buf[0] = 0x40  # Fast mode command
        buf[1] = value >> 4
        buf[2] = (value & 0xF) << 4
        self.i2c.writeto(self.address, buf)

    def get_value(self) -> int:
        """Get current raw DAC value (12 bit integer, 0-4095)"""
        buf = self.i2c.readfrom(self.address, 5)
        return ((buf[1] << 4) | (buf[2] >> 4)) & 0xFFF

    def set_voltage(self, voltage: float) -> None:
        """
        Set DAC output voltage.
        NOTE: Cannot truly measure voltage, only used as a shorthand based on the reference voltage.
        :param voltage: Desired output voltage (0 to VCC)
        """
        value = self._voltage_to_value(voltage)
        self.set_value(value)

    def get_voltage(self) -> float:
        """
        Get current DAC output voltage.
        NOTE: Cannot truly measure voltage, only used as a shorthand based on the reference voltage.
        :return: Current voltage as float
        """
        value = self.get_value()
        return self._value_to_voltage(value)

    def set_value_norm(self, value: float) -> None:
        """
        Set DAC output using normalized value (0.0 to 1.0).
        Fast mode, does not write EEPROM.
        :param value: Float between 0.0 and 1.0 (0% to 100%)
        """
        value = max(0.0, min(1.0, float(value)))
        dac_value = int(value * 4095)
        self.set_value(dac_value)

    def get_value_norm(self) -> float:
        """Get current DAC value as normalized value (0.0 to 1.0)"""
        value = self.get_value()
        return value / 4095

    # ======================
    # EEPROM OPERATIONS
    # ======================

    def get_eeprom(self) -> int:
        """Get stored EEPROM value (the value that will be restored when the device is powered on)"""
        buf = self.i2c.readfrom(self.address, 5)
        return ((buf[3] << 4) | (buf[4] >> 4)) & 0xFFF

    def set_eeprom_value(self, value: int) -> None:
        """
        Set DAC output and store value in EEPROM (power-on default).
        :param value: 12-bit integer (0-4095)
        """
        value = max(0, min(4095, int(value)))
        buf = bytearray(3)
        buf[0] = 0x60  # Write DAC and EEPROM
        buf[1] = value >> 4
        buf[2] = (value & 0xF) << 4
        self.i2c.writeto(self.address, buf)

    # ======================
    # INTERNAL FUNCTIONS
    # ======================

    def _value_to_voltage(self, value: int) -> float:
        """Internal: Convert raw DAC value to voltage"""
        return (value / 4095) * self.vcc

    def _voltage_to_value(self, voltage: float) -> int:
        """Internal: Convert voltage to raw DAC value"""
        return int((voltage / self.vcc) * 4095)

    # ======================
    # COMPATIBILITY MODES
    # For non-standard implementations only
    #
    # Note: These are not part of the official MCP4725 specification.
    # They are provided for compatibility with certain non-compliant modules.
    # Some of the Chinese clones I purchased did not support the 3-byte writes and only worked on values from 0-255.
    # ======================

    def set_value_8bit(self, value):
        """
        Non-standard: Set raw DAC output value using only upper 8 bits (0-255).
        Only for compatibility with certain non-compliant modules.
        :param value: 8-bit integer (0-255)
        """
        value = max(0, min(255, int(value)))
        buf = bytearray(3)
        buf[0] = 0x40  # Fast mode command
        buf[1] = value
        buf[2] = 0x00  # Lower 4 bits zeroed
        self.i2c.writeto(self.address, buf)

    def set_value_8bit_legacy(self, value):
        """
        Non-standard: Set raw DAC output value using 2-byte write (no command byte).
        Only for diagnosis or compatibility with certain clones.
        :param value: 8-bit integer (0-255)
        """
        value = max(0, min(255, int(value)))
        buf = bytearray(2)
        buf[0] = value
        buf[1] = 0x00
        self.i2c.writeto(self.address, buf)
