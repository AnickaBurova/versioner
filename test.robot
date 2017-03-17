*** Settings ***
Library         Process


*** Keywords ***
Python exec
    [Arguments]     ${python}   ${input}
    ${result} =     Run Process     ${python} versioner.py ${input}   shell=True
    [return]    ${result}

Run success
    [Arguments]     ${python}   ${input}
    ${result} =     Python exec    ${python}      ${input}
    Should be equal     ${0}    ${result.rc}


Run not success
    [Arguments]     ${python}   ${input}
    ${result} =     Python exec    ${python}      ${input}
    Should not be equal     ${0}    ${result.rc}

*** Test Cases ***
Check version python
    Run success         python2     --version
    Run success         python3     --version


Check incorrect language
    Run not success         python2     -l wrong
    Run not success         python3     -l wrong


