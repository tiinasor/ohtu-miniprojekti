*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Citations


*** Test Cases ***
View article citation information on info page
    Go To  ${HOME_URL}
    # CREATE CITATION FIRST
    Select From List By Value  citation_type  article
    Input Text  name:name     UniqueArticle
    Input Text  name:author   Test Author A
    Input Text  name:title    My First Article
    Input Text  name:journal  Science Journal
    Input Text  name:year     1996
    Input Text  name:volume   1
    Input Text  name:number   42
    Input Text  name:pages    10-20
    Select From List By Label  name:month  Jan
    Input Text  name:note     This might be useful
    Click Button  Save citation

    # NOW VIEW INFO PAGE
    Click Link  UniqueArticle
    Page Should Contain  UniqueArticle
    Page Should Contain  Test Author A
    Page Should Contain  My First Article
    Page Should Contain  Science Journal
    Page Should Contain  1996
    Page Should Contain  42
    Page Should Contain  10-20
    Page Should Contain  Jan
    Page Should Contain  This might be useful


Navigate back to list from article info page
    Go To  ${HOME_URL}
    # CREATE CITATION FIRST
    Select From List By Value  citation_type  article
    Input Text  name:name     TestArticle
    Input Text  name:author   Test Author B
    Input Text  name:title    Test Article Title
    Input Text  name:journal  Test Journal
    Input Text  name:year     2024
    Input Text  name:volume   5
    Click Button  Save citation

    # GO TO INFO PAGE
    Click Link  TestArticle
    Page Should Contain  Test Author B

    # NAVIGATE BACK
    Click Button  Back to List
    Page Should Contain  Citations
    Page Should Contain  TestArticle
    Page Should Contain  All saved entries


View book citation information on info page
    Go To    ${HOME_URL}
    # CREATE CITATION FIRST
    Select From List By Value    citation_type    book
    Input Text    name:name    UniqueBook
    Input Text    author_book    Test Author C
    Input Text    editor_book    Test Editor A
    Input Text    title_book    The Great Book
    Input Text    publisher_book    WSOY Press
    Input Text    year_book    1996
    Input Text    volume_book    10
    Input Text    series_book    Book Series
    Input Text    address_book    Helsinki
    Input Text    edition_book    3rd
    Select From List By Label    month_book    Mar
    Input Text    note_book    Important book
    Click Button    Save citation

    # NOW VIEW INFO PAGE
    Click Link    UniqueBook
    Page Should Contain    UniqueBook
    Page Should Contain    Test Author C
    Page Should Contain    Test Editor A
    Page Should Contain    The Great Book
    Page Should Contain    WSOY Press
    Page Should Contain    1996
    Page Should Contain    Helsinki
    Page Should Contain    3rd
    Page Should Contain    Mar
    Page Should Contain    Important book


Navigate back to list from book info page
    Go To    ${HOME_URL}
    # CREATE CITATION FIRST
    Select From List By Value    citation_type    book
    Input Text    name:name    TestBook
    Input Text    author_book    Test Author
    Input Text    title_book    Test Book Title
    Input Text    publisher_book    Test Publisher
    Input Text    year_book    2023
    Click Button    Save citation

    # GO TO INFO PAGE
    Click Link    TestBook
    Page Should Contain    Test Author

    # NAVIGATE BACK
    Click Button    Back to List
    Page Should Contain    Citations
    Page Should Contain    TestBook


View mastersthesis citation information on info page
    Go To  ${HOME_URL}
    # CREATE CITATION FIRST
    Select From List By Value  citation_type  mastersthesis
    Input Text  name:name              UniqueThesis
    Input Text  author_mastersthesis   Test Author D
    Input Text  title_mastersthesis    My Masters Thesis
    Input Text  school_mastersthesis   Testing School
    Input Text  type_mastersthesis     Masters Thesis
    Input Text  year_mastersthesis     1996
    Select From List By Label  month_mastersthesis  Mar
    Input Text  address_mastersthesis  New York
    Input Text  note_mastersthesis     Interesting thesis
    Click Button  Save citation

    # NOW VIEW INFO PAGE
    Click Link  UniqueThesis
    Page Should Contain  UniqueThesis
    Page Should Contain  Test Author D
    Page Should Contain  My Masters Thesis
    Page Should Contain  Testing School
    Page Should Contain  1996
    Page Should Contain  Mar
    Page Should Contain  New York
    Page Should Contain  Interesting thesis


Navigate back to list from mastersthesis info page
    Go To  ${HOME_URL}
    # CREATE CITATION FIRST
    Select From List By Value  citation_type  mastersthesis
    Input Text  name:name              TestThesis
    Input Text  author_mastersthesis   Test Student
    Input Text  title_mastersthesis    Test Thesis
    Input Text  school_mastersthesis   Test University
    Input Text  year_mastersthesis     2022
    Click Button  Save citation

    # GO TO INFO PAGE
    Click Link  TestThesis
    Page Should Contain  Test Student

    # NAVIGATE BACK
    Click Button  Back to List
    Page Should Contain  Citations
    Page Should Contain  TestThesis
