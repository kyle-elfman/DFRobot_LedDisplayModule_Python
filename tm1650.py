from smbus2 import SMBus
import time

class TM1650:
    """
    TM1650 4-digit 7-segment LED display driver
    Compatible with DFRobot DFR0645 display modules.
    """

    CTRL_ADDR = 0x24
    DIGIT_ADDRS = [0x34, 0x35, 0x36, 0x37]

    # 7-segment encoding
    SEG_MAP = {
        ' ': 0x00,
        '-': 0x40,
        '_': 0x08,
        '0': 0x3F,
        '1': 0x06,
        '2': 0x5B,
        '3': 0x4F,
        '4': 0x66,
        '5': 0x6D,
        '6': 0x7D,
        '7': 0x07,
        '8': 0x7F,
        '9': 0x6F,
        'A': 0x77, 'a': 0x77,
        'b': 0x7C, 'B': 0x7C,
        'C': 0x39, 'c': 0x58,
        'D': 0x5E, 'd': 0x5E,
        'E': 0x79, 'e': 0x79,
        'F': 0x71, 'f': 0x71,
        'H': 0x76, 'h': 0x74,
        'L': 0x38, 'l': 0x30,
        'P': 0x73, 'p': 0x73,
        'U': 0x3E, 'u': 0x1C,
        'r': 0x50,
    }

    def __init__(self, bus_num=1):
        self.bus = SMBus(bus_num)
        self.enable(True)

    def enable(self, on=True, brightness=7):
        """Turn display on/off and set brightness (0–7)."""
        if not on:
            self.bus.write_byte(self.CTRL_ADDR, 0x00)
        else:
            brightness = max(0, min(brightness, 7))
            cmd = 0x01 | (brightness << 4)
            # Some TM1650 clones use brightness in low bits
            cmd = brightness | 0x01
            self.bus.write_byte(self.CTRL_ADDR, cmd)

    def clear(self):
        for addr in self.DIGIT_ADDRS:
            self.bus.write_byte(addr, 0x00)

    def set_digit(self, index, char, dot=False):
        """Write a single character (0–3)."""
        if index < 0 or index > 3:
            return

        seg = self.SEG_MAP.get(char, 0x00)
        if dot:
            seg |= 0x80

        self.bus.write_byte(self.DIGIT_ADDRS[index], seg)

    def print(self, text):
        """Print up to 4 characters to the display."""
        self.clear()
        for i in range(min(4, len(text))):
            ch = text[i]
            dot = False

            # check for decimal point after char
            if i + 1 < len(text) and text[i+1] == '.':
                dot = True

            self.set_digit(i, ch, dot)

            if dot:
                # skip decimal point in text
                text = text[:i+1] + text[i+2:]

    def show_number(self, num):
        """Display an integer from -999 to 9999."""
        s = str(num)
        if len(s) > 4:
            s = s[-4:]  # last 4 digits
        self.print(s)

    def close(self):
        self.bus.close()

