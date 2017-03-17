*** Settings ***
Library         Process


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

*** Test Cases ***
Check version python
    Success         python2     --version
    Success         python3     --version


Check incorrect language
    Failure         python2     -l wrong
    Failure         python3     -l wrong


