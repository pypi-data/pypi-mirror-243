AM_LFLAGS = -Cf
AM_YFLAGS = -d -v -l -p libfplist_xml_scanner_

if HAVE_LOCAL_LIBFPLIST
AM_CPPFLAGS = \
	-I$(top_srcdir)/include \
	-I$(top_srcdir)/common \
	@LIBCERROR_CPPFLAGS@ \
	@LIBCDATA_CPPFLAGS@ \
	@LIBCNOTIFY_CPPFLAGS@ \
	@LIBUNA_CPPFLAGS@ \
	@LIBFGUID_CPPFLAGS@ \
	@LIBFVALUE_CPPFLAGS@ 

BUILT_SOURCES = \
	libfplist_xml_scanner.c \
	libfplist_xml_parser.c \
	libfplist_xml_parser.h

noinst_LTLIBRARIES = libfplist.la

libfplist_la_SOURCES = \
	libfplist_definitions.h \
	libfplist_extern.h \
	libfplist_error.c libfplist_error.h \
	libfplist_libcdata.h \
	libfplist_libcerror.h \
	libfplist_libcnotify.h \
	libfplist_libfguid.h \
	libfplist_libfvalue.h \
	libfplist_libuna.h \
	libfplist_property.c libfplist_property.h \
	libfplist_property_list.c libfplist_property_list.h \
	libfplist_support.c libfplist_support.h \
	libfplist_types.h \
	libfplist_unused.h \
	libfplist_xml_attribute.c libfplist_xml_attribute.h \
	libfplist_xml_parser.y \
	libfplist_xml_scanner.l \
	libfplist_xml_tag.c libfplist_xml_tag.h
endif

EXTRA_DIST = \
	libfplist_xml_parser.c libfplist_xml_parser.h \
	libfplist_xml_scanner.c

MAINTAINERCLEANFILES = \
	Makefile.in

distclean: clean
	-rm -f libfplist_xml_parser.c
	-rm -f libfplist_xml_parser.h
	-rm -f libfplist_xml_parser.output
	-rm -f libfplist_xml_scanner.c
	-rm -f Makefile

sources-local: $(BUILT_SOURCES)

splint-local:
	@echo "Running splint on libfplist ..."
	-splint -preproc -redef $(DEFS) $(DEFAULT_INCLUDES) $(INCLUDES) $(AM_CPPFLAGS) $(libfplist_la_SOURCES)

