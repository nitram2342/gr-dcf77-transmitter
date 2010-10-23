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
#ifndef INCLUDED_DCF77_MOD_H
#define INCLUDED_DCF77_MOD_H

#include <gr_block.h>

class dcf77_mod;

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
typedef boost::shared_ptr<dcf77_mod> dcf77_mod_sptr;

/*!
 * \brief Return a shared_ptr to a new instance of dcf77_mod.
 *
 * To avoid accidental use of raw pointers, dcf77_mod's
 * constructor is private.  dcf77_make_mod is the public
 * interface for creating new instances.
 */
dcf77_mod_sptr dcf77_make_mod (long sample_rate);

/*!
 * \brief generate AM modulated carrier signal from bit input stream
 * \ingroup block
 *
 */

const int STATE_AMPL_SEND_0_low = 0;
const int STATE_AMPL_SEND_0_high = 1;
const int STATE_AMPL_SEND_1_low = 2;
const int STATE_AMPL_SEND_1_high = 3;
const int STATE_AMPL_NO_MOD = 4;

class dcf77_mod : public gr_block
{
private:


  // The friend declaration allows dcf77_make_mod to
  // access the private constructor.

  friend dcf77_mod_sptr dcf77_make_mod (long sample_rate);

  dcf77_mod (long sample_rate);	// private constructor

  bool state_change;
  long sample_rate;
  //long samples_produced;
  int state;
  float ampl;
  int next_state;
  long hold_state_for_n_samples;

 public:
  ~dcf77_mod ();	// public destructor

  void forecast(int noutput_items, gr_vector_int &ninput_items_required);

  // Where all the action really happens

  int general_work (int noutput_items,
		    gr_vector_int &ninput_items,
		    gr_vector_const_void_star &input_items,
		    gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DCF77_MOD_H */
