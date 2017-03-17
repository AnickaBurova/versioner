*** Settings ***
Library         OperatingSystem
Library         Process

Test Setup      Create test files
Test Teardown   Remove test files

*** Variables ***
${python_file} =  ${TEMPDIR}${/}test.py
${cpp_file} =  ${TEMPDIR}${/}test.cpp
${haskell_file} =  ${TEMPDIR}${/}test.hs
${test_version} =   0.1.2

'
*** Keywords ***
Create test files
    Copy file           python_test.py          ${python_file}
    Copy file           haskell_test.cabal          ${haskell_file}
    Copy file           cpp_test.cpp          ${cpp_file}

Remove test files
    Remove file         ${python_file}
    Remove file         ${cpp_file}
    Remove file         ${haskell_file}

Python exec
    [Arguments]     ${python}   ${input}
    ${result} =     Run Process     ${python} versioner.py ${input}   shell=True
    [return]    ${result}

Success
    [Arguments]     ${python}   ${input}
    ${result} =     Python exec    ${python}      ${input}
    Should be equal     ${0}    ${result.rc}


Failure
    [Arguments]     ${python}   ${input}
    ${result} =     Python exec    ${python}      ${input}
    Should not be equal     ${0}    ${result.rc}

Choose language
    [Arguments]     ${python}
    Failure     ${python}       -l wrong ${python_file}
    Success     ${python}       -l cpp ${cpp_file}
    Success     ${python}       -l python ${python_file}
    Success     ${python}       -l haskell ${haskell_file}
    Success     ${python}       -l cPp ${cpp_file}
    Success     ${python}       -l pYthon ${python_file}
    Success     ${python}       -l hasKell ${haskell_file}


Set input file
    [Arguments]     ${python}
    Log         No argument
    Failure     ${python}
    Log         Not existing file
    Failure     ${python}   some_file.none
    ${wrong_file}   ${TEMPDIR}${/}wrong.file
    Touch           ${wrong_file}
    Failure     ${python}   ${wrong_file}
    Remove file     ${wrong_file}



*** Test Cases ***
Check version python
    Success         python2     --version
    Success         python3     --version


Choose language
    Choose language     python2
    Choose language     python3
