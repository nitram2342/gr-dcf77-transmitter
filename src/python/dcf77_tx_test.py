#!/usr/bin/env python

"""
Simple DCF77 Transmitter test
"""

from gnuradio import gr, eng_notation
from gnuradio import usrp
from gnuradio import audio
from gnuradio import blks
from gnuradio.eng_option import eng_option
from optparse import OptionParser
from usrpm import usrp_dbid
import sys
from gnuradio import dcf77

from gnuradio.wxgui import stdgui, fftsink, scopesink
from gnuradio import tx_debug_gui
import wx

class pipeline(gr.hier_block):
    def __init__(self, fg,  lo_freq, usrp_rate):


        cl = dcf77.clock(07, # hour
                         35-2, # min
                         6,  # day in month
                         7,  # day of week
                         2,  # month
                         8,  # year
                         0)  # loop
        tx = dcf77.mod(usrp_rate)
	f2c = gr.float_to_complex()

        mixer = gr.multiply_ff()

        fg.connect (cl, tx, f2c)
        
        gr.hier_block.__init__(self, fg, cl, f2c)


class tx_graph (stdgui.gui_flow_graph):
    def __init__(self, frame, panel, vbox, argv):

        stdgui.gui_flow_graph.__init__ (self, frame, panel, vbox, argv)

        parser = OptionParser (option_class=eng_option)
        parser.add_option("-T", "--tx-subdev-spec", type="subdev", default=None,
                          help="select USRP Tx side A or B")
        parser.add_option("-f", "--freq", type="eng_float", default=None,
                           help="set Tx frequency to FREQ [required]", metavar="FREQ")
        parser.add_option("","--debug", action="store_true", default=False,
                          help="Launch Tx debugger")
        (options, args) = parser.parse_args ()

        if len(args) != 0:
            parser.print_help()
            sys.exit(1)

        if options.freq is None:
            sys.stderr.write("usrp_tx_video.py: must specify frequency with -f FREQ\n")
            parser.print_help()
            sys.exit(1)

        # ----------------------------------------------------------------

        self.u = usrp.sink_c ()       # the USRP sink (consumes samples)

        self.dac_rate = self.u.dac_rate()                    # 128 MS/s
        self.usrp_interp = 128
        self.usrp_rate = self.dac_rate / self.usrp_interp


        self.u.set_interp_rate(self.usrp_interp)

        # determine the daughterboard subdevice we're using
        if options.tx_subdev_spec is None:
            options.tx_subdev_spec = usrp.pick_tx_subdevice(self.u)

        m = usrp.determine_tx_mux_value(self.u, options.tx_subdev_spec)
        self.u.set_mux(m)
        self.subdev = usrp.selected_subdev(self.u, options.tx_subdev_spec)
        print "Using TX d'board %s with rate %ld" % (self.subdev.side_and_name(), self.usrp_rate)

        self.subdev.set_gain(self.subdev.gain_range()[1])    # set max Tx gain
	self.u.tune(self.subdev._which, self.subdev, options.freq)
        self.subdev.set_enable(True)                         # enable transmitter

        t = pipeline(self, options.freq, self.usrp_rate)

        gain = gr.multiply_const_cc (32000.0)

        # connect it all
        self.connect (t, gain)
        self.connect (gain, self.u)

        # plot an FFT to verify we are sending what we want
        if 1:
            post_mod_fft = fftsink.fft_sink_c(self, panel, title="Signal in frequency domain",
                                              fft_size=64, sample_rate=self.usrp_rate,
                                              y_per_div=20, ref_level=40)

            #post_mod_oscope = scopesink.scope_sink_c(self, panel, sample_rate=self.usrp_rate,
            #                                         title="Signal in time domain", v_scale = 1,
            #                                         t_scale=0.0001)

            self.connect (t, post_mod_fft)
            #self.connect (t, post_mod_oscope)
            vbox.Add (post_mod_fft.win, 1, wx.EXPAND)
            #vbox.Add (post_mod_oscope.win, 1, wx.EXPAND)
            

        if options.debug:
            self.debugger = tx_debug_gui.tx_debug_gui(self.subdev)
            self.debugger.Show(True)


def main ():
    app = stdgui.stdapp (tx_graph, "DCF77 transmitter")
    app.MainLoop ()

if __name__ == '__main__':
    main ()
