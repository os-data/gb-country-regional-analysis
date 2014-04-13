The HM Treasury Country and Regional Analysis (CRA) dataset shows where in the
country benefit has been had from the spending of each government department.

The CRA is a data set produced annually by the HM Treasury and is part of their
Public Expenditure and Statistical Analysis (PESA). The data is produced by
each government department and collected by the Treasury in February. Each
government department has to determine which parts of the country have
benefited from spending in its different programs (Program Object Groups --
POGs). Each department defines their own POGs and the Treasury require that the
departments fit their POGS under COFOG functions.

Public Expenditure Statistical Analyses (PESA) is published by HM Treasury,
annually soon after the Budget. It is public spending by combinations of:

* Government function (defined by the UN Classification Of the Functions Of
  Government (COFOG) for 2007 onwards)
* Government department
* Area of the country (defined by the NUTS12 classification system)
* Time (estimates of future spending and reviews of past spending) 
* Forms of aggregation (this includes dividing spending between DEL and AME,
  resource (near-cash and non-cash) and capital, and administration and
  programme budgets).

# cratools: tools to extract and load the UK's Country Regional Analysis into OpenSpending

## Usage

To use this package you will need to have [Python](http://python.org),
[pip](http://www.pip-installer.org) and [virtualenv](http://virtualenv.org).
The remaining dependencies will then be installed by the following sequence of
commands.

    virtualenv pyenv
    source pyenv/bin/activate
    pip install -e .

You can then run the conversion from Excel files to flat CSV by running:

    cratools csvexport

This will generate an output csv file at:

    data/cra.csv

This command may complain that you don't have all the data files you need. In
particular, the ~5MB CRA data files are not included in this repository, and
you will need to download them as per the instructions in the error message.

## Unmatched rows

CRA Table 9 has regional breakdown, while table 10 has COFOG2 codes. `cratools csvexport`
combines them and deals with inconsistencies. If there are any rows that can't
be matched, they'll be dumped into files called `unmatched_table9.csv` and
`unmatched_table10.csv`. Very often these will be small typos that you can then
go and fix in the source files by hand before rerunning `cratools csvexport`.

## Data warnings

This section is largely transcribed from e-mail: <http://lists.okfn.org/pipermail/wdmmg-discuss/2010-April/000165.html>

The "function" and "subfunction" columns of the published CRA data contain broken
data, and that we have been using a mapping designed by William Waites to fix
them. Dave Boyce has also produced such a mapping, and we thought it would be a
good idea to cross-check them.

It was! I have been able to fix several errors and omissions. However, there
are still some hard ones that I would like some help with. There is some
partially helpful advice from HM Treasury here:

<http://epp.eurostat.ec.europa.eu/cache/ITY_OFFPUB/KS-RA-07-022/EN/KS-RA-07-022-EN.PDF>

Here are the noteworthy ones:

  - Anything with a subfunction of "LA data subfunction" is a problem. I don't
    know what this means. This occurs at least once for every function.  I have
    mapped these to relatively coarse COFOG codes: 1, 2, 3, 4.1, 4.2, 5, 6, 7,
    8, 9 and 10.

  - Function "EU entries", subfunction "EC receipts" is left
    "unclassified" by HMT. I've mapped this to 1.8 (Transfers of a general
    character between different levels of government).

  - Function "EU entries", subfunction "GNI-based contribution (net of
    abatement and collection costs)" is also left unmapped. I have mapped it to
    1.2 (Foreign economic aid).

  - [APS updating for 2010] Rows with function "EU entries", subfunction
    also "EU entries": I've attributed to 1.8 for now, but will ask others
    to review.

  - Many of the sub-sub-functions of COFOG function 1 (General public services)
    all say "of which: public and common services". This is presumably a
    cut-and-paste error.

  - Function "3. Public order and safety", subfunction "of which: immigration
    and citizenship" is a tricky one. HMT recommends mapping it to 3.1.2.

  - Function "of which: agriculture, fisheries and forestry", sub-function "of
    which: other agriculture, food and fisheries policy" maps to two COFOG
    codes: 4.2.1 and 4.2.3. I have mapped it all to 4.2.3, on the feeble
    grounds that nothing else is mapped there.

  - We previous little level-3 data for code 4 (economic affairs) except for
    4.5 (transport). Even there, nothing maps onto 4.5.2 (water transport) or
    4.5.4 (air transport).

  - Function "of which: transport", subfunction "of which: local public
    transport" is mapped to 4.5.1 (road transport).

  - Many of the sub-sub-functions of COFOG function 4 (economic affairs) all
    say "of which: enterprise and economic development". This is presumably a
    cut-and-paste error.

  - Function "7. Health" and subfunction "Central and other health services"
    maps to both 7.4 and 7.6. I have mapped it all to 7.4.

  - Function "7. Health", subfunction "Medical services" maps to 7.1, 7.2 and
    7.3. I have mapped it all to 7.1.

  - Code 10 means "Social protection", and inside it are codes 10.7 "Social
    exclusion" and 10.9 "Social protection". Therefore, where the published
    data says function is "Social protection" and subfunction is "blah, blah
    (social exclusion)" I assume I should use 10.7. However, when both function
    and subfunction say "Social protection" is it valid to use 10.9?
