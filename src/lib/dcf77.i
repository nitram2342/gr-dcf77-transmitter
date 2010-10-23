/* -*- c++ -*- */

%feature("autodoc", "1");		// generate python docstrings

%include "exception.i"
%import "gnuradio.i"			// the common stuff

%{
#include "gnuradio_swig_bug_workaround.h"	// mandatory bug fix
#include "dcf77_clock.h"
#include "dcf77_mod.h"
#include <stdexcept>
%}

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dcf77,clock);

dcf77_clock_sptr dcf77_make_clock(int hour, int min, int mday, int dow, int month, int year, int loops);

class dcf77_clock : public gr_block {

private:
  dcf77_clock(int hour, int min, int mday, int dow, int month, int year, int loops);
};


GR_SWIG_BLOCK_MAGIC(dcf77,mod);

dcf77_mod_sptr dcf77_make_mod(long sample_rate);

class dcf77_mod : public gr_block {

private:
  dcf77_mod(long sample_rate);
};

