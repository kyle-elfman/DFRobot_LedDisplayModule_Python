from tm1650 import TM1650
import time

class TM1650Display:
    """
    High-level wrapper for TM1650 4-digit LED display with animations.
    """

    def __init__(self, bus_num=1):
        self.display = TM1650(bus_num)
    
    def clear(self):
        self.display.clear()
    
    def show_number(self, num):
        """Display integer number (-999 to 9999)."""
        self.display.show_number(num)
    
    def show_text(self, text):
        """Display up to 4 characters."""
        self.display.print(text)
    
    def scroll_text(self, text, delay=0.5):
        """
        Scroll text across the 4-digit display.
        Example: 'HELLO' -> 'HELL', 'ELLO', 'LLO ', 'LO  ', 'O   '
        """
        text = str(text)
        padded = text + " " * 4
        for i in range(len(padded) - 3):
            self.display.print(padded[i:i+4])
            time.sleep(delay)
    
    def blink(self, text, times=5, interval=0.5):
        """
        Blink a text on/off.
        """
        for _ in range(times):
            self.display.print(text[:4])
            time.sleep(interval)
            self.display.clear()
            time.sleep(interval)
    
    def countdown(self, start=9, interval=1):
        """Simple countdown animation."""
        for i in range(start, -1, -1):
            self.display.show_number(i)
            time.sleep(interval)
    
    def countup(self, end=9, interval=1):
        """Simple countup animation."""
        for i in range(end + 1):
            self.display.show_number(i)
            time.sleep(interval)
    
    def close(self):
        self.display.close()










disp = TM1650Display()

# Simple text
disp.show_text("HELLO")  # displays "HELL"

# Scroll text
disp.scroll_text("HELLO WORLD", delay=0.3)

# Blink message
disp.blink("1234", times=4, interval=0.4)

# Countdown
disp.countdown(9, interval=0.7)

# Countup
disp.countup(5, interval=0.5)

disp.clear()
disp.close()
