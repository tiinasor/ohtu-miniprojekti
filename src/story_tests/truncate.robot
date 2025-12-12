*** Settings ***
Library  SeleniumLibrary
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Citations

*** Test Cases ***

Long citation titles are truncated in table
    # Create citation with very long title
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  article
    Input Text  name:name  LongTitleTest
    Input Text  name:author  Test Author
    Input Text  name:title  This is an extremely long title that should definitely be truncated to a single line in the table view to maintain readability and consistent layout
    Input Text  name:journal  Test Journal
    Input Text  name:year  2024
    Input Text  name:volume  1
    Click Button  Save citation
   
    # Verify the title cell has the truncation class
    ${title_cell}=  Get WebElement  xpath=//td[@class='col-title']//span[@class='cell-clip']
    Element Should Be Visible  ${title_cell}
   
    # Verify CSS property for text truncation
    ${overflow}=  Execute JavaScript  return window.getComputedStyle(document.querySelector('.cell-clip')).textOverflow
    Should Be Equal  ${overflow}  ellipsis
