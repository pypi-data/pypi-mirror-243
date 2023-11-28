###############################################################################
# (c) Copyright 2023 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

import collections
import os
import random
import string


def as_list(x, length=1) -> list:
    """Return x if it is a list, else return x wrapped in a list."""
    if not isinstance(x, list):
        x = length*[x]
    return x


def update(d: dict, u: dict) -> dict:
    """Updates a nested dictionary
    """
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    
    return d


def ensure_trailing_slash( directory: str ) -> str:
    """ Formats directory paths """
    return os.path.join(directory, '')


def directory_exists( directory: str ) -> bool:
    return os.path.exists(directory)


def check_output_directory( directory: str ):
    """ Will check if the directory exists, if not create it.
    """
    if not directory_exists(directory):
        os.makedirs(directory)


def file_exists ( file_name: str ) -> bool:
    """Checks if the file exists """
    return os.path.exists(file_name)


def id_generator(size=9, chars=string.ascii_uppercase) -> str:
    """ Random name generator """
    return ''.join(random.choice(chars) for _ in range(size))
