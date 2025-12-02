*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser 
Suite Teardown   Close Browser
Test Setup       Reset Citations


*** Test Cases ***
Add content to the page and search works correctly
    #Robot test can find search bar
    Go To  ${HOME_URL}
    Input Text  css:input[placeholder="Search citations…"]  thisissearchbaryes

    #Add article citation correctly
    
    Select From List By Value  citation_type  article
    Input Text  name:name  UniqueNameForArticle
    Input Text  name:author  John Doe
    Input Text  name:title  My First Article
    Input Text  name:journal  Science Journal
    Input Text  name:year  1996
    Input Text  name:volume  1
    Input Text  name:number  42
    Input Text  name:pages  10-20
    Input Text  name:month  January
    Input Text  name:note  This might be useful
    Click Button  Save citation    
    Page Should Contain  UniqueNameForArticle


    #Add book citation correctly
    
    Select From List By Value  citation_type  book
    Input Text  name:name  UniqueNameforBook
    Input Text  author_book  Joanna Doe
    Input Text  editor_book  Bob Marley
    Input Text  title_book  The Great Book
    Input Text  publisher_book  WSOY Press
    Input Text  year_book  1996
    Input Text  volume_book  10
    Input Text  number_book  2
    Input Text  series_book  4
    Input Text  address_book  Mannerheimintie 10, Helsinki
    Input Text  edition_book  3rd
    Input Text  month_book  March
    Input Text  note_book  This is probably important
    Click Button  Save citation
    Page Should Contain  UniqueNameforBook


    #Add inproceedings citation correctly
    
    Select From List By Value  citation_type  inproceedings
    Input Text  name:name  UniqueNameforInproceedings
    Input Text  author_inproceedings  John Doe
    Input Text  title_inproceedings   My First Inproceedings
    Input Text  booktitle_inproceedings   Conference Proceedings
    Input Text  editor_inproceedings   Bob Marley
    Input Text  year_inproceedings   1996
    Input Text  series_inproceedings  4
    Input Text  volume_inproceedings  10
    Input Text  number_inproceedings  2
    Input Text  month_inproceedings  March
    Input Text  pages_inproceedings  10-20
    Input Text  address_inproceedings  Mannerheimintie 10, Helsinki
    Input Text  organization_inproceedings  Helsinki University
    Input Text  publisher_inproceedings  WSOY Press
    Input Text  note_inproceedings  This is probably not very important
    Click Button  Save citation
    Page Should Contain  UniqueNameforInproceedings

    #Add mastersthesis citation correctly
    
    Select From List By Value  citation_type  mastersthesis
    Input Text  name:name  UniqueNameForMastersthesis
    Input Text  author_mastersthesis  Mary Madelaine
    Input Text  title_mastersthesis  My First Mastersthesis
    Input Text  school_mastersthesis  Testing School
    Input Text  type_mastersthesis  Thesis Type
    Input Text  year_mastersthesis  1996
    Input Text  month_mastersthesis  March
    Input Text  address_mastersthesis  Times Square 10, New York
    Input Text  note_mastersthesis  This is probably interesting
    Click Button  Save citation
    Page Should Contain  UniqueNameForMastersthesis

    #Add phdthesis citation correctly
    
    Select From List By Value  citation_type  phdthesis
    Input Text  name:name  UniqueNameForphdthesis
    Input Text  author_phdthesis  Mads Mikkelsen
    Input Text  title_phdthesis  My First Phdthesis
    Input Text  school_phdthesis  Film School
    Input Text  year_phdthesis  1996
    Input Text  month_phdthesis  January
    Input Text  keywords_phdthesis  films, acting, drama
    Input Text  address_phdthesis  Hollywood Blvd 20, Los Angeles
    Input Text  note_phdthesis  Not relevant to thesis
    Click Button  Save citation
    Page Should Contain  UniqueNameForphdthesis


    #Add misc citation correctly
    
    Select From List By Value  citation_type  misc

    Input Text  name:name  UniqueNameFormisc
    Input Text  author_misc  Michael Scott
    Input Text  title_misc  The Best Boss
    Input Text  year_misc  1996
    Input Text  month_misc  January
    Input Text  howpublished_misc  fictionally published by Dunder Mifflin
    Input Text  note_misc  really insightful
    Click Button  Save citation
    Page Should Contain  UniqueNameFormisc

    #Search works correctly
    
    #Test1
    Input Text  css:input[placeholder="Search citations…"]  Times Square 10
    Page Should Contain  My First Mastersthesis
    Citation list contains only one row

    #Test2
    Input Text  css:input[placeholder="Search citations…"]  Los Angeles
    Page Should Contain  UniqueNameForphdthesis
    Citation list contains only one row

    #Test3
    Input Text  css:input[placeholder="Search citations…"]  Los Angeles
    Page Should Contain  UniqueNameForphdthesis
    Citation list contains only one row

    #Test4
    Input Text  css:input[placeholder="Search citations…"]  WSOY Press
    Page Should Contain  1996
    Page Should Contain  The Great Book
    Page Should Contain  UniqueNameforInproceedings
    Page Should Contain  UniqueNameforBook
    Citation list contains two rows

    #Test5
    Input Text  css:input[placeholder="Search citations…"]  really
    Page Should Contain  UniqueNameFormisc
    Citation list contains only one row

    #Test6
    Input Text  css:input[placeholder="Search citations…"]  ${EMPTY}
    Page Should Contain  UniqueNameForArticle
    Page Should Contain  UniqueNameforBook
    Page Should Contain  UniqueNameforInproceedings
    Page Should Contain  UniqueNameForMastersthesis
    Page Should Contain  UniqueNameForphdthesis
    Page Should Contain  UniqueNameFormisc

    #Test7
    Input Text  css:input[placeholder="Search citations…"]  10-20
    Page Should Contain  UniqueNameForArticle
    Page Should Contain  UniqueNameforInproceedings

    #Test8
    Input Text  css:input[placeholder="Search citations…"]  January
    Page Should Contain  UniqueNameForArticle
    Page Should Contain  UniqueNameForphdthesis
    Page Should Contain  UniqueNameFormisc
    Reset Citations
