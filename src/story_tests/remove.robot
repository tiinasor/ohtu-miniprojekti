*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Citations

#This is a copy-paste of creation robot tests but it also checks that canceling the removal works

*** Test Cases ***
Removal of article citation works correctly if confirmation pop-up is accepted
    Go To  ${HOME_URL}
    # CREATE CITATION FIRST
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

    # NOW REMOVE IT
    Click Element  xpath=//table//tbody//tr[td[normalize-space(.)="My First Article"]]
    Click Button   id=delete_selected
    # NOW CONFIRM POP-UP
    Handle Alert   ACCEPT
    Page Should Not Contain  UniqueNameForArticle

Removal of article citation works correctly if confirmation pop-up is dismissed
    Go To  ${HOME_URL}
    # CREATE CITATION FIRST
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
    # NOW REMOVE IT
    Click Element  xpath=//table//tbody//tr[td[normalize-space(.)="My First Article"]]
    Click Button   id=delete_selected
    # NOW CANCEL POP-UP
    Handle Alert   DISMISS
    Page Should Contain  UniqueNameForArticle

Removal of book citation works correctly if confirmation pop-up is accepted
    Go To  ${HOME_URL}
    # CREATE CITATION FIRST
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
    Page Should Contain  The Great Book

    # NOW REMOVE IT
    Click Element  xpath=//table//tbody//tr[td[normalize-space(.)="The Great Book"]]
    Click Button   id=delete_selected
    # NOW CONFIRM POP-UP
    Handle Alert   ACCEPT
    Page Should Not Contain  The Great Book

Removal of book citation works correctly if confirmation pop-up is dismissed
    Go To  ${HOME_URL}
    # CREATE CITATION FIRST
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
    Page Should Contain  The Great Book

    # NOW REMOVE IT
    Click Element  xpath=//table//tbody//tr[td[normalize-space(.)="The Great Book"]]
    Click Button   id=delete_selected
    # NOW CANCEL POP-UP
    Handle Alert   DISMISS
    Page Should Contain  The Great Book



# Removal of inproceedings citation works correctly if confirmation pop-up is accepted
    # Go To  ${HOME_URL}
    # CREATE CITATION FIRST
    # Select From List By Value  citation_type  inproceedings
    # Input Text  name:name  UniqueNameforInproceedings
    # Input Text  author_inproceedings  John Doe
    # Input Text  title_inproceedings   My First Inproceedings
    # Input Text  booktitle_inproceedings   Conference Proceedings
    # Input Text  editor_inproceedings   Bob Marley
    # Input Text  year_inproceedings   1996
    # Input Text  series_inproceedings  4
    # Input Text  volume_inproceedings  10
    # Input Text  number_inproceedings  2
    # Input Text  month_inproceedings  March
    # Input Text  pages_inproceedings  10-20
    # Input Text  address_inproceedings  Mannerheimintie 10, Helsinki
    # Input Text  organization_inproceedings  Helsinki University
    # Input Text  publisher_inproceedings  WSOY Press
    # Input Text  note_inproceedings  This is probably not very important
    # Click Button  Save citation
    #Page Should Contain  UniqueNameforInproceedings

    # NOW REMOVE IT 
    # Click Element  xpath=//table//tbody//tr[td[normalize-space(.)="My First Inproceedings"]]
    # Click Button   id=delete_selected
    # NOW CONFIRM POP-UP
    # Handle Alert   ACCEPT
    #Page Should Not Contain  UniqueNameforInproceedings

# Removal of inproceedings citation works correctly if confirmation pop-up is dismissed
    # Go To  ${HOME_URL}
    # CREATE CITATION FIRST
    # Select From List By Value  citation_type  inproceedings
    # Input Text  name:name  UniqueNameforInproceedings
    # Input Text  author_inproceedings  John Doe
    # Input Text  title_inproceedings   My First Inproceedings
    # Input Text  booktitle_inproceedings   Conference Proceedings
    # Input Text  editor_inproceedings   Bob Marley
    # Input Text  year_inproceedings   1996
    # Input Text  series_inproceedings  4
    # Input Text  volume_inproceedings  10
    # Input Text  number_inproceedings  2
    # Input Text  month_inproceedings  March
    # Input Text  pages_inproceedings  10-20
    # Input Text  address_inproceedings  Mannerheimintie 10, Helsinki
    # Input Text  organization_inproceedings  Helsinki University
    # Input Text  publisher_inproceedings  WSOY Press
    # Input Text  note_inproceedings  This is probably not very important
    # Click Button  Save citation
    # Page Should Contain  UniqueNameforInproceedings

    # NOW REMOVE IT
    # Click Element  xpath=//table//tbody//tr[td[normalize-space(.)="My First Inproceedings"]]
    # Click Button   id=delete_selected
    # NOW CANCEL POP-UP
    # Handle Alert   DISMISS
    # Page Should Contain  UniqueNameforInproceedings


Removal of mastersthesis citation works correctly if confirmation pop-up is accepted
    #Go To  ${HOME_URL}
    # CREATE CITATION FIRST
    #Select From List By Value  citation_type  mastersthesis
    # Input Text  name:name  UniqueNameForMastersthesis
    # Input Text  author_mastersthesis  Mary Madelaine
    # Input Text  title_mastersthesis  My First Mastersthesis
    # Input Text  school_mastersthesis  Testing School
    # Input Text  type_mastersthesis  Thesis Type
    # Input Text  year_mastersthesis  1996
    # Input Text  month_mastersthesis  March
    # Input Text  address_mastersthesis  Times Square 10, New York
    # Input Text  note_mastersthesis  This is probably interesting
    # Click Button  Save citation
    # Page Should Contain  UniqueNameForMastersthesis

     # NOW REMOVE IT
    # Click Element  xpath=//table//tbody//tr[td[normalize-space(.)="My First Mastersthesis"]]
    # Click Button   id=delete_selected
    # NOW ACCEPT POP-UP
    # Handle Alert   ACCEPT
    #Page Should Not Contain  UniqueNameForMastersthesis

# Removal of mastersthesis citation works correctly if confirmation pop-up is dismissed
    # Go To  ${HOME_URL}
    # CREATE CITATION FIRST
    # Select From List By Value  citation_type  mastersthesis
    # Input Text  name:name  UniqueNameForMastersthesis
    # Input Text  author_mastersthesis  Mary Madelaine
    # Input Text  title_mastersthesis  My First Mastersthesis
    # Input Text  school_mastersthesis  Testing School
    # Input Text  type_mastersthesis  Thesis Type
    # Input Text  year_mastersthesis  1996
    # Input Text  month_mastersthesis  March
    # Input Text  address_mastersthesis  Times Square 10, New York
    # Input Text  note_mastersthesis  This is probably interesting
    # Click Button  Save citation
    #Page Should Contain  UniqueNameForMastersthesis

    # NOW REMOVE IT
    # Click Element  xpath=//table//tbody//tr[td[normalize-space(.)="My First Mastersthesis"]]
    # Click Button   id=delete_selected
    # NOW DISMISS POP-UP
    # Handle Alert   DISMISS
    # Page Should Contain  UniqueNameForMastersthesis

# Removal of phdthesis citation works correctly if confirmation pop-up is accepted
    Go To  ${HOME_URL}
    # CREATE CITATION FIRST
    # Select From List By Value  citation_type  phdthesis
    # Input Text  name:name  UniqueNameForphdthesis
    # Input Text  author_phdthesis  Mads Mikkelsen
    # Input Text  title_phdthesis  My First Phdthesis
    # Input Text  school_phdthesis  Film School
    # Input Text  year_phdthesis  1996
    # Input Text  month_phdthesis  January
    # Input Text  keywords_phdthesis  films, acting, drama
    # Input Text  address_phdthesis  Hollywood Blvd 20, Los Angeles
    # Input Text  note_phdthesis  Not relevant to thesis
    # Click Button  Save citation
    # Page Should Contain  UniqueNameForphdthesis

    # NOW REMOVE IT
    # Click Element  xpath=//table//tbody//tr[td[normalize-space(.)="My First Phdthesis"]]
    # Click Button   id=delete_selected
    # NOW ACCEPT POP-UP
    # Handle Alert   ACCEPT
    # Page Should Not Contain  UniqueNameForphdthesis

# Removal of phdthesis citation works correctly if confirmation pop-up is dismissed
    Go To  ${HOME_URL}
    # CREATE CITATION FIRST
    Select From List By Value  citation_type  phdthesis
    # Input Text  name:name  UniqueNameForphdthesis
    # Input Text  author_phdthesis  Mads Mikkelsen
    # Input Text  title_phdthesis  My First Phdthesis
    # Input Text  school_phdthesis  Film School
    # Input Text  year_phdthesis  1996
    # Input Text  month_phdthesis  January
    # Input Text  keywords_phdthesis  films, acting, drama
    # Input Text  address_phdthesis  Hollywood Blvd 20, Los Angeles
    # Input Text  note_phdthesis  Not relevant to thesis
    # Click Button  Save citation
    # Page Should Contain  UniqueNameForphdthesis

    # NOW REMOVE IT
    # Click Element  xpath=//table//tbody//tr[td[normalize-space(.)="My First Phdthesis"]]
    # Click Button   id=delete_selected
    # NOW DISMISS POP-UP
    # Handle Alert   DISMISS
    # Page Should Contain  UniqueNameForphdthesis



Removal of misc citation works correctly if confirmation pop-up is accepted
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  misc
    # CREATE CITATION FIRST
    Input Text  name:name  UniqueNameFormisc
    Input Text  author_misc  Michael Scott
    Input Text  title_misc  The Best Boss
    Input Text  year_misc  1996
    Input Text  month_misc  January
    Input Text  howpublished_misc  fictionally published by Dunder Mifflin
    Input Text  note_misc  really insightful
    Click Button  Save citation
    Page Should Contain  UniqueNameFormisc

    # NOW REMOVE IT
    Click Element  xpath=//table//tbody//tr[td[normalize-space(.)="The Best Boss"]]
    Click Button   id=delete_selected
    # NOW ACCEPT POP-UP
    Handle Alert   ACCEPT
    Page Should Not Contain  UniqueNameFormisc

Removal of misc citation works correctly if confirmation pop-up is dismissed
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  misc
    # CREATE CITATION FIRST
    Input Text  name:name  UniqueNameFormisc
    Input Text  author_misc  Michael Scott
    Input Text  title_misc  The Best Boss
    Input Text  year_misc  1996
    Input Text  month_misc  January
    Input Text  howpublished_misc  fictionally published by Dunder Mifflin
    Input Text  note_misc  really insightful
    Click Button  Save citation
    Page Should Contain  UniqueNameFormisc

    # NOW REMOVE IT
    Click Element  xpath=//table//tbody//tr[td[normalize-space(.)="The Best Boss"]]
    Click Button   id=delete_selected
    # NOW DISMISS POP-UP
    Handle Alert   DISMISS
    Page Should Contain  UniqueNameFormisc