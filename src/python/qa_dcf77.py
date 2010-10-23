#!/usr/bin/env python
#
# Copyright 2004 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, gr_unittest
import dcf77

class qa_dcf77 (gr_unittest.TestCase):

    def setUp (self):
        self.fg = gr.flow_graph ()

    def tearDown (self):
        self.fg = None

    def test_001_clock (self):
        cl = dcf77.clock(14, 44, 1, 7, 1, 6, 3)

        dst = gr.vector_sink_i()
        self.fg.connect (cl, dst)

        self.fg.run ()
        result_data = dst.data ()

        expected_result = (
            0,                            # 0: always 0
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,  # 1-14: reserved/ unused
            0,                            # 15: 0 =default antenna
            0,                            # 16: 0 = no mez/mesz-change
            0,1,                          # 17-18: 01= mez
            0,                            # 19: no leap second with next 59 sec
            1,                            # 20: start bit for time block, always 1
            0,0,1,0,0,0,1,                # 21-27: min = 1, 2, 4, 8, 10, 20, 40 -- 44
            0,                            # 28: check bit for minutes: 0 = even, 1 = odd
            0,0,1,0,1,0,                  # 29-34: hours
            0,                            # 35: check bit
            1,0,0,0,0,0,                  # 36-41: day within month
            1,1,1,                        # 42-44: day of week (1-7)
            1,0,0,0,0,                    # 45-49: month
            0,1,1,0,0,0,0,0,              # 50-57: year
            1,                            # 58: check bit, here 1
            2,
            0,                            # 0: always 0
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,  # 1-14: reserved/ unused
            0,                            # 15: 0 =default antenna
            0,                            # 16: 0 = no mez/mesz-change
            0,1,                          # 17-18: 01= mez
            0,                            # 19: no leap second with next 59 sec
            1,                            # 20: start bit for time block, always 1
            1,0,1,0,0,0,1,                # 21-27: min = 1, 2, 4, 8, 10, 20, 40 -- 45
            1,                            # 28: check bit for minutes: 0 = even, 1 = odd
            0,0,1,0,1,0,                  # 29-34: hours
            0,                            # 35: check bit
            1,0,0,0,0,0,                  # 36-41: day within month
            1,1,1,                        # 42-44: day of week (1-7)
            1,0,0,0,0,                    # 45-49: month
            0,1,1,0,0,0,0,0,              # 50-57: year
            1,                            # 58: check bit, here 1
            2,
            0,                            # 0: always 0
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,  # 1-14: reserved/ unused
            0,                            # 15: 0 =default antenna
            0,                            # 16: 0 = no mez/mesz-change
            0,1,                          # 17-18: 01= mez
            0,                            # 19: no leap second with next 59 sec
            1,                            # 20: start bit for time block, always 1
            0,1,1,0,0,0,1,                # 21-27: min = 1, 2, 4, 8, 10, 20, 40 -- 46
            1,                            # 28: check bit for minutes: 0 = even, 1 = odd
            0,0,1,0,1,0,                  # 29-34: hours
            0,                            # 35: check bit
            1,0,0,0,0,0,                  # 36-41: day within month
            1,1,1,                        # 42-44: day of week (1-7)
            1,0,0,0,0,                    # 45-49: month
            0,1,1,0,0,0,0,0,              # 50-57: year
            1,                            # 58: check bit, here 1
            2
            )

        print "bit pos | expected | result  | error"

        for i in range(len(result_data)):
            comment = ""
            if expected_result[i] != result_data[i]:
                comment = "error"
            print "%03d     | %d        | %d       | %s" % (i,
                  expected_result[i], result_data[i], comment)
            
        self.assertFloatTuplesAlmostEqual (expected_result, result_data, len(expected_result))

    def test_002_clock_to_tx (self):
        sample_rate = 10
        expected_result = [0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           0.25, 0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

        cl = dcf77.clock(14, 44, 1, 7, 1, 6, 2)
        tx = dcf77.mod(sample_rate)

        dst = gr.vector_sink_f ()
        self.fg.connect (cl, tx, dst)

        self.fg.run ()
        result_data = dst.data()[0:len(expected_result)]
        
        self.assertFloatTuplesAlmostEqual( expected_result, result_data,
                                           len(expected_result))


if __name__ == '__main__':
    gr_unittest.main ()
