*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser


*** Test Cases ***
Remove citation correctly
    Go To  ${HOME_URL}
    
    #Finds the remove button which has the unique test name in its row
    Click Button  xpath=//tr[td[normalize-space()="jhojkjsadfj"]]//button[text()="Remove"]


    Page Should Contain  Citation removal
    Click Button  Remove
    Page Should Contain  Create citation
    Page Should Not Contain  jhojkjsadfj


