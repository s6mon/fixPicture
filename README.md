# fixPicture
method to fix a part of picture by pad / eye tracking or mix between the two


How use : ./fixPartOfPict.py ...
There is 2 modes test and expe
  -test run with : test nameFile reverse
    test : string "test"
    nameFile : is the name in ressources directory where is obj format ressource/myOBJ.obj => myOBJ
    reverse : 0 or 1 for reverse vertices order to array of glDrawArrays
  -expe run with : expe userName technique
    userName : string
    technique : 0 to use T1 (statue quo), 1 for T2 (pdp = cursor) and 2 for T3 (pdp = eyes)
