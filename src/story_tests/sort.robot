*** Settings ***
Resource        resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser

*** Test Cases ***
Add content to the page and sorting works correctly
    Go To    ${HOME_URL}

    # Add inproceedings citation correctly
    Select From List By Value    citation_type    inproceedings
    Input Text    name:name    UniqueNameforInproceedings
    Input Text    author_inproceedings    John Doe
    Input Text    title_inproceedings    My First Inproceedings
    Input Text    booktitle_inproceedings    Conference Proceedings
    Input Text    editor_inproceedings    Bob Marley
    Input Text    year_inproceedings    1993
    Input Text    series_inproceedings    4
    Input Text    volume_inproceedings    10
    Input Text    number_inproceedings    2
    Select From List By Label    month_inproceedings    Mar
    Input Text    pages_inproceedings    10-20
    Input Text    address_inproceedings    Mannerheimintie 10, Helsinki
    Input Text    organization_inproceedings    Helsinki University
    Input Text    publisher_inproceedings    WSOY Press
    Input Text    note_inproceedings    This is probably not very important
    Click Button    Save citation
    Page Should Contain    UniqueNameforInproceedings

    # Add article citation correctly
    Select From List By Value    citation_type    article
    Input Text    name:name    UniqueNameForArticle
    Input Text    name:author    John Doe
    Input Text    name:title    My First Article
    Input Text    name:journal    Science Journal
    Input Text    name:year    1992
    Input Text    name:volume    1
    Input Text    name:number    42
    Input Text    name:pages    10-20
    Select From List By Label    name:month    Jan
    Input Text    name:note    This might be useful
    Click Button    Save citation
    Page Should Contain    UniqueNameForArticle

    # Add book citation correctly
    Select From List By Value    citation_type    book
    Input Text    name:name    UniqueNameforBook
    Input Text    author_book    Joanna Doe
    Input Text    editor_book    Bob Marley
    Input Text    title_book    The Great Book
    Input Text    publisher_book    WSOY Press
    Input Text    year_book    1991
    Input Text    volume_book    10
    Input Text    number_book    2
    Input Text    series_book    4
    Input Text    address_book    Mannerheimintie 10, Helsinki
    Input Text    edition_book    3rd
    Select From List By Label    month_book    Mar
    Input Text    note_book    This is probably important
    Click Button    Save citation
    Page Should Contain    UniqueNameforBook

    # Add mastersthesis citation correctly
    Select From List By Value    citation_type    mastersthesis
    Input Text    name:name    UniqueNameForMastersthesis
    Input Text    author_mastersthesis    Mary Madelaine
    Input Text    title_mastersthesis    My First Mastersthesis
    Input Text    school_mastersthesis    Testing School
    Input Text    type_mastersthesis    Thesis Type
    Input Text    year_mastersthesis    1994
    Select From List By Label    month_mastersthesis    Mar
    Input Text    address_mastersthesis    Times Square 10, New York
    Input Text    note_mastersthesis    This is probably interesting
    Click Button    Save citation
    Page Should Contain    UniqueNameForMastersthesis

    # Add phdthesis citation correctly
    Select From List By Value    citation_type    phdthesis
    Input Text    name:name    UniqueNameForphdthesis
    Input Text    author_phdthesis    Mads Mikkelsen
    Input Text    title_phdthesis    My First Phdthesis
    Input Text    school_phdthesis    Film School
    Input Text    year_phdthesis    1995
    Select From List By Label    month_phdthesis    Jan
    Input Text    keywords_phdthesis    films, acting, drama
    Input Text    address_phdthesis    Hollywood Blvd 20, Los Angeles
    Input Text    note_phdthesis    Not relevant to thesis
    Click Button    Save citation
    Page Should Contain    UniqueNameForphdthesis

    # Add misc citation correctly
    Select From List By Value    citation_type    misc
    Input Text    name:name    UniqueNameFormisc
    Input Text    author_misc    Michael Scott
    Input Text    title_misc    The Best Boss
    Input Text    year_misc    1996
    Select From List By Label    month_misc    Jan
    Input Text    howpublished_misc    fictionally published by Dunder Mifflin
    Input Text    note_misc    really insightful
    Click Button    Save citation
    Page Should Contain    UniqueNameFormisc

    # sort works correctly

    # Test1


    Click Element    css:span.sort-up[data-col="0"]
    Table Row Should Contain  id:sortable  1  UniqueNameForArticle
    Click Element    css:span.sort-down[data-col="0"]
    Table Row Should Contain  id:sortable  1  UniqueNameForphdthesis
    Click Element    css:span.sort-down[data-col="0"]
    Table Row Should Contain  id:sortable  1  UniqueNameforInproceedings

    # Test2
    Click Element    css:span.sort-up[data-col="1"]
    Table Row Should Contain  id:sortable  1  UniqueNameForArticle
    Click Element    css:span.sort-down[data-col="1"]
    Table Row Should Contain  id:sortable  1  UniqueNameForphdthesis
    Click Element    css:span.sort-down[data-col="1"]
    Table Row Should Contain  id:sortable  1  UniqueNameforInproceedings

    # Test3
    Click Element    css:span.sort-up[data-col="2"]
    Table Row Should Contain  id:sortable  1  My First Article
    Click Element    css:span.sort-down[data-col="2"]
    Table Row Should Contain  id:sortable  1  The Great Book
    Click Element    css:span.sort-down[data-col="2"]
    Table Row Should Contain  id:sortable  1  My First Inproceedings

    # Test4     
    Click Element    css:span.sort-up[data-col="3"]
    Table Row Should Contain  id:sortable  1  UniqueNameforBook
    Click Element    css:span.sort-down[data-col="3"]
    Table Row Should Contain  id:sortable  1  UniqueNameFormisc
    Click Element    css:span.sort-down[data-col="3"]
    Table Row Should Contain  id:sortable  1  UniqueNameforInproceedings
