*** Settings ***
Library         OperatingSystem
Library         Process

Test Setup      Touch               ${test_file}
Test Teardown   Remove File         ${test_file}

*** Variables ***
${test_file} =  ${TEMPDIR}${/}test.py


*** Keywords ***
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
    Failure     ${python}       -l wrong ${test_file}
    Success     ${python}       -l cpp ${test_file}
    Success     ${python}       -l python ${test_file}
    Success     ${python}       -l haskell ${test_file}
    Success     ${python}       -l cPp ${test_file}
    Success     ${python}       -l pYthon ${test_file}
    Success     ${python}       -l hasKell ${test_file}


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
