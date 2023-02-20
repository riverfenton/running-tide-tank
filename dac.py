import board
import busio

import adafruit_mcp4725

class dac_ops:
    
    def find_voltage(freq):
        max_rpm=4000/46
        out_v=freq/max_rpm*4096
        out_v=out_v*10/6.66
        return out_v

    def dac_write(freq):
        # Initialize I2C bus.
        i2c = busio.I2C(board.SCL, board.SDA)

        # Initialize MCP4725.
        dac = adafruit_mcp4725.MCP4725(i2c, address=0x60)
        # Optionally you can specify a different addres if you override the A0 pin.
        # amp = adafruit_max9744.MAX9744(i2c, address=0x63)

        # There are a three ways to set the DAC output, you can use any of these:
        dac.value = 65535  # Use the value property with a 16-bit number just like
        # the AnalogOut class.  Note the MCP4725 is only a 12-bit
        # DAC so quantization errors will occur.  The range of
        # values is 0 (minimum/ground) to 65535 (maximum/Vout).


        dac.normalized_value = 1.0  # Use the normalized_value property to set the
        # output with a floating point value in the range
        # 0 to 1.0 where 0 is minimum/ground and 1.0 is
        # maximum/Vout.

        # Main loop will go up and down through the range of DAC values forever.
        out_v=dac_ops.find_voltage(freq)
        dac.raw_value =  out_v
        print(out_v)

        
