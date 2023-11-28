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

"""Module contianing definitions of the dataclasses
which are kept in the database
"""

from dataclasses import dataclass


@dataclass
class Observable:
    name: str
    identifier: int = None

@dataclass
class ObservableEx:
    observable: Observable
    paper_reference: str

@dataclass
class Analysis:
    identifier: str # paper number

    dataset: list
    title: str

    # dict of uncertainties *per observable*
    total_systematic_uncertainty: dict = None
    total_statistical_uncertainty: dict = None

    ana: str = None #  not really needed
    
    url: str = None
    journal_reference: str = None
    preprint: str = None
    enabled: bool = True

    # list of ObservableEx objects
    observables: dict = None

    # list of identifiers
    obsolete_observables: list = None

    extra_info_html: str = None

    # dict of uncertainties *per observable*
    specified_statistical_uncertainties: dict = None
    specified_systematic_uncertainties: dict = None

    tuple_path: str = None

    def __str__(self):
        return_string = f"-------- {self.identifier} ----\n"
        return_string += "| Title: "
        return_string += self.title + "\n"
        return_string += "| ana: " + str(self.ana) + "\n"

        return_string += "| dataset: "
        return_string += ", ".join( [str(j) for j in self.dataset] )
        return_string += "\n"

        return_string += "| url: " + str(self.url) + "\n"
        return_string += "| preprint: " + str(self.preprint) + "\n"
        return_string += "| journal_reference: " + str(self.journal_reference) + "\n"
        return_string += "| tuple_path: " + str(self.tuple_path) + "\n"

        return_string += "| observables \n"

        for o_id, o_ex in self.observables.items():
            o = o_ex.observable
            return_string += f"|   > [{o_id!s}] '{o.name}' (paper_reference '{o_ex.paper_reference}') \n"

        return_string += "| Uncertainties \n"
        if not isinstance(self.total_statistical_uncertainty, dict):
            return_string += "| ! Invalid type / not set \n"
        else:
            for o_id, stat_error in self.total_statistical_uncertainty.items():
                o = self.observables[ o_id ].observable

                syst_error = self.total_systematic_uncertainty[ o_id ]

                return_string += f"|   > [{o.name}] {stat_error} Stat.\n"
                return_string += f"|   > [{o.name}] {syst_error} Syst.\n"


        return_string += "| Specified Uncertainties: statistical \n"
        if not isinstance(self.specified_statistical_uncertainties, dict):
            return_string += "| ! Invalid type / not set \n"
        else:
            for o_id, uncertainty_information in self.specified_statistical_uncertainties.items():
                o = self.observables[ o_id ].observable

                for uncertainty_name, stat_error in uncertainty_information.items():
                    return_string += f"|   > [{o.name}] {stat_error} Stat ('{uncertainty_name}') \n"

        return_string += "| Specified Uncertainties: systematic \n"
        if not isinstance(self.specified_systematic_uncertainties, dict):
            return_string += "| ! Invalid type / not set \n"
        else:
            for o_id, uncertainty_information in self.specified_systematic_uncertainties.items():
                o = self.observables[ o_id ].observable

                for uncertainty_name, stat_error in uncertainty_information.items():
                    return_string += f"|   > [{o.name}] {stat_error} Syst ('{uncertainty_name}') \n"

        return_string += "| obsolete_observables \n"
        if self.obsolete_observables is not None:
            for o_id in self.obsolete_observables:
                o = self.observables[o_id].observable
                return_string += f"|   > [{o_id!s}] '{o.name}' (paper_reference '{o_ex.paper_reference}') \n"
        else:
            return_string += "|   > None \n"
            

        return_string += "-------------------"

        return return_string
        


""" Internal structure only """
@dataclass
class CorrelatedError:
    analysis_identifier_A: str
    observable_identifier_A: int
    specified_uncertainty_name_A: str

    analysis_identifier_B: str
    observable_identifier_B: int
    specified_uncertainty_name_B: str

    correlation_coefficient: float
