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


__all__ = ['units', 'CharmCorrelationDatabase', 'Observable', 'Analysis', 'ObservableEx', 
            'DatabaseSummary', 'publish', 'calculate_correlations_weighted_tuples']

import logging

import coloredlogs
import ROOT

from . import (
    calculate_correlations_weighted_tuples,
    units,  # expose the units module as well
)
from .database import CharmCorrelationDatabase
from .db_classes import Analysis, Observable, ObservableEx
from .publisher import DatabaseSummary, publish

ROOT.PyConfig.IgnoreCommandLineOptions = True

ROOT.TH1.SetDefaultSumw2(True)
ROOT.gROOT.SetBatch()

logging.basicConfig( level=logging.INFO )

coloredlogs.install(level='INFO')
logging.debug("Installed colored logs.")

#  expose the main classes