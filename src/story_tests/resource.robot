*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${SERVER}     localhost:5001
${DELAY}      0.25 seconds
${HOME_URL}   http://${SERVER}
${RESET_URL}  http://${SERVER}/reset_db
${BROWSER}    chrome
${HEADLESS}   false

*** Keywords ***
Open And Configure Browser
    IF  $BROWSER == 'chrome'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys
        Call Method  ${options}  add_argument  --incognito
    ELSE IF  $BROWSER == 'firefox'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].FirefoxOptions()  sys
        Call Method  ${options}  add_argument  --private-window
    END
    IF  $HEADLESS == 'true'
        Set Selenium Speed  0.01 seconds
        Call Method  ${options}  add_argument  --headless
    ELSE
        Set Selenium Speed  ${DELAY}
    END
    Open Browser  browser=${BROWSER}  options=${options}

Reset Citations
    Go To  ${RESET_URL}


Citation list contains only one row
    ${visible_count}=    Execute JavaScript    return document.querySelectorAll('tbody tr.citation:not([style*="display: none"])').length;
    Should Be Equal As Integers    ${visible_count}    1

Citation list contains two rows
    ${visible_count}=    Execute JavaScript    return document.querySelectorAll('tbody tr.citation:not([style*="display: none"])').length;
    Should Be Equal As Integers    ${visible_count}    2