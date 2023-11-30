#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: nu:ai:ts=4:sw=4

#
#  Copyright (C) 2023 Joseph Areeda <joseph.areeda@ligo.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Create gwf frame files containing a subset of channels in the full frames
covering specific time intervals.
"""

import time

start_time = time.time()

import argparse
import logging
from pathlib import Path
import re
import subprocess
import sys

try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = Path(__file__).name

logger = None


def parser_add_args(parser):
    """
    Set up command parser
    :param argparse.ArgumentParser parser:
    :return: None but parser object is updated
    """
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('--config', type=Path, nargs='*',
                        help='A convenient way to save arguments for common processes. Command line '
                             'arguments override configuration specs. Default is internal.'
                             'Use --print-defaults to use as a template')
    parser.add_argument('--print-default', action='store_true', help='show default configuration')

    in_group = parser.add_argument_group(title='in_group', description="""
    Input data specifications:
    The channel list and time intervals must be specified here or in a configuration file.
    For most channels we can discover the appropriate frame type so input channels nned 
    not be contained in the same frame type or even from the same IFO
    
    If input data is not
    """)
    in_group.add_argument('-c', '--chan', nargs='*', help='List of channels')
    in_group.add_argument('--chan-file', type=Path, help='Path to file with list of channels, 1 per line')
    in_group.add_argument('-t', '--time', nargs='*', help='Specification')

    out_group = parser.add_argument_group(title="out_group", description="""
    Output specifications:
    Multiple files may be created if data size exceeds limits, more than one IFO is involved or if time 
    intervals are not consistent.
    """)

    out_group.add_argument('-o', '--out-dir', type=Path, help='Path to output directory')
    out_group.add_argument('--frame-type', default='RDS-SUBSET',
                           help='Should be of the form <sys>-<info>[_info..] we will prepend "<ifo>:" '
                                'and append "-<gps start>-<duration>.gwf"')
    out_group.add_argument('--max-size', type=int, default=800, help='Max size of output files in megabyte')


def main():
    global logger

    logging.basicConfig()
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(description=__doc__, prog=__process_name__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_add_args(parser)
    args = parser.parse_args()
    verbosity = 0 if args.quiet else args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    # debugging?
    logger.debug(f'{__process_name__} version: {__version__} called with arguments:')
    for k, v in args.__dict__.items():
        logger.debug('    {} = {}'.format(k, v))


if __name__ == "__main__":

    main()
    if logger is None:
        logging.basicConfig()
        logger = logging.getLogger(__process_name__)
        logger.setLevel(logging.DEBUG)
    # report our run time
    logger.info(f'Elapsed time: {time.time() - start_time:.1f}s')
