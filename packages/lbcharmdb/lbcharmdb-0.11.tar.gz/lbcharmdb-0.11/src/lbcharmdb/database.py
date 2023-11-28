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

"""Module contianing the main database class,
along with the i/o functionality to persist and 
read this database in a JSON format.
"""

import json
import logging
from dataclasses import asdict
from typing import Optional

from . import utilities
from .db_classes import Analysis, CorrelatedError, Observable, ObservableEx
from .publisher import DatabaseSummary


def construct_observables_from_json( json_data: dict ) -> dict:
    """Reads the result of a json.load and turns it into 
    observable objects, in their dictionary form """

    observables = {}

    for observable_key, o in json_data.items():
        observables[ int(observable_key) ] = Observable( identifier=o["identifier"],
                        name=o["name"] )
    
    return observables

def construct_analyses_from_json( json_data: dict, observables: dict,
                        optional_parameters: list ) -> dict:
    """Reads the result of a json.load and turns it into 
    analysis objects, in their dictionary form """
    analyses = {}

    for a_key, a in json_data.items():
        analysis_observable_links = {}
        specified_statistical_uncertainties = {}
        specified_systematic_uncertainties = {}
        
        total_statistical_uncertainties = {}
        total_systematic_uncertainties = {}

        for _o_id, o_ex in a["observables"].items():
            observable_id = int(o_ex["observable_id"])
            paper_reference = o_ex["paper_reference"]
            
            if observable_id not in observables:
                logging.error (f"Observable id {observable_id} not found in observables.")
                return False
            
            observable = observables[ observable_id ]

            analysis_observable_links[ observable_id ] = ObservableEx(observable=observable, 
                                                            paper_reference = paper_reference)
            
            specified_statistical_uncertainties[ observable_id ] = a["specified_statistical_uncertainties"][ str(o_ex["observable_id"]) ]
            specified_systematic_uncertainties[ observable_id ] = a["specified_systematic_uncertainties"][ str(o_ex["observable_id"]) ]
            total_statistical_uncertainties[ observable_id ] = a["total_statistical_uncertainty"][ str(o_ex["observable_id"]) ]
            total_systematic_uncertainties[ observable_id ] = a["total_systematic_uncertainty"][ str(o_ex["observable_id"]) ]
        
        for opt_param in optional_parameters:
            if opt_param not in a:
                a[ opt_param ] = None
        
        analyses[ a_key ] = Analysis( identifier=a_key,
                        dataset=a["dataset"],
                        ana=a["ana"],
                        title=a["title"],
                        total_statistical_uncertainty=total_statistical_uncertainties,
                        total_systematic_uncertainty=total_systematic_uncertainties,
                        url=a["url"],
                        journal_reference=a["journal_reference"],
                        preprint=a["preprint"],
                        observables = analysis_observable_links,
                        obsolete_observables = a["obsolete_observables"],
                        extra_info_html = a["extra_info_html"],
                        specified_statistical_uncertainties = specified_statistical_uncertainties,
                        specified_systematic_uncertainties = specified_systematic_uncertainties,
                        tuple_path = a["tuple_path"]
                        )
    
    return analyses

def construct_correlations_from_dict( json_data: dict ) -> dict:
    correlation_dict = {}

    for analysis_key, other_analysis_dicts in json_data.items():
        correlation_dict[ analysis_key ] = {}

        for other_analysis_key, c in other_analysis_dicts.items():
            ab_specific_dict = {}

            for observable_A_id, observable_A_correlations in c.items():
                ab_specific_dict[ int(observable_A_id) ] = {}

                for observable_B_id, observable_B_correlations in observable_A_correlations.items():
                    ab_specific_dict[ int(observable_A_id) ][ int(observable_B_id) ] = {}

                    for specific_uncertainty_name_A, c_v in observable_B_correlations.items():
                        ab_specific_dict[ int(observable_A_id) ][ int(observable_B_id) ][ specific_uncertainty_name_A ] = c_v

            correlation_dict[ analysis_key ][ other_analysis_key ] = ab_specific_dict
    
    return correlation_dict


class CharmCorrelationDatabase:
    """ Loads a full JSON db into memory, 
    allowing local manipulations. Database
    is persisted using 'flush', after which the 
    db is written to a temporary location (nothing
    is overwitten) """

    version = 0.1
    metadata_file_name     = "metadata.json"
    observable_file_name   = "observables.json"
    analyses_file_name     = "analyses.json"
    correlations_file_name = "correlations.json"

    DIRECTORY_SLUG_FULL_DB    = "full/"
    DIRECTORY_SLUG_SUMMARY_DB = "summary/"

    def __init__( self, input_directory: str, 
                  output_directory: Optional[str] = None):
        if output_directory is None:
            output_directory = input_directory
        
        self.input_directory = utilities.ensure_trailing_slash( input_directory )
        self.output_directory = utilities.ensure_trailing_slash( output_directory )

        self.analyses = {}
        self.observables = {}
        self.correlations = {}
        self.initialized = False

        self.n_analyses_updated = 0
        self.n_analyses_added = 0
        self.logger = logging.getLogger("CharmCorrelationDb")

        self.encountered_errors = []
    
    def get_analyses( self ) -> dict:
        return self.analyses
    
    def get_observables( self ) -> dict:
        return self.observables
    
    def encounter_error( self, message: str ):
        self.encountered_errors += [ message ]
        self.logger.error( self.encountered_errors[-1] )
    
    """
    Main I/O controllers
    """
    def load( self, optional_analysis_parameters: Optional[list]=None ) -> bool:
        self.logger.info(f"Loading in data from full database at '{self.input_directory}/full'")
        # load json files
        if optional_analysis_parameters is None:
            optional_analysis_parameters = []
        base = self.input_directory + self.DIRECTORY_SLUG_FULL_DB
        metadata_file_name = f"{base}{self.metadata_file_name}"
        observable_file_name = f"{base}{self.observable_file_name}"
        analyses_file_name = f"{base}{self.analyses_file_name}"
        correlations_file_name = f"{base}{self.correlations_file_name}"

        for f in [metadata_file_name, 
                    observable_file_name, 
                    analyses_file_name, 
                    correlations_file_name]:
            if not utilities.file_exists( f ):
                self.logger.fatal(f"File does not exist {f}")
                return

        with open(metadata_file_name) as handle:
            ok = self.parse_json_metadata( json.load(handle) )

        if ok:
            with open(observable_file_name) as handle:
                ok = self.parse_json_observables( json.load(handle) )

        if ok:
            with open(analyses_file_name) as handle:
                ok = self.parse_json_analyses( json.load(handle), optional_analysis_parameters )
        
        if ok :
            with open(correlations_file_name) as handle:
                ok = self.parse_json_correlations( json.load(handle) )
        
        if not ok:
            self.encounter_error("Error at loading - database not initialised.")


        if self.input_directory == self.output_directory:
            if not utilities.directory_exists( self.input_directory + ".git" ):
                self.logger.warning("Input directory and output directory are the same. " 
                                "Please remember to use version control.")
            else:
                self.logger.info("Input directory and output directory are the same. " 
                                "Git repository found for version control.")
        
        self.logger.info("Initialised database.")
        
        self.initialized = ok

        return ok
    
    def flush(self, *, write_summary: bool = True):
        if len(self.encountered_errors):
            self.logger.error("Not continuing with flushing this database - errors were found.")
            return
        
        # write json files
        base = self.output_directory + self.DIRECTORY_SLUG_FULL_DB
        write_summary_to = self.output_directory + self.DIRECTORY_SLUG_SUMMARY_DB

        utilities.check_output_directory( self.output_directory )
        utilities.check_output_directory( base )
        utilities.check_output_directory( write_summary_to )

        metadata_file_name = f"{base}{self.metadata_file_name}"
        observable_file_name = f"{base}{self.observable_file_name}"
        analyses_file_name = f"{base}{self.analyses_file_name}"
        correlations_file_name = f"{base}{self.correlations_file_name}"

        with open(metadata_file_name, "w") as handle:
            json.dump( self.serialize_metadata(), handle, indent=1 )
        
        with open(observable_file_name, "w") as handle:
            json.dump( self.serialize_observables(), handle, indent=1 )

        with open(analyses_file_name, "w") as handle:
            json.dump( self.serialize_analyses(), handle, indent=1 )
        
        with open(correlations_file_name, "w") as handle:
            json.dump( self.serialize_correlations(), handle, indent=1)
        
        if write_summary:
            utilities.check_output_directory( write_summary_to )
            db_summary = DatabaseSummary( write_summary_to )
            db_summary.convert_database( self )
            db_summary.write()

        return
    
    """
    Metadata functionality
    """
    def parse_json_metadata( self, json_data ) -> bool:
        if self.version != json_data["version"]:
            error_message =  f"Trying to read data version {json_data['version']} with application version {self.version}. "
            error_message += "Convert the data before."

            self.logger.error( error_message )
        
        return (self.version == json_data["version"])
    
    def serialize_metadata( self ) -> dict:
        return {"version": self.version}
    
    """
    Observable functionality
    """
    
    def parse_json_observables( self, json_data ) -> dict:
        """Unpack observables from json dictionary """
        observables = construct_observables_from_json( json_data )

        v = self.verify_observables( observables )

        if ( v ):
            self.observables = observables
            return True
        else:
            self.encounter_error("Could not laod observables.")
            return v
    
    def serialize_observables( self ) -> dict:
        """Pack observables to json dict"""
        return_dict = {}

        for _o_id, o in self.observables.items():
            return_dict[ o.identifier ] = asdict( o )
        
        return return_dict

    def get_observable_by_id( self, identifier: int ) -> Observable:
        """ Searches the known observables to find the one by name,
        where name is case-insensitive"""

        if identifier not in self.observables:
            return False
        
        return self.observables[ identifier ]
    

    def get_observable_by_name( self, name: str ) -> Observable:
        """ Searches the known observables to find the one by name,
        where name is case-insensitive"""

        for _o_key,o in self.observables.items():
            if o.name.lower() == name.lower():
                return o
        
        return False
    
    def get_or_add_observable_by_name( self, name:str ):
        return self.add_or_update_observable( Observable(name=name) )
    
    def add_or_update_observable( self, observable: Observable ):
        """ Adds, or updates an observable in the database. In case of adding
        a new observable, the identifier is set with the last available. """

        if observable.identifier is None:
            # get the last identifier available
            if self.get_observable_by_name( observable.name ):
                self.logger.info(f"Observable with name {observable.name} already known; returning it.")
                return self.get_observable_by_name(observable.name)
            
            if len(self.observables.keys()):
                o_key = max( self.observables.keys() ) + 1
            else:
                o_key = 0

            observable.identifier = o_key

        if observable.identifier in self.observables:
            self.logger.info( f"Updating observable {observable.identifier} ('{self.observables[observable.identifier].name}')" )
            self.logger.debug( f"Observable name: '{self.observables[observable.identifier].name}' => '{observable.name}'" )
        else:
            self.logger.info( f"Adding observable '{observable.name}' (number {observable.identifier})" )
        
        self.observables[ observable.identifier ] = observable

        return observable

    def verify_observables_exist( self, observable_list: list ) -> bool:
        """ Tests whether all observables are registered 
        in the db."""

        for observable_name in observable_list:
            if observable_name not in self.observables:
                self.logger.warning( f"Observable {observable_name} not known")
                return False
        
        return True
    
    def verify_observables( self, observables: dict ) -> bool:
        for o_key, o in observables.items():
            if o.name == "":
                self.logger.warning(f"Observable key '{o_key}' has an empty name")
                return False
            
            if o_key != o.identifier:
                self.logger.warning(f"Observable key '{o_key}' does not match id '{o.identifier}'")
                return False
        
        return True
    
    """ 
    Analysis functionaltiy
    """
    def parse_json_analyses( self, json_data, optional_analysis_parameters:list ) -> dict:
        """Analysis unpacking"""
        analyses = construct_analyses_from_json( json_data, self.observables, optional_analysis_parameters )

        v = self.verify_analyses( analyses )

        if ( v ):
            self.analyses = analyses
            return True
        else:
            self.encounter_error("Could not laod analyses.")
            return v
    
    def serialize_analyses( self ) -> dict:
        return_dict = {}

        for _a_id, a in self.analyses.items():
            return_dict[ a.identifier ] = self.serialize_analysis( a )
        
        return return_dict
    
    def serialize_analysis( self, analysis: Analysis ) -> dict:
        return_dict = {}
        return_dict = asdict ( analysis )
        
        # Remove the deeper observable links
        for _o_ex_id, o_ex_dict in return_dict["observables"].items():
            o_ex_dict["observable_id"] = o_ex_dict["observable"]["identifier"]
            del o_ex_dict["observable"]
        
        return return_dict
    
    def verify_analyses( self, analyses: dict ):
        v = True

        for _a_id, a in analyses.items():
            v = v and (self.verify_analysis( a ))
        
        return v
    
    def verify_analysis_identifier( self, identifier ):
        if identifier[0:5] != "LHCb-":
            self.encounter_error (f"Analysis identifier '{identifier}' does not start with LHCb-")
            return False
        
        if " " in identifier or '\n' in identifier or '\t' in identifier:
            self.encounter_error (f"Analysis identifier '{identifier}' contains empty characters")
            return False
        
        if identifier == "":
            self.encounter_error( f"Incorrect identifier for analysis {identifier}" )
            return False
        
        return True
    
    def verify_analysis( self, analysis: Analysis ):
        identifier = analysis.identifier

        # as dataclasses aren't allowed to have mutable
        # defaults, set these in here.
        if analysis.observables is None:
            analysis.observables = {}

        if not self.verify_analysis_identifier( analysis.identifier ):
            self.encounter_error( "Identifier failed check.")
            return False
            
        if not self.verify_observables_exist( analysis.observables ):
            self.encounter_error( f"Observables part of analysis {identifier} not known.")
            return False
        
        if not len(analysis.dataset):
            self.encounter_error( f"No dataset registered for analysis {identifier}")
            return False

        if not len(analysis.observables):
            self.encounter_error( f"No observables registered for analysis {identifier}")
            return False

        if analysis.title == "":
            self.encounter_error( f"Title missing for analysis {identifier}")
            return False

        if analysis.ana == "":
            self.encounter_error( f"ANA number missing for analysis {identifier}")
            return False
        
        # we should know the total uncertainty per observable
        if len(analysis.total_statistical_uncertainty) != len(analysis.observables):
            self.encounter_error( f"The number of stat uncertainties for analysis {identifier} " \
                                    "is different from the number of observables.")
            return False

        if len(analysis.total_systematic_uncertainty) != len(analysis.observables):
            self.encounter_error( f"The number of syst uncertainties for analysis {identifier} " \
                                    "is different from the number of observables.")
            return False

        return True

    def add_or_update_analysis( self, updated_analysis: Analysis ) -> bool:
        if not self.initialized:
            self.logger.fatal("Trying to update an analysis on a non-initialised database.")
            return False
        
        identifier = updated_analysis.identifier
        if not self.verify_analysis( updated_analysis ):
            self.logger.fatal(f"Analysis information for {identifier} incomplete")
            return False

        if updated_analysis.specified_statistical_uncertainties is None:
            updated_analysis.specified_statistical_uncertainties  = {}
            updated_analysis.specified_systematic_uncertainties  = {}

            for _observable_id, _o_ex in updated_analysis.observables:
                observable = _o_ex.observable
                updated_analysis.specified_statistical_uncertainties[observable.identifier] = \
                                        {"total": updated_analysis.total_statistical_uncertainty[_observable_id]}
                updated_analysis.specified_systematic_uncertainties[observable.identifier] = \
                                        {"total": updated_analysis.total_statistical_uncertainty[_observable_id]}

        if identifier in self.analyses:
            self.analyses[ identifier ] = updated_analysis
            self.n_analyses_updated += 1
        else:
            self.analyses[ identifier ] = updated_analysis
            self.n_analyses_added += 1
            self.logger.info(f"Analysis '{identifier}' added.")
        
        return True

    def change_analysis_identifier( self, analysis_identifier_before:str, analysis_identifier_after:str ) -> bool:
        """ Try to avoid using this! 
        TODO: Create an 'alias table' to preserve previous links"""

        if not self.verify_analysis_identifier( analysis_identifier_after ):
            return False

        if analysis_identifier_after[0:5] != "LHCb-":
            self.enocunter_error (f"Analysis identifier '{analysis_identifier_after}' does not start with LHCb-")
            return False
        
        if " " in analysis_identifier_after or '\n' in analysis_identifier_after or '\t' in analysis_identifier_after:
            self.enocunter_error (f"Analysis identifier '{analysis_identifier_after}' contains empty characters")
            return False

        if analysis_identifier_before not in self.analyses:
            self.encounter_error(f"Analysis with name '{analysis_identifier_before}' not known.")
            return False

        if analysis_identifier_after.lower() in [ k.lower() for k in self.analyses ]:
            self.encounter_error(f"Analysis with name '{analysis_identifier_after}' *already* known (matched case-insensitive).")
            return False

        analysis = self.analyses[ analysis_identifier_before ]
        analysis.identifier = analysis_identifier_after
        del self.analyses[ analysis_identifier_before]
        
        self.analyses[ analysis_identifier_after ] = analysis

        self.logger.info(f"Changed analysis identifier '{analysis_identifier_before}' => '{analysis_identifier_after}'")

        # TODO: Update correlation tables
        #self.correlations = None;

        return True
    
    def get_analysis( self, identifier: str ) -> Analysis:
        if not self.verify_analysis_identifier( identifier ):
            return False
        
        if identifier in self.analyses:
            return self.analyses[ identifier ]
        
        self.logger.warning(f"Could not find analysis '{identifier}'")
        return False


    """
    Correlation functionality
    """
    def serialize_correlations( self ) -> dict:
        return self.correlations # this is a flat dictionary
    
    def parse_json_correlations( self, json_data ) -> list:
        self.correlations = construct_correlations_from_dict( json_data )

        return self.verify_correlations( self.correlations )
    
    def verify_correlations( self, correlation_list: dict ) -> bool:
        for analysis_A_key, a_A_corrs in correlation_list.items():
            if analysis_A_key not in self.analyses:
                self.encounter_error(f"Correlated analysis '{analysis_A_key}' not found.")
                return False
            
            analysis_A = self.get_analysis( analysis_A_key )
            
            for analysis_B_key, observables_A in a_A_corrs.items():
                if analysis_B_key not in self.analyses: 
                    self.encounter_error(f"Correlated analysis '{analysis_B_key}' not found.")
                    return False
                
                analysis_B = self.get_analysis( analysis_B_key )
                
                for observable_A_key, observables_B in observables_A.items():
                    if observable_A_key not in analysis_A.observables:
                        self.encounter_error(f"Observable '{observable_A_key}' not found for analysis '{analysis_A_key}'.")
                        return False
                    
                    self.get_observable_by_id( observable_A_key )

                    for observable_B_key, correlation_specification in observables_B.items():
                        if observable_B_key not in analysis_B.observables:
                            self.encounter_error(f"Observable '{observable_B_key}' not found for analysis '{analysis_B_key}'.")
                            return False

                        for c_name in correlation_specification:
                            if c_name[0:5] != "stat":
                                continue
                            
                            c_name_adjusted = c_name[5:]
                            if c_name_adjusted not in analysis_A.specified_statistical_uncertainties[ observable_A_key ]:
                                self.encounter_error(f"Correlation for uncertainty part '{c_name_adjusted}' not found " \
                                                        "for analysis '{analysis_A_key}'.")
                                return False
            
        return True
    
    def make_and_register_correlation( self, *,
                            analysis_A, observable_A, 
                            analysis_B, observable_B, 
                            correlation_coefficient,
                            specified_uncertainty_name_A: str = "total", 
                            is_statistical_uncertainty_A: bool=True,
                            specified_uncertainty_name_B: str = "total", 
                            is_statistical_uncertainty_B: bool=True ):
        if isinstance( analysis_A, str):
            # get the analysis by str
            analysis_A = self.get_analysis( analysis_A )

            if not analysis_A:
                self.encounter_error(f"Could not find analysis {analysis_A}")
                return False
        if isinstance(analysis_B, str):
            # get the analysis by str
            analysis_B = self.get_analysis( analysis_B )

            if not analysis_B:
                self.encounter_error(f"Could not find analysis {analysis_B}")
                return False
        
        if isinstance(observable_A, str):
            # get the analysis by str
            observable_A = self.get_observable_by_name( observable_A )

            if not observable_A:
                self.encounter_error(f"Could not find observable {observable_A}")
                return False
        
        if isinstance(observable_B, str):
            # get the analysis by str
            observable_B = self.get_observable_by_name( observable_B )

            if not observable_B:
                self.encounter_error(f"Could not find observable {observable_B}")
                return False
        
        # check if observable_A in analysis_A
        if observable_A.identifier not in analysis_A.observables:
            self.encounter_error(f"Observable '{observable_A.name}' not found for analysis '{analysis_A.identifier}'")
            return False

        if observable_B.identifier not in analysis_B.observables:
            self.encounter_error(f"Observable '{observable_B.name}' not found for analysis '{analysis_B.identifier}'")
            return False

        if is_statistical_uncertainty_A:
            specified_uncertainty_name_A = "stat:" + specified_uncertainty_name_A 
        else:
            specified_uncertainty_name_A = "syst:" + specified_uncertainty_name_A
        
        if is_statistical_uncertainty_B:
            specified_uncertainty_name_B = "stat:" + specified_uncertainty_name_B 
        else:
            specified_uncertainty_name_B = "syst:" + specified_uncertainty_name_B

        # add correlation to database
        correlated_error = CorrelatedError( analysis_identifier_A=analysis_A.identifier, 
                                observable_identifier_A=observable_A.identifier,
                                specified_uncertainty_name_A=specified_uncertainty_name_A,
                                analysis_identifier_B=analysis_B.identifier,
                                observable_identifier_B=observable_B.identifier,
                                specified_uncertainty_name_B=specified_uncertainty_name_B,
                                correlation_coefficient=correlation_coefficient )
        self.register_correlation( correlated_error )

        return correlated_error

    def register_correlation( self, c_e: CorrelatedError ) -> bool:
        if c_e.analysis_identifier_A not in self.correlations:
            self.correlations[ c_e.analysis_identifier_A ] = {}
        
        if c_e.analysis_identifier_B not in self.correlations[ c_e.analysis_identifier_A ]:
            self.correlations[ c_e.analysis_identifier_A ][ c_e.analysis_identifier_B ] = {}

        if c_e.observable_identifier_A not in self.correlations[ c_e.analysis_identifier_A ][ c_e.analysis_identifier_B ]:
            self.correlations[ c_e.analysis_identifier_A ][ c_e.analysis_identifier_B ][ c_e.observable_identifier_A ] = {}

        shortcut = self.correlations[ c_e.analysis_identifier_A ][ c_e.analysis_identifier_B ][ c_e.observable_identifier_A ]
        if c_e.observable_identifier_B not in shortcut:
            shortcut[ c_e.observable_identifier_B ] = {}

        if c_e.specified_uncertainty_name_A not in shortcut[ c_e.observable_identifier_B ]:
            shortcut[ c_e.observable_identifier_B ][ c_e.specified_uncertainty_name_A ] = {}
        deeper_shortcut = shortcut[ c_e.observable_identifier_B ][ c_e.specified_uncertainty_name_A ]
        deeper_shortcut[ c_e.specified_uncertainty_name_B ] = c_e.correlation_coefficient

        shortcut[ c_e.observable_identifier_B ][ c_e.specified_uncertainty_name_A ] = deeper_shortcut
        self.correlations[ c_e.analysis_identifier_A ][ c_e.analysis_identifier_B ][ c_e.observable_identifier_A ] = shortcut

        # Now swap A <-> B
        if c_e.analysis_identifier_B not in self.correlations:
            self.correlations[ c_e.analysis_identifier_B ] = {}
        
        if c_e.analysis_identifier_A not in self.correlations[ c_e.analysis_identifier_B ]:
            self.correlations[ c_e.analysis_identifier_B ][ c_e.analysis_identifier_A ] = {}

        if c_e.observable_identifier_B not in self.correlations[ c_e.analysis_identifier_B ][ c_e.analysis_identifier_A ]:
            self.correlations[ c_e.analysis_identifier_B ][ c_e.analysis_identifier_A ][ c_e.observable_identifier_B ] = {}

        shortcut = self.correlations[ c_e.analysis_identifier_B ][ c_e.analysis_identifier_A ][ c_e.observable_identifier_B ]
        if c_e.observable_identifier_A not in shortcut:
            shortcut[ c_e.observable_identifier_A ] = {}

        if c_e.specified_uncertainty_name_B not in shortcut[ c_e.observable_identifier_A ]:
            shortcut[ c_e.observable_identifier_A ][ c_e.specified_uncertainty_name_B ] = {}
        deeper_shortcut = shortcut[ c_e.observable_identifier_A ][ c_e.specified_uncertainty_name_B ]

        if c_e.specified_uncertainty_name_A in deeper_shortcut:
            self.logger.info("Overwriting pre-existing correlation.")
        
        deeper_shortcut[ c_e.specified_uncertainty_name_A ] = c_e.correlation_coefficient
        
        shortcut[ c_e.observable_identifier_A ][ c_e.specified_uncertainty_name_B ] = deeper_shortcut
        self.correlations[ c_e.analysis_identifier_B ][ c_e.analysis_identifier_A ][ c_e.observable_identifier_B ] = shortcut

        return True
    
    def get_correlations( self, a_id_A, observable_id_A, a_id_B, observable_id_B ) -> dict:
        if a_id_A not in self.correlations:
            return False
        
        if a_id_B not in self.correlations[ a_id_A ]:
            return False
        
        if observable_id_A not in self.correlations[ a_id_A ][ a_id_B ]:
            return False
        
        if observable_id_B not in self.correlations[ a_id_A ][ a_id_B ][ observable_id_A ]:
            return False

        return self.correlations[ a_id_A ][ a_id_B ][ observable_id_A ][ observable_id_B ]
    
    """ Helper function """
    def add_observable_to_analysis_by_name( self, analysis: Analysis, 
                        observable_name: str, 
                        paper_reference: str, 
                        statistical_uncertainty: float, 
                        systematic_uncertainty: float ):
        """Modifies the analysis and the database to add a new observable to it, 
        with a specific paper reference and stat/syst error. 

        Prepares the analysis to contain a specification of the uncertainty as well."""
        observable = self.get_or_add_observable_by_name( observable_name )
        observable_ex = ObservableEx( observable=observable, paper_reference=paper_reference )

        if analysis.observables is None:
            analysis.observables = {}
        
        analysis.observables[ observable.identifier ] = observable_ex

        if analysis.total_statistical_uncertainty is None:
            analysis.total_statistical_uncertainty = {}
        
        if analysis.total_systematic_uncertainty is None:
            analysis.total_systematic_uncertainty = {}
        
        if analysis.specified_statistical_uncertainties is None:
            analysis.specified_statistical_uncertainties = {} #{observable.identifier: {}}
        
        if analysis.specified_systematic_uncertainties is None:
            analysis.specified_systematic_uncertainties = {} #{observable.identifier: {}}
        
        if observable.identifier not in analysis.specified_statistical_uncertainties:
            analysis.specified_statistical_uncertainties[ observable.identifier ] = {}

        if observable.identifier not in analysis.specified_systematic_uncertainties:
            analysis.specified_systematic_uncertainties[ observable.identifier ] = {}
        
        analysis.total_statistical_uncertainty[ observable.identifier ] = statistical_uncertainty
        analysis.total_systematic_uncertainty[ observable.identifier ] = systematic_uncertainty

        analysis.specified_statistical_uncertainties[ observable.identifier ]["total"] = statistical_uncertainty
        analysis.specified_systematic_uncertainties[ observable.identifier ]["total"] = systematic_uncertainty

        return observable
    
    def specify_uncertainty_for_analysis( self, analysis: Analysis, 
                        observable, 
                        uncertainty_reference: str, 
                        statistical_uncertainty: float, 
                        systematic_uncertainty: float ):
        """Modifies the analysis and the database to add a new observable to it, 
        with a specific paper reference and stat/syst error. 

        Prepares the analysis to contain a specification of the uncertainty as well."""
        if isinstance(observable, str):
            observable = self.get_or_add_observable_by_name( observable )
        
        if observable.identifier not in analysis.observables:
            self.encounter_error(f"Cannot find observable '{observable.identifier}' for analysis '{analysis.identifier}'")
            return False
        
        if analysis.specified_statistical_uncertainties is None:
            analysis.specified_statistical_uncertainties = {observable.identifier: {}}
        
        if analysis.specified_systematic_uncertainties is None:
            analysis.specified_systematic_uncertainties = {observable.identifier: {}}


        if analysis.total_statistical_uncertainty[ observable.identifier ] < statistical_uncertainty:
            self.encounter_error(f"The total statistical uncertainty for '{observable.name}' " \
                                "is smaller ({analysis.total_statistical_uncertainty[ observable.identifier ]})!")
            self.encounter_error("Did you forget to multiply by percent?")
            return False

        if statistical_uncertainty > 0:
            analysis.specified_statistical_uncertainties[ observable.identifier ][ uncertainty_reference ] = statistical_uncertainty

        if systematic_uncertainty > 0:
            analysis.specified_systematic_uncertainties[ observable.identifier ][ uncertainty_reference ] = systematic_uncertainty

        return True
