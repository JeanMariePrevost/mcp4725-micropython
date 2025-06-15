# MCP4725 MicroPython Driver

Easy MicroPython interface for the MCP4725 DAC.

Developed for a hobby project, it turns this :

 ``` python
value = max(0, min(4095, int(2792)))
buf = bytearray(3)
buf[0] = 0x40 
buf[1] = value >> 4
buf[2] = (value & 0xF) << 4
self.i2c.writeto(self.address, buf)
```

into this:

``` python
dac.set_voltage(2.25)
```

<img src="images/MCP4725_Picture.webp" alt="MCP4725" width="300">

---

## Quick Start

Drop `mcp4725.py` on your board's flash memory or your project folder, then :

```python
from machine import I2C, Pin
from mcp4725 import MCP4725 # Import the driver's class

# Create an I2C bus
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

# Create an instance of MCP4725 on that bus, here with a reference VCC of 3.3V
dac = MCP4725(i2c, vcc=3.3)

# And you can now control the DAC in various manners:
dac.set_value(2048)          # Set raw 12-bit value
dac.set_voltage(1.65)        # Or set the voltage directly
dac.set_value_norm(0.5)      # Or set a ratio from 0.0 - 1.0
```

See [mcp4725_quickstart.py](mcp4725_quickstart.py) for a more in-depth example.

---

## Usage Notes / Considerations

* `set_voltage()` cannot actually determine voltage and requires the correct `vcc` reference voltage to work as expected (the voltage supplied to your MCP4725, e.g., 3.3 or 5.0).
* All input values are clamped to valid ranges (overflows will not error).
* Compatibility functions provided for clone/nonstandard modules that fail with the standard one.

---

## Known Limitations

* No explicit error handling for I2C bus errors (exceptions will propagate).
* Does not detect device presence or bus lock-up.

---

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## Author

Jean-Marie Prévost
[https://github.com/JeanMariePrevost](https://github.com/JeanMariePrevost)
