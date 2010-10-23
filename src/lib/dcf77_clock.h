/* -*- c++ -*- */
/*
 * Copyright 2004 Free Software Foundation, Inc.
 * 
 * This file is part of GNU Radio
 * 
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 * 
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */
#ifndef INCLUDED_DCF77_CLOCK_H
#define INCLUDED_DCF77_CLOCK_H

#include <gr_block.h>

class dcf77_clock;

/*
 * We use boost::shared_ptr's instead of raw pointers for all access
 * to gr_blocks (and many other data structures).  The shared_ptr gets
 * us transparent reference counting, which greatly simplifies storage
 * management issues.  This is especially helpful in our hybrid
 * C++ / Python system.
 *
 * See http://www.boost.org/libs/smart_ptr/smart_ptr.htm
 *
 * As a convention, the _sptr suffix indicates a boost::shared_ptr
 */
typedef boost::shared_ptr<dcf77_clock> dcf77_clock_sptr;

/*!
 * \brief Return a shared_ptr to a new instance of dcf77_clock.
 *
 * To avoid accidental use of raw pointers, dcf77_clock's
 * constructor is private.  dcf77_make_clock is the public
 * interface for creating new instances.
 */

dcf77_clock_sptr dcf77_make_clock(int hour, int min, int mday, int dow, 
				  int month, int year, int loops);

/*!
 * \brief generate AM modulated carrier signal from bit input stream
 * \ingroup block
 *
 */

class dcf77_clock : public gr_block
{
private:


  // The friend declaration allows dcf77_make_clock to
  // access the private constructor.

  friend dcf77_clock_sptr dcf77_make_clock (int hour, int min, int mday, int dow, 
					    int month, int year, int loops);

  dcf77_clock (int hour, int min, int mday, int dow, 
	       int month, int year, int loops); // private constructor

  int hour, min, mday, dow, month, year;
  int bit_buf[60];
  int bit_buf_pos;

  int loops;
  int loop_cnt;

  void fill_bit_buffer();
  int calc_bit_vector(int value, int * valency, int len, int * buf_ptr);

 public:
  ~dcf77_clock ();	// public destructor

  void forecast(int noutput_items, gr_vector_int &ninput_items_required);

  // Where all the action really happens

  int general_work (int noutput_items,
		    gr_vector_int &ninput_items,
		    gr_vector_const_void_star &input_items,
		    gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DCF77_CLOCK_H */
