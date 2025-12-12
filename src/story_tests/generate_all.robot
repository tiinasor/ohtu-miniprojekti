*** Settings ***
Library  SeleniumLibrary
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Citations

*** Test Cases ***

Generate .bib file with all citations works correctly   
    # CREATE A FEW CITATIONS FIRST
    Go To  ${HOME_URL}
   
    # CREATE AN ARTICLE CITATION
    Select From List By Value  citation_type  article
    Input Text  name:name  TestArticle
    Input Text  name:author  John Doe
    Input Text  name:title  Test Article Title
    Input Text  name:journal  Science Journal
    Input Text  name:year  2020
    Input Text  name:volume  1
    Click Button  Save citation   
    Page Should Contain  TestArticle

    # CREATE A BOOK CITATION
    Select From List By Value  citation_type  book
    Input Text  name:name  TestBook
    Input Text  author_book  Jane Smith
    Input Text  editor_book  Bob Editor
    Input Text  title_book  Test Book Title
    Input Text  publisher_book  Test Publisher
    Input Text  year_book  2021
    Click Button  Save citation
    Page Should Contain  TestBook

    # CREATE A MISC CITATION
    Select From List By Value  citation_type  misc
    Input Text  name:name  TestMisc
    Input Text  author_misc  Alice Brown
    Input Text  title_misc  Test Misc Title
    Input Text  year_misc  2022
    Click Button  Save citation
    Page Should Contain  TestMisc

    # CLICK THE BUTTON TO GENERATE ALL CITATIONS
    Click Button  Generate .bib (all citations)
   
    # VERIFY THAT THE DOWNLOAD NOTIFICATION APPEARS
    Wait Until Element Is Visible  id:download-notification  timeout=2s
    Element Should Contain  id:download-notification  File downloaded successfully
