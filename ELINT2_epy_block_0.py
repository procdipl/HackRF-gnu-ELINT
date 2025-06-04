"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""


import pmt
from gnuradio import gr

class blk(gr.basic_block):
    def __init__(self, start=1e6, stop=5.5e6, step=100e3):
        gr.basic_block.__init__(self, name="Freq Sweeper", in_sig=None, out_sig=None)
        self.start = start
        self.stop = stop
        self.step = step
        self.freq = self.start
        self.running = True
        self.message_port_register_in(pmt.intern("cmd"))
        self.set_msg_handler(pmt.intern("cmd"), self.handle_cmd)
    
    def handle_cmd(self, msg):
        # DEBUG: print the type and contents of the message
        print("Freq Sweeper got msg:", msg, "type:", type(msg))
        # Accept both strings and PMT symbols and floats for debugging
        if pmt.is_symbol(msg):
            m = pmt.symbol_to_string(msg)
        elif pmt.is_string(msg):
            m = pmt.symbol_to_string(msg)
        elif isinstance(msg, str):
            m = msg
        elif pmt.is_number(msg):
            # Ignore floats, but print for debug
            print("Ignored float message:", msg)
            return
        else:
            m = str(msg)

        if m == "TICK" and self.running:
            self.freq += self.step
            if self.freq > self.stop:
                self.freq = self.start
            try:
                self.set_variable("freq", self.freq)
                print("Set freq to", self.freq)
            except Exception as e:
                print("Freq update error:", e)
        elif m == "START":
            self.running = True
            print("Freq Sweeper: started")
        elif m == "STOP":
            self.running = False
            print("Freq Sweeper: stopped")
        else:
            print("Freq Sweeper: Unknown message", m)