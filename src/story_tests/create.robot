*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser


*** Test Cases ***
Add citation correctly
    Go To  ${HOME_URL}
    Input Text  name  jhojkjsadfj
    Input Text  author  kifgj
    Input Text  title  hfhhhdf
    Input Text  journal  tasd
    Input Text  year  1996
    Input Text  volume  100
    Input Text  number  500
    Input Text  pages  500
    Click Button  Save citation
    Page Should Contain  jhojkjsadfj