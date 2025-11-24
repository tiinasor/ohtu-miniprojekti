*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser


*** Test Cases ***
Add article citation correctly
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  article
    Input Text  name  jhojkjsadfj
    Input Text  author_article  kifgj
    Input Text  title_article  hfhhhdf
    Input Text  journal_article  tasd
    Input Text  year_article  1996
    Input Text  volume_article  100
    Input Text  number_article  500
    Input Text  pages_article  500
    Click Button  Save citation
    Page Should Contain  jhojkjsadfj