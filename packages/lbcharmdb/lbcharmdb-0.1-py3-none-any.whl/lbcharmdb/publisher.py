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

"""Application to reduce the verbose analysis & correlation
database to the minimum required for the correlation website (front-end)

Takes two arguments: the path to the internal database, and a path to the
envisioned external 'public' database.
"""

import json

from . import utilities


def calculate_correlation_coefficient( analysis_a, analysis_b,
                                o_a_id, o_b_id, 
                                correlations ) -> float:
    uncertainty_a = analysis_a.total_statistical_uncertainty[o_a_id]
    uncertainty_b = analysis_b.total_statistical_uncertainty[o_b_id]

    # force the correlation to be 1 for itself
    if analysis_a == analysis_b and o_a_id == o_b_id:
        return 1.0

    cov_element_total = 0.0
    for name_uncertainty_a, analy_b_info in correlations.items():
        # strip "stat:" from name
        name_uncertainty_a_stripped = name_uncertainty_a[5:]
        cov_element_A = analysis_a.specified_statistical_uncertainties[o_a_id][ name_uncertainty_a_stripped ]
        
        for name_uncertainty_b, correlation in analy_b_info.items():
            # strip "stat:" from name
            name_uncertainty_b_stripped = name_uncertainty_b[5:]
            cov_element_B = analysis_b.specified_statistical_uncertainties[o_b_id][ name_uncertainty_b_stripped ]
            cov_element_total += correlation * cov_element_A * cov_element_B
        
    return cov_element_total/(uncertainty_a*uncertainty_b)

def get_default_url( id:str ) -> str:
    """ Uses the LHCbProject public website URL """
    
    return f"https://lhcbproject.web.cern.ch/lhcbproject/Publications/LHCbProjectPublic/{id}.html"

class DatabaseSummary:
    def __init__( self, output_file_directory ):
        self.analyses = {}
        self.cov_matrices = {}
        self.index = []
        self.output_file_directory = utilities.ensure_trailing_slash(output_file_directory)
    
    def convert_database( self, db ):
        observable_orders = {}

        for a_id in db.analyses.keys():
            analysis = db.get_analysis( a_id )

            if not analysis.enabled:
                continue

            self.analyses[ a_id ] = {}
            self.analyses[ a_id ]["title"] = analysis.title
            self.analyses[ a_id ]["journal_reference"] = analysis.journal_reference
            self.analyses[ a_id ]["preprint"] = analysis.preprint
            self.analyses[ a_id ]["dataset"] = analysis.dataset

            if analysis.url is None:
                self.analyses[ a_id ]["more_information"] = get_default_url( a_id )
            else:
                self.analyses[ a_id ]["more_information"] = analysis.url
            self.analyses[ a_id ]["extra_info_html"] = analysis.extra_info_html
            self.analyses[ a_id ]["observables"] = []
            observable_orders[ a_id ] = []

            for o_id, o_ex in analysis.observables.items():
                self.analyses[ a_id ]["observables"] += [ f"{o_ex.observable.name} [{o_ex.paper_reference}]" ]
                observable_orders[ a_id ] += [ o_id ]

        self.index = list(self.analyses.keys())

        #  this loop is over enabled analyses only
        #{
        #    "LHCb-PAPER-2019-002": [[0.13, 0.04, -0.004]],
        #    "LHCb-PAPER-2022-024": [[1.0]]
        #}
        for ana_a, _ana_a_data in self.analyses.items():
            cov = {}
            analysis_A = db.get_analysis( ana_a )
            #self.cov_matrices[ ana_a ] = {}

            for ana_b, _ana_b_data in self.analyses.items():
                analysis_B = db.get_analysis( ana_b )
                cov[ ana_b ] = []
                
                for o_a_id in observable_orders[ ana_a ]:
                    cov_for_this_observable = []

                    for o_b_id in observable_orders[ ana_b ]:
                        total_correlation = 0.0

                        if ana_a == ana_b and o_a_id == o_b_id:
                            total_correlation = 1.0
                        else:
                            # check if correlation is known
                            correlations = db.get_correlations( ana_a, o_a_id, ana_b, o_b_id )
                            if correlations:
                                total_correlation = calculate_correlation_coefficient( analysis_A, 
                                            analysis_B, o_a_id, o_b_id, correlations )
                        
                        cov_for_this_observable += [ total_correlation ]
                    
                    cov[ ana_b ] += [ cov_for_this_observable ]
            
            self.cov_matrices[ ana_a ] = cov

    def write( self ):
        # write json files
        base = self.output_file_directory
        utilities.check_output_directory( base )

        cov_matrix_directory = f"{base}/cov_matrices/"
        utilities.check_output_directory( cov_matrix_directory )

        with open(f"{base}/index.json", "w") as handle:
            json.dump({"activated_papers": self.index}, handle, indent=1 )
        
        for analysis_key in self.index:
            with open( f"{base}/{analysis_key}.json", "w") as handle:
                json.dump( self.analyses[ analysis_key ], handle, indent=1 )

            with open( f"{cov_matrix_directory}/{analysis_key}.json", "w") as handle:
                json.dump( self.cov_matrices[ analysis_key ], handle, indent=1 )

        return

def publish( database, output_file_directory: str ):
    db_summary = DatabaseSummary( output_file_directory )
    db_summary.convert_database( database )
    db_summary.write()