*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser

#This is a copy-paste of creation robot tests but it also checks that canceling the removal works

*** Test Cases ***
Removal of article citation works correctly
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  article

    #THIS IS UNIQUE NAME FIELD
    Input Text  author_article  UniqueNameForArcticle_testtest123123

    Input Text  name:author  jhojkjsadfj
    Input Text  title_article  hfhhhdf
    Input Text  journal_article  tasd
    Input Text  year_article  1996
    Input Text  volume_article  100
    Input Text  number_article  500
    Input Text  pages_article  500
    Input Text  month_article  500123123
    Input Text  note_article  500192asdokasdkpasjd34349!==#¤J#¤JN
    Click Button  Save citation
    Page Should Contain  UniqueNameForArcticle_testtest123123
    Click Button  css:form.remove-form[data-name="UniqueNameForArcticle_testtest123123"] button
    Handle Alert  DISMISS
    Page Should Contain  UniqueNameForArcticle_testtest123123
    Click Button  css:form.remove-form[data-name="UniqueNameForArcticle_testtest123123"] button
    Handle Alert  ACCEPT
    Page Should Not Contain  UniqueNameForArcticle_testtest123123

Removal of book citation works correctly
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  book
    #This is unique name field
    Input Text  author_article  UniqueNameforBook_testtest123123
    Input Text  author_book  jhojkjsadfj
    Input Text  editor_book  bobmarley
    Input Text  title_book  hfhhhdf
    Input Text  publisher_book  bobmarleyscousin
    Input Text  year_book  1996
    Input Text  volume_book  10022
    Input Text  number_book  01230
    Input Text  series_book  52200
    Input Text  address_book  23rd Y03843 uqd
    Input Text  edition_book  123rdeiditon
    Input Text  month_book  22
    Input Text  note_book  500notes100!="#)23492834axvxcvxcv
    Click Button  Save citation
    Page Should Contain  UniqueNameforBook_testtest123123
    Click Button  css:form.remove-form[data-name="UniqueNameforBook_testtest123123"] button
    Handle Alert  DISMISS
    Page Should Contain  UniqueNameforBook_testtest123123
    Click Button  css:form.remove-form[data-name="UniqueNameforBook_testtest123123"] button
    Handle Alert  ACCEPT
    Page Should Not Contain  UniqueNameforBook_testtest123123

Removal of inproceedings citation works correctly
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  inproceedings

    #THIS IS UNIQUE NAME FIELD
    Input Text  author_article  UniqueNameforInproceedings_testtest123123

    Input Text  author_inproceedings  jhojkjsadfj
    Input Text  title_inproceedings  hfhhhdf
    Input Text  booktitle_inproceedings  booktitletesttest
    Input Text  editor_inproceedings  bobmarley
    Input Text  year_inproceedings  1996
    Input Text  series_inproceedings  52200
    Input Text  volume_inproceedings  10022
    Input Text  number_inproceedings  01230
    Input Text  month_inproceedings  JanFebJFSJF
    Input Text  pages_inproceedings  1010-123491
    Input Text  address_inproceedings  23rd Y03843 uqd
    Input Text  organization_inproceedings  helsingisdjasdn
    Input Text  publisher_inproceedings  bobmarleyscousin
    Input Text  note_inproceedings  500notes100!="#)23492834axvxcvxcv
    Click Button  Save citation
    Page Should Contain  UniqueNameforInproceedings_testtest123123
    Click Button  css:form.remove-form[data-name="UniqueNameforInproceedings_testtest123123"] button
    Handle Alert  DISMISS
    Page Should Contain  UniqueNameforInproceedings_testtest123123
    Click Button  css:form.remove-form[data-name="UniqueNameforInproceedings_testtest123123"] button
    Handle Alert  ACCEPT
    Page Should Not Contain  UniqueNameforInproceedings_testtest123123

Removal of mastersthesis citation works correctly
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  mastersthesis

    #THIS IS UNIQUE NAME FIELD
    Input Text  author_article  UniqueNameForMastersthesis_testtest123123

    Input Text  author_mastersthesis  notme
    Input Text  title_mastersthesis  hfhhhdf
    Input Text  school_mastersthesis  testingschool
    Input Text  type_mastersthesis  typeshixdxdxd
    Input Text  year_mastersthesis  1996
    Input Text  month_mastersthesis  JanFebJFSJF
    Input Text  address_mastersthesis  23rd Y03843 uqd
    Input Text  note_mastersthesis  500notes100!="#)23492834axvxcvxcv
    Click Button  Save citation
    Page Should Contain  UniqueNameForMastersthesis_testtest123123
    Click Button  css:form.remove-form[data-name="UniqueNameForMastersthesis_testtest123123"] button
    Handle Alert  DISMISS
    Page Should Contain  UniqueNameForMastersthesis_testtest123123
    Click Button  css:form.remove-form[data-name="UniqueNameForMastersthesis_testtest123123"] button
    Handle Alert  ACCEPT
    Page Should Not Contain  UniqueNameForMastersthesis_testtest123123
	
Removal of phdthesis citation works correctly
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  phdthesis

    #THIS IS UNIQUE NAME FIELD
    Input Text  author_article  UniqueNameForphdthesis_testtest123123

    Input Text  author_phdthesis  notme
    Input Text  title_phdthesis  hfhhhdf
    Input Text  school_phdthesis  testingschool
    Input Text  year_phdthesis  1996
    Input Text  month_phdthesis  JanFebJFSJF
    Input Text  keywords_phdthesis  robot,frameworks,stuff,is,good
    Input Text  address_phdthesis  23rd Y03843 uqd
    Input Text  note_phdthesis  500notes100!="#)23492834axvxcvxcv
    Click Button  Save citation
    Page Should Contain  UniqueNameForphdthesis_testtest123123
    Click Button  css:form.remove-form[data-name="UniqueNameForphdthesis_testtest123123"] button
    Handle Alert  DISMISS
    Page Should Contain  UniqueNameForphdthesis_testtest123123
    Click Button  css:form.remove-form[data-name="UniqueNameForphdthesis_testtest123123"] button
    Handle Alert  ACCEPT
    Page Should Not Contain  UniqueNameForphdthesis_testtest123123
	
Removal of misc citation works correctly
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  misc

    #THIS IS UNIQUE NAME FIELD
    Input Text  author_article  UniqueNameFormisc_testtest123123

    Input Text  author_misc  notme
    Input Text  title_misc  hfhhhdf
    Input Text  year_misc  1996
    Input Text  month_misc  JanFebJFSJF
    Input Text  howpublished_misc  it was posted on stackoverflow
    Input Text  note_misc  500notes100!="#)23492834axvxcvxcv
    Click Button  Save citation
    Page Should Contain  UniqueNameFormisc_testtest123123
    Click Button  css:form.remove-form[data-name="UniqueNameFormisc_testtest123123"] button
    Handle Alert  DISMISS
    Page Should Contain  UniqueNameFormisc_testtest123123
    Click Button  css:form.remove-form[data-name="UniqueNameFormisc_testtest123123"] button
    Handle Alert  ACCEPT
    Page Should Not Contain  UniqueNameFormisc_testtest123123
	
