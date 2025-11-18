*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser


*** Test Cases ***
Add and remove citation correctly
    Go To  ${HOME_URL}
    Input Text  name  jhojkjsadfj
    Input Text  author  kifgj
    Input Text  title  hfhhhdf
    Input Text  journal  tasd
    Input Text  year  1996
    Input Text  volume  100
    Input Text  number  500
    Input Text  pages  500
    Click Button  Create
    Page Should Contain  jhojkjsadfj
    
    #Finds the remove button which has the unique test name in its row
    Click Button  xpath=//tr[td[normalize-space()="jhojkjsadfj"]]//button[text()="Remove"]


    Page Should Contain  Citation removal
    Click Button  Remove
    Page Should Contain  Citations engine
    Page Should Not Contain  jhojkjsadfj


