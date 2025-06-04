"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = example_param

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        output_items[0][:] = input_items[0] * self.example_param
        return len(output_items[0])
import pmt

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self,
            name="Freq Sweeper",
            in_sig=None,
            out_sig=None)

        self.start = 100e6
        self.stop = 110e6
        self.step = 1e6
        self.freq = self.start

        self.declare_sample_delay(0)

        self.message_port_register_in(pmt.intern("in"))
        self.set_msg_handler(pmt.intern("in"), self.handle_msg)

    def handle_msg(self, msg):
        self.freq += self.step
        if self.freq > self.stop:
            self.freq = self.start

        # Schimbă valoarea variabilei globale `freq`
        try:
            self.set_variable("freq", self.freq)
        except Exception as e:
           print(f"[sweep] current freq: {self.freq / 1e6:.2f} MHz")

