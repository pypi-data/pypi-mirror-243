# lbcharmdb editor

This project contains the Python machinery to modify the LHCb charm correlations database.

## Introduction to nomenclature: full and summary database
The database itself consists of two parts: 
 - a "full" database, with elaborate details per analysis, including internal information
 - a "summary", which is *generated* from the full (verbose) database each time you save changes

All manipulations happen on the verbose database, and the publisher takes care of generating
the summary. A version control for the database itself is also used, with the most
recent version available at
 https://gitlab.cern.ch/lhcb-charm/correlations-database

Currently, the database manipulations happen through Python. 
When initialising this editor of the database, simply point it to the directory 
containing *both* the summary and the full database. 

## Structure
The database itself contains:
 - Observables
 - Analyses, which can have results on multiple observables
 - Correlations, which are relations between (analysis, observable) pairs

Under the hood, everything is saved in JSON files to help the debugging and
portability.

## Working with lbcharmdb: setup
Firstly, it is required to `git clone` the latest correlation database from 
```bash
git clone https://gitlab.cern.ch/lhcb-charm/correlations-database db
```
Such that you can make changes to the latest database, and create a merge request
for your changes to be published.

After this has been set up, you can use this package either via pip or via
lb-conda(TODO):
```bash
pip install lbconddb
```

You can start editing the charm database in Python. To start with, you can load the 
database:

```python
from lbcharmdb import Analysis, CharmCorrelationDatabase, DatabaseSummary, units

database = CharmCorrelationDatabase( "db/" )
database.load()
```

Note that we have loaded the entire result of the git clone, and we don't have to
worry about setting any specifics. The trailing slash in the directory path 
is optional. After the database has been loaded, it's time to manipulate it, 
following the examples below.

## Adding a new analysis
Per example, an analysis is added to the database which contains more than
one observable: three CP asymmetries are reported. 

The following opens a database, defines the analysis ("LHCb-PAPER-2019-002") and 
adds three of the observables and their results to this analysis.

Lastly, it adds the newly defined analysis to the database. 
After this step, the changes have **not yet** been written to the database; the 
'flushing' is described further below.

```python
lhcb_paper_2019_002 = Analysis( identifier="LHCb-PAPER-2019-002",
    dataset = [2015, 2016, 2017],
    preprint="arXiv:1903.01150",
    journal_reference="Phys. Rev. Lett.122 (2019) 191803",
    title=r"Search for CP violation in $Ds+ \to KS0\pi+$, $D+ \to KS0K+$ and $D+ \to \phi \pi+$ decays" 
    )

acp_phi_pi = database.add_observable_to_analysis_by_name( analysis=lhcb_paper_2019_002,
            observable_name="ACP(D+ -> phi pi+)", 
            paper_reference="Eq. 6",
            statistical_uncertainty=0.042*units.percent,
            systematic_uncertainty=0.029*units.percent )

acp_ks_k = database.add_observable_to_analysis_by_name( analysis=lhcb_paper_2019_002,
            observable_name="ACP(D+ -> KS K+)", 
            paper_reference="Eq. 5",
            statistical_uncertainty=0.065*units.percent,
            systematic_uncertainty=0.048*units.percent )

acp_ks_pi = database.add_observable_to_analysis_by_name( analysis=lhcb_paper_2019_002,
            observable_name="ACP(Ds+ -> KS pi+)", 
            paper_reference="Eq. 4",
            statistical_uncertainty=0.19*units.percent,
            systematic_uncertainty=0.05*units.percent )

database.add_or_update_analysis( lhcb_paper_2019_002 )
```

## Correlating results from analyses

## Updating an existing analysis

To update an analysis, you first have to get it from the database, then update the parameters, 
and then make a call to `add_or_update_analysis`. For example:

```python
from lbcharmdb import Analysis, CharmCorrelationDatabase, DatabaseSummary, units

database = CharmCorrelationDatabase( input_directory="db" )
database.load()

lhcb_paper_2019_002 = database.get_analysis( "LHCb-PAPER-2019-002" )
lhcb_paper_2019_002.title=r"Search for CP violation in $Ds+ \to KS0\pi+$, $D+ \to KS0K+$ and $D+ \to \phi \pi+$ decays" 
add_or_update_analysis( lhcb_paper_2019_002 ) 
```

Afterwards, you need to [persist the changes to the database](#flush). 

## List all information and observables for an analysis

In case you have to work with an analysis, and want to know which
observables have been registered, you can use `print`:

```python
    lhcb_paper_2022_024 = database.get_analysis("LHCb-PAPER-2022-024")
    print(lhcb_paper_2022_024)
```
which provides:
```
-------- LHCb-PAPER-2022-024 ----
| Title: Measurement of the time-integrated $CP$ asymmetry in $D^0 \to K^- K^+$ decays
| ana: LHCb-ANA-2022-005
| dataset: 2015, 2016, 2017, 2018
| url: https://lhcbproject.web.cern.ch/Publications/p/LHCb-PAPER-2022-024.html
| preprint: arXiv:2209.03179
| journal_reference: None
| tuple_path: None
| observables
|   > [3] 'ACP(D0 -> K- K+)' (paper_reference 'Eq. 1')
| Uncertainties
|   > [ACP(D0 -> K- K+)] 0.00054 Stat.
|   > [ACP(D0 -> K- K+)] 0.00016 Syst.
| Specified Uncertainties: statistical
|   > [ACP(D0 -> K- K+)] 0.00054 Stat ('total')
| Specified Uncertainties: systematic
|   > [ACP(D0 -> K- K+)] 0.00016 Syst ('total')
| obsolete_observables
|   > None
-------------------
```

## Add, or update, a correlation between measurements

It is possible to add correlations to the database between different observables of the same, 
or different analyses. It is possible to correlate the statistical uncertainty of one to that of the
other, but also to correlate the systematic uncretainty of one to the systematic of the other. 

In its most basic form, an example of adding a correlation looks as follows:
```python
lhcb_paper_2022_024 = database.get_analysis("LHCb-PAPER-2022-024")
lhcb_paper_2019_002 = database.get_analysis("LHCb-PAPER-2019-002")
acp_kk = database.get_observable_by_name("ACP(D0 -> K- K+)")
acp_phi_pi = database.get_observable_by_name("ACP(D+ -> phi pi+)")

database.make_and_register_correlation( 
                    analysis_A=lhcb_paper_2022_024, observable_A=acp_kk,
                    analysis_B=lhcb_paper_2019_002, observable_B=acp_phi_pi,
                    correlation_coefficient=0.13 )
```

In the code above, the total *statistical* uncertainties between these two are correlated with 
a coefficient 0.13. In case you wanted to add a correlation between *systematic* uncertainties,
it would look as follows:

```python

database.make_and_register_correlation( 
                    analysis_A=lhcb_paper_2022_024, observable_A=acp_kk,
                    analysis_B=lhcb_paper_2019_002, observable_B=acp_phi_pi,
                    is_statistical_uncertainty_A=False, is_statistical_uncertainty_B=False,
                    correlation_coefficient=0.13 )
```

If you wish to update the correlation coefficient, you can simply call the same function
with the updated coefficient. There will be a message in your console warning you 
that you are updating a pre-existing correlation
> CharmCorrelationDb[54728] INFO Overwriting pre-existing correlation.

To remove a correlation, one simply sets the correlation coefficient
to 0.

## <a name="flush"></a>Finalising the database and create a summary database
The database that is in memory locally can be written back into JSON format by the `flush()` command.
In addition to the full database, a summary needs to be created which is used for the front-end. 
This can be done in one go as follows:

```python
    database.flush( write_summary_to="db/summary" ) #  this writes the "full" database *and* the summary
```

In case you explicitly only want to write out the database, and not create a summary, you can omit
the `write_summary_to` keyword altogether.

## Helpers: Calculating the correlation coefficient between two 
## KPi asymmetries

A regular correction made is that for the detection asymmetry of K- pi+ pairs,
calculated using either a couple of Ds+ or D+ decays. 

To help with the calculation of correlation coefficients, a set of scripts
are made available to calculate the *statistical* correlations. Please follow the instructions
at (here)[this_link].