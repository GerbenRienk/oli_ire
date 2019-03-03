

def write_odm_line( oc_item_name, ls_item_value, is_date=False, is_time=False, is_decimal=False, is_integer=False, is_utf8 = False):
    _one_line = ''
    if (ls_item_value):
        _this_value = ls_item_value
        if (is_date):
            _this_value = ls_item_value[0:10]
        if (is_time):
            # time field: for now we do nothing with it
            _this_value = _this_value
            
        if (is_decimal):
            _this_value = str(ls_item_value)
        if (is_integer):
            _this_value = str(int(float(ls_item_value)))
        if (is_utf8):
            _this_value = str(_this_value.encode(encoding="ascii",errors="xmlcharrefreplace"))
            # now we have something like b'some text &amp; more' so we want to loose the first two characters and the last one
            # TODO: make this nicer somehow
            _this_value = _this_value[2:]
            _this_value = _this_value[:-1]
              
        _one_line = _one_line + '            <ItemData ItemOID="' + oc_item_name + '" Value="' + _this_value + '"/>'
    else:
        _one_line = _one_line + '            <ItemData ItemOID="' + oc_item_name + '" Value=""/>'
    #print(_one_line)
    return _one_line

def compose_odm(study_subject_oid, data_ls):
    """
    compose the xml-content to send to the web-service 
    just for this one occasion we write out everything literally
    and we make a big exception for birth-weight, which is given 
    in grams, but must be imported in kilo's and grams 
    """
    
    if (data_ls['q5birthweightgram'] is not None):
        kilograms = int(float(data_ls['q5birthweightgram'])/1000)
        I_IEFAM_BIRTHWEIGHTKG = str(kilograms)
        if (I_IEFAM_BIRTHWEIGHTKG == '0'):
            I_IEFAM_BIRTHWEIGHTKG = ''
        grams = int(float(data_ls['q5birthweightgram']) - kilograms * 1000)
        I_IEFAM_BIRTHWEIGHTGR = str(grams)
        #print(data_ls['q5birthweightgram'], I_IEFAM_BIRTHWEIGHTKG, I_IEFAM_BIRTHWEIGHTGR)
    else:
        I_IEFAM_BIRTHWEIGHTKG = ''
        I_IEFAM_BIRTHWEIGHTGR = ''
    
    # opening tags
    _odm_data = ''
    _odm_data = _odm_data + '<ODM>'
    _odm_data = _odm_data + '  <ClinicalData StudyOID="S_CPIRE">'
    _odm_data = _odm_data + '    <SubjectData SubjectKey="' + study_subject_oid + '">'
    _odm_data = _odm_data + '      <StudyEventData StudyEventOID="SE_IRE_CD">'
    _odm_data = _odm_data + '        <FormData FormOID="F_IEFAMILYFORM_V11">'
    _odm_data = _odm_data + '          <ItemGroupData ItemGroupOID="IG_PTFAM_UNGROUPED" ItemGroupRepeatKey="1" TransactionType="Insert">'
    # data
    _odm_data = _odm_data + write_odm_line('I_IEFAM_RELATIONSHIP', data_ls['q1relationship'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_RELATIONSHIPOTH', data_ls['q1relationshipother'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_DATEOFBIRTHCOMPLETE', data_ls['q3birthdatecomplete'], is_date=True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_GENDER', data_ls['q4sex'])
    # begin first exception !
    _odm_data = _odm_data + write_odm_line('I_IEFAM_BIRTHWEIGHTKG', I_IEFAM_BIRTHWEIGHTKG)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_BIRTHWEIGHTGR', I_IEFAM_BIRTHWEIGHTGR)
    # end first exception
    _odm_data = _odm_data + write_odm_line('I_IEFAM_IE_BIRTHWEIGHTLBS', data_ls['qiebirthweightlbs'], is_integer = True) 
    _odm_data = _odm_data + write_odm_line('I_IEFAM_IE_BIRTHWEIGHTOZ', data_ls['qiebirthweightoz'], is_integer = True) 
    
    # generated from testcosi5
    _odm_data = _odm_data + write_odm_line('I_IEFAM_LATEEARLYBIRTH', data_ls['q6fullterm'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_BREASTFEDEVER', data_ls['q7breastfed'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_BREASTFEDHOWLONG', data_ls['q7breastfedmonths'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_BREASTEXCLEVER', data_ls['q8breastfedexclusive'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_BREASTEXCLUSIVE', data_ls['q8breastexclusive'], is_integer = True)   
    _odm_data = _odm_data + write_odm_line('I_IEFAM_DISTANCESCHOOLHOME', data_ls['q9distance'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_TRANSPSCHOOLFROM', data_ls['q10transpschoolfrom'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_TRANSPSCHOOLTO', data_ls['q10transpschoolto'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_REASONMOTORIZED', data_ls['q10areasonmotorized']) 
    _odm_data = _odm_data + write_odm_line('I_IEFAM_REASONMOTORIZEDOTH', data_ls['q10areasonmotorizedo'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_SAFEROUTESCHOOL', data_ls['q11routesafe']) 
    
    #awful hack for wrong codes
    if (data_ls['q13sportclubsfrequen'] is not None and data_ls['q13sportclubsfrequen'] != ''):
        q13sportclubsfrequen = int(data_ls['q13sportclubsfrequen'])
        q13sportclubsfrequen = q13sportclubsfrequen - 1   
    else:
        q13sportclubsfrequen = ''
    _odm_data = _odm_data + write_odm_line('I_IEFAM_SPORTCLUB', data_ls['q12sportclubs'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_SPORTCLUBFREQ', q13sportclubsfrequen, is_integer = True)
    
    _odm_data = _odm_data + write_odm_line('I_IEFAM_BEDTIME', data_ls['q14bedtime'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_WAKEUPTIME', data_ls['q15wakeuptime'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_WDSPLAYINGACTIVE', data_ls['q16playoutweekdays'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_WEPLAYINGACTIVE', data_ls['q16playouteweekdays'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_WDREADING', data_ls['q17readingweekdays'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_WEREADING', data_ls['q17readingweekends'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_WDELECTRONICSH', data_ls['q18wdelectronicsh'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_WDELECTRONICSM', data_ls['q18wdelectronicsm'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_WEELECTRONICSH', data_ls['q18weelectronicsh'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_WEELECTRONICSM', data_ls['q18weelectronicsm'], is_integer = True)
    
    # begin second exception !
    # these checkboxes can only be Y in ls
    # which corresponds to 1 in oc
    if (data_ls['q18wdelectrnotatall[NAA]'] == 'Y'):
        q18wdelectrnotatall = '1'
    else:
        q18wdelectrnotatall = ''
    if (data_ls['q18weelectrnotatall[NAA]'] == 'Y'):
        q18weelectrnotatall = '1'
    else:
        q18weelectrnotatall = ''
        
    _odm_data = _odm_data + write_odm_line('I_IEFAM_WDELECTRNOTATALL', q18wdelectrnotatall)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_WEELECTRNOTATALL', q18weelectrnotatall)
    # end second exception !
    
    _odm_data = _odm_data + write_odm_line('I_IEFAM_IE_MOBDEV', data_ls['q18iemobdev']) 

    _odm_data = _odm_data + write_odm_line('I_IEFAM_BREAKFAST', data_ls['q19breakfast'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_FREQCANDY', data_ls['q20[Candy]'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_FREQCEREALS', data_ls['q20[Cereals]'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_CEREALSSUGAR', data_ls['q20cerealssugar'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_FREQCHEESE', data_ls['q20[Cheese]'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_FREQCHIPS', data_ls['q20[Chips]'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_FREQDAIRY', data_ls['q20[Dairy]'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_FREQDIET', data_ls['q20[DietSoftDrinks]'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_FREQEGG', data_ls['q20[Egg]'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_FREQFISH', data_ls['q20[Fish]'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_FREQFLAVOUREDMILK', data_ls['q20[FlavouredMilk]'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_FREQFRUIT', data_ls['q20[FreshFruit]'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_FREQFRUITJUICE', data_ls['q20[FruitJuice]'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_FREQLEGUMES', data_ls['q20[Legumes]'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_FREQLOWFATMILK', data_ls['q20[LowFatMilk]'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_FREQMEAT', data_ls['q20[Meat]'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_FREQSOFTDRINKS', data_ls['q20[SoftDrinksSugar]'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_FREQVEGETABLES', data_ls['q20[Vegetables]'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_FREQWHOLEFATMILK', data_ls['q20[WholeFatMilk]'])
    
    _odm_data = _odm_data + write_odm_line('I_IEFAM_WEIGHTOPINION', data_ls['q21weightopinion'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_HOUSEHOLDBLOODPRESSURE', data_ls['q22househouldbloodpr'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_HOUSEHOLDDIABETES', data_ls['q23householddiabetes'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_HOUSEHOLDCHOLESTEROL', data_ls['q24householdcholeste'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_SPOUSEHEIGHT', data_ls['q25spouseheight'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_SPOUSEWEIGHT', data_ls['q25spouseweight'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_YOUHEIGHT', data_ls['q25youheight'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_YOUWEIGHT', data_ls['q25youweight'])

    _odm_data = _odm_data + write_odm_line('I_IEFAM_HMNRBROTHER', data_ls['q26hmnr[Brother]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_HMNRELSE', data_ls['q26hmnr[Else]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_HMNRELSESPEC', data_ls['q26hmnrelsespec'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_HMNRFATHER', data_ls['q26hmnr[Father]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_HMNRFOSTER', data_ls['q26hmnr[Foster]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_HMNRGRANDFATHER', data_ls['q26hmnr[Grandfather]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_HMNRGRANDMOTHER', data_ls['q26hmnr[Grandmother]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_HMNRMOTHER', data_ls['q26hmnr[Mother]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_HMNRSISTER', data_ls['q26hmnr[Sister]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_HMNRSTEPFATHER', data_ls['q26hmnr[Stepfather]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_HMNRSTEPMOTHER', data_ls['q26hmnr[Stepmother]'], is_integer = True)
    
    _odm_data = _odm_data + write_odm_line('I_IEFAM_IE_CHILDBORNOTH', data_ls['q27childbornoth'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_IE_CHILDBORN', data_ls['q27childborn'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_IE_MOTHERBORNOTH', data_ls['q28motherbornoth'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_IE_MOTHERBORN', data_ls['q28motherborn'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_IE_FATHERBORNOTH', data_ls['q29fatherbornoth'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_IE_FATHERBORN', data_ls['q29fatherborn'])
    
    # yet another exception: value 4 must be changed into 9
    if (data_ls['q30language'] is not None and data_ls['q30language'] != ''):
        q30language = int(data_ls['q30language'])
        if (q30language == 4):
            q30language = 9
    else:
        q30language = ''
    _odm_data = _odm_data + write_odm_line('I_IEFAM_IE_LANGUAGE', q30language, is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_IE_LANGUAGEOTH', data_ls['q30languageoth'], is_utf8 = True)
    
    _odm_data = _odm_data + write_odm_line('I_IEFAM_EDUSPOUSE', data_ls['q31eduspouse'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_EDUYOU', data_ls['q31eduyou'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_EARNINGS', data_ls['q32earnings'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_OCCUPSPOUSE', data_ls['q33occupspouse'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_OCCUPSPOUSEOTH', data_ls['q33occupspouseoth'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_OCCUPYOU', data_ls['q33occupyou'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_OCCUPYOUOTH', data_ls['q33occupyouoth'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_IEFAM_DATECOMPLETION', data_ls['q34datecompletion'])
    _odm_data = _odm_data + write_odm_line('I_IEFAM_REMARKS', data_ls['q35remarks'], is_utf8 = True)




    # closing tags
    _odm_data = _odm_data + '          </ItemGroupData>'
    _odm_data = _odm_data + '        </FormData>'
    _odm_data = _odm_data + '      </StudyEventData>'
    _odm_data = _odm_data + '    </SubjectData>'
    _odm_data = _odm_data + '  </ClinicalData>'
    _odm_data = _odm_data + '</ODM>'

    return _odm_data
