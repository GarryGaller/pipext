==================
 pipext
==================

The extension of the functionality of pip
-----------------------------------------

::

    >>python -m pipext --help
    usage: pipext.py [-h] [-s SELECT [SELECT ...]]
                     [--raw RAW | -i INSTALL [INSTALL ...]]
                     [-m MODULES [MODULES ...]] [-e EXCLUDE [EXCLUDE ...]]
                     [--no-deps] [-c COLUMNS [COLUMNS ...] | -C C [C ...]] [--pre]
                     [-f FORMAT [FORMAT ...] | -F NO_FORMAT]
                     [--not-req | --not-req2] [--editable | --user | --local]
                     [--test] [-v VERSION]

    Script      : pipext.py
    Author      : Gary Galler
    Copyright(C): Gary Galler, 2017.  All rights reserved
    Version     : 1.0.0

optional arguments:
  -h, --help            show this help message and exit
  -s SELECT [SELECT ...], --select SELECT [SELECT ...]
                        Module selection type: a|all|full - all installed (by
                        default), o|out|outdated - outdated, u|up|uptodate -
                        uptodated
  --raw RAW             Raw options
  -i INSTALL [INSTALL ...], --install INSTALL [INSTALL ...]
                        List of parameters to update. u,U,upgrade:
                        --upgrade,-U; if,if-needed: --upgrade-strategy only-
                        if-needed; eager: --upgrade-strategy eager; f,force:
                        --force-reinstall; i,ignore: --ignore-installed;
  -c COLUMNS [COLUMNS ...], --columns COLUMNS [COLUMNS ...]
                        List of the number of columns to display in the range
                        0-6. By default, when using --select=all displayed
                        columns 0,1,2,6, when using --select=out - extended
                        version - 0,1,3,4,5,6 - without the Location column.
  -C C [C ...]          List of columns to exclude.
  --pre                 Include pre-release and development versions. By
                        default, pip only finds stable versions.
  -f FORMAT [FORMAT ...], --format FORMAT [FORMAT ...]
                        List of output formatting options: header|head|h - to
                        show headings, separator|sep|s - to separate lines.
  -F NO_FORMAT, --no-format NO_FORMAT
                        Output only a list of names. name - for standard
                        names, egg - names in the format egg, count - output
                        only the number of modules
  --not-req             List packages that are not dependencies of installed
                        packages (original option).
  --not-req2            List of packages that do not have dependencies.
  --editable            List editable projects.
  --user                Only output packages installed in user-site.
  --local               If in a virtualenv that has global access, do not list
                        globally-installed packages.
  --test                Test options
  -v VERSION, --version VERSION
                        The version of the installed module: --version pip

install:
  -m MODULES [MODULES ...], --modules MODULES [MODULES ...]
                        The list of modules to update.
  -e EXCLUDE [EXCLUDE ...], --exclude EXCLUDE [EXCLUDE ...]
                        The list of modules to exclude from the update. Only
                        option -U
  --no-deps             Don't install package dependencies.
-----------------------------------------------------------------------------------
EXAMPLES:  
-----------------------------------------------------------------------------------  
::

    # By default - show all modules
    >>python -m pipext
    ------------------------  ------------------  -------------------------------------------------------------------  ----------------------------------------------------------------------------------------------------
    0 Package                 1 Version           2 Location                                                           6 Depends
    ------------------------  ------------------  -------------------------------------------------------------------  ----------------------------------------------------------------------------------------------------
    Babel                     2.3.4               d:\install\python3\lib\site-packages                                 ['pytz>=0a']
    CVXcanon                  0.1.1               d:\install\python3\lib\site-packages                                 ['numpy', 'scipy']
    CouchDB                   1.1                 d:\install\python3\lib\site-packages
    ...


    # Show modules without dependencies
    >>python -m pipext --not-req2
    -------------------  ------------------  ------------------------------------  ---------
    0 Package            1 Version           2 Location                            6 Depends
    -------------------  ------------------  ------------------------------------  ---------
    CouchDB              1.1                 d:\install\python3\lib\site-packages
    Cython               0.25.2              d:\install\python3\lib\site-packages
    DAWG-Python          0.7.2               d:\install\python3\lib\site-packages
    Hyphenate            1.1.0               d:\install\python3\lib\site-packages
    ...


    # Add columns from the output
    >>python -m pipext --columns 3 4 5
    ------------------------  ------------------  -------------------------------------------------------------------  --------  ------  --------  ----------------------
    0 Package                 1 Version           2 Location                                                           3 Latest  4 Type  5 Python  6 Depends
    ------------------------  ------------------  -------------------------------------------------------------------  --------  ------  --------  ----------------------
    Babel                     2.3.4               d:\install\python3\lib\site-packages                                 None      None    None      ['pytz>=0a']
    CVXcanon                  0.1.1               d:\install\python3\lib\site-packages                                 None      None    None      ['scipy', 'numpy']
    CouchDB                   1.1                 d:\install\python3\lib\site-packages                                 None      None    None
    Cython                    0.25.2              d:\install\python3\lib\site-packages                                 None      None    None
    DAWG-Python               0.7.2               d:\install\python3\lib\site-packages                                 None      None    None
    ...

    # Remove columns from the output
    >>python -m pipext -C 2 6
    ------------------------  ------------------
    0 Package                 1 Version
    ------------------------  ------------------
    Babel                     2.3.4
    CVXcanon                  0.1.1
    CouchDB                   1.1
    Cython                    0.25.2
    DAWG-Python               0.7.2
    ...


    # Select outdated modules
    >>python -m pipext --select=out
    ----------------  ----------  -----------  ------  --------  ---------------------------------------------------------------------
    0 Package         1 Version   3 Latest     4 Type  5 Python  6 Depends
    ----------------  ----------  -----------  ------  --------  ---------------------------------------------------------------------
    PyBuilder         0.11.9      0.11.10      sdist   3.5       ['pip>=7.0', 'tblib', 'wheel']
    PyQt5             5.8.1       5.8.1.1      wheel   None      ['sip<4.20']
    Werkzeug          0.12        0.12.1       wheel   None
    aiohttp           1.3.3       1.3.5        sdist   None      ['multidict>=2.1.4', 'chardet', 'yarl<0.10', 'async-timeout>=1.1.0']
    asn1crypto        0.21.1      0.22.0       wheel   None
    ...


    # Show outdated modules with regard to prerelease versions
    >>python -m pipext --select=out --pre
    ----------------  -----------  -------------------------  ------  --------  ------------------------------------------------------------------------
    0 Package         1 Version    3 Latest                   4 Type  5 Python  6 Depends
    ----------------  -----------  -------------------------  ------  --------  ------------------------------------------------------------------------
    PyBuilder         0.11.9       0.11.11.dev20170316102956  sdist   3.5       ['pip>=7.0', 'tblib', 'wheel']
    PyQt5             5.8.1        5.8.1.1                    wheel   None      ['sip<4.20']
    Werkzeug          0.12         0.12.1                     wheel   None
    aiohttp           1.3.3        2.0.0rc1                   sdist   None      ['multidict>=2.1.4', 'yarl>=0.9.8', 'async-timeout>=1.1.0', 'chardet']
    ...

    # Select uptodated modules
    >>python -m pipext --select=uptodate
    ------------------------  ------------------  ------------------  ------  --------
    0 Package                 1 Version           3 Latest            4 Type  5 Python
    ------------------------  ------------------  ------------------  ------  --------
    Babel                     2.3.4               2.3.4               wheel   None
    CVXcanon                  0.1.1               0.1.1               sdist   None
    CouchDB                   1.1                 1.1                 wheel   None
    Cython                    0.25.2              0.25.2              wheel   None
    DAWG-Python               0.7.2               0.7.2               wheel   None
    Delorean                  0.6.0               0.6.0               sdist   3.5 
    ...

    # Display the names of the modules list in egg format
    >>python -m pipext -F=egg
    Babel-2.3.4-py3.5
    CVXcanon-0.1.1-py3.5
    CouchDB-1.1-py3.5
    Cython-0.25.2-py3.5
    DAWG_Python-0.7.2-py3.5
    Delorean-0.6.0-py3.5
    Hyphenate-1.1.0-py3.5
    ...

    # Count the number of modules and show
    >>python -m pipext -F=count
    234

    >>python -m pipext -v pipext
    1.0.0

    # Matches:pip install --upgrade-strategy only-if-needed
    >>python -m pipext -s=o -i if

    # Matches:pip install --upgrade --no-deps
    >>python -m pipext -s=o -i u --no-deps

    # Matches:pip install --force-reinstall --no-deps
    >>python -m pipext -s=o -i f --no-deps

    # Matches:pip install --ignore-installed
    >>python -m pipext -s=o -i i

    # Using raw options - you can pass any options pip install --all_other_options
    >>python -m pipext --raw="--upgrade --no-deps" -m some_module
