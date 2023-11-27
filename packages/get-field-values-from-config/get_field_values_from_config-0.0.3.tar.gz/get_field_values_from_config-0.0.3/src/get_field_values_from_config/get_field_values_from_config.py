import logging
import arrow
import re

__version__ = '1.1'

today = arrow.now()

def get_field_values(raw_emp, schema_field, delta_date, data_profiles):

    original_value_type = schema_field['valueType']['value']
    emp = raw_emp['field']
    source_field = schema_field['sourceField']['value']
    try:
        has_planned_change = raw_emp['hasPlannedChange'] == '1'
    except:
        has_planned_change = False
    if schema_field['fieldType'] == 'dataProfile':
        schema_field['valueType']['value'] = 'uniqueImportId'
    output = {
        "is_modified": False,
        "always_include": schema_field['alwaysInclude'],
        "planned_change" : schema_field['plannedChange'],
        'field_value': "",
        "valid_from": "",
        'source_field': schema_field['sourceField']['value'],
        'field_value_planned': '',
        'valid_from_planned': '',
        'is_modified_planned': False,
        'canceled_planned_change': False,
        'canceled_planned_change_valid_from': "",
        'objectFields': "",
        'has_value': False,
        "batch_run_change": False,
    }
    try:
    
        if schema_field['fieldType'] == 'hardCoded':
            output['field_value'] = schema_field['hardCodedValue']
        elif schema_field['fieldType'] == 'object':
            object_fields = get_object_fields(emp, schema_field['objectField'], delta_date)
            output['objectFields'] = object_fields['fields']
            output['is_modified'] = object_fields['is_modified']
            output['has_value'] = object_fields['has_value']
            output['valid_from'] = object_fields['valid_from']
            output['batch_run_change'] = object_fields['batch_run_change']
        elif schema_field['fieldType'] == 'concat':
            concat_output = concat_value(emp, schema_field['concatedOutput'], delta_date)
            output['field_value'] = concat_output['field_value']
            output['valid_from'] = concat_output['valid_from']
            output['is_modified'] = concat_output['is_modified']
            output['batch_run_change'] = concat_output['batch_run_change']
            if has_planned_change:
                try:
                    try:
                        concat_output_planned = concat_value_planned(emp, schema_field['concatedOutput'], delta_date)
                        output['is_modified_planned'] = concat_output_planned['is_modified']
                        output['field_value_planned'] = concat_output_planned['field_value']
                        output['valid_from_planned'] = concat_output_planned['valid_from']
                    except:
                        pass
                except:
                    pass
        elif schema_field['fieldType'] == 'c1Field' or schema_field['fieldType'] == 'dataProfile':
            c1Field = emp[schema_field['c1Field']['value']]
            output['field_value'] = c1Field['data'][schema_field['valueType']['value']]
            if schema_field['c1Field']['type'] == "PERCENTAGE":
                output['field_value'] = c1Field['data'][schema_field['valueType']['value']].replace('%', '')
            output['valid_from'] = c1Field['dataValidFrom']
            try:
                output['is_modified'] = arrow.get(c1Field['lastModified']) > delta_date
                output['batch_run_change'] = c1Field['lastModified'][11:15] == '04:0' and int(c1Field['lastModified'][15:16]) < 6
            except Exception as e:
                pass
            if has_planned_change:
                try:
                    planned_field = c1Field['plannedChange']
                    output['is_modified_planned'] = arrow.get(planned_field['lastModified']) > delta_date
                    output['field_value_planned'] = planned_field['data'][schema_field['valueType']['value']]
                    if schema_field['c1Field']['type'] == "PERCENTAGE":
                        output['field_value_planned'] = planned_field['data'][schema_field['valueType']['value']].replace('%', '')
                    output['valid_from_planned'] = planned_field['dataValidFrom']
                except:
                    pass
        elif schema_field['fieldType'] == 'calculated':
            calculated_values = calculated_output(schema_field['calculatedValue'],emp,delta_date)
            output['field_value'] = str(calculated_values['field_value'])
            output['valid_from'] = calculated_values['valid_from']
            output['is_modified'] = calculated_values['is_modified']
            output['field_value_planned'] = str(calculated_values['field_value_planned'])
            output['valid_from_planned'] = calculated_values['valid_from_planned']
            output['is_modified_planned'] = calculated_values['is_modified_planned']
            output['batch_run_change'] = calculated_values['batch_run_change']
    
        elif schema_field['fieldType'] == 'logic':
            condition_passed = False
            condition_passed_planned = False
            
            for condition in schema_field['customLogic']:
                if not condition_passed:       
                    try:
                        if not condition['else']:
                            test_condition = loop_condition_fields(emp, condition['conditionFields'],delta_date)
                            output['is_modified'] = test_condition['is_modified']
                            output['valid_from'] = test_condition['valid_from']
                            output['batch_run_change'] = test_condition['batch_run_change']
                        else:
                            test_condition = {'pass_condition': True, 'is_modified': False, 'valid_from': ''}
                        
                        condition_passed = test_condition['pass_condition']
                        if test_condition['pass_condition']:
                            if condition['fieldType'] == 'concat':
                                concated_values = concat_value(emp, condition['concatedOutput'],delta_date)['field_value']
                                output['field_value'] = concated_values['field_value']
                                output['valid_from'] = concated_values['valid_from']
                                output['is_modified'] = concated_values['is_modified']
                                output['batch_run_change'] = concated_values['batch_run_change']
                                
                            elif condition['fieldType'] == 'c1Field':
                                value_type = condition['valueType']['value']
                                if not output['is_modified']:
                                    try:
                                        if arrow.get(emp[condition['fieldValue']['value']]['lastModified']) > delta_date:
                                            output['is_modified'] = True
                                            output['batch_run_change'] = emp[condition['fieldValue']['value']]['lastModified'][11:15] == '04:0' and int(emp[condition['fieldValue']['value']]['lastModified'][15:16]) < 6
                                        
                                    except:
                                        pass                        
                                output['field_value'] = emp[condition['fieldValue']['value']]['data'][value_type]
                                output['valid_from'] = emp[condition['fieldValue']['value']]['dataValidFrom']
                                if has_planned_change:
                                    try:
                                        planned_field = emp[condition['fieldValue']['value']]['plannedChange']
                                        output['is_modified_planned'] = arrow.get(planned_field['lastModified']) > delta_date
                                        output['field_value_planned'] = planned_field['data'][value_type]
                                        output['valid_from_planned'] = planned_field['dataValidFrom']
                                    except:
                                        pass
                            elif condition['fieldType'] == 'object':
                                object_fields = get_object_fields(emp, condition['objectField'], delta_date)
                                output['objectFields'] = object_fields['fields']
                                output['is_modified'] = object_fields['is_modified']
                                output['has_value'] = object_fields['has_value']
                                output['valid_from'] = object_fields['valid_from']
                                output['batch_run_change'] = object_fields['batch_run_change']
                                if test_condition['is_modified']:
                                    output['is_modified'] = True
                                    output['valid_from'] = test_condition['valid_from']
                                    output['batch_run_change'] = test_condition['batch_run_change']
                            elif condition['fieldType'] == 'calculated':                   
                                calculated_values = calculated_output(condition['calculatedValue'],emp,delta_date)
                                output['field_value'] = str(calculated_values['field_value'])
                                output['valid_from'] = calculated_values['valid_from']
                                output['is_modified'] = calculated_values['is_modified']
                                output['bacth_run_change'] = calculated_values['batch_run_change']

                            else:
                                output['field_value'] = condition['textValue']
                    except Exception as e:
                        #logging.error(f'Condition loop, get_field_values_from_cofig: Field: {source_field} Error:  {e}. Condition: {condition}')
                        pass
                if not condition_passed_planned: 
                    if has_planned_change:
                        try:
                            if not condition['else']:
                                test_condition_planned = loop_condition_fields_planned(emp, condition['conditionFields'],delta_date)   
                                output['is_modified_planned'] = test_condition_planned['is_modified']
                                output['valid_from_planned'] = test_condition_planned['valid_from']
                            else:
                                test_condition_planned = {'pass_condition': True, 'is_modified': False, 'valid_from': ''}
                            if test_condition_planned['pass_condition']:
                                condition_passed_planned = True
                                if condition['fieldType'] == 'concat':
                                    output['field_value_planned'] = concat_value_planned_with_logic(emp, condition['concatedOutput'],test_condition_planned['valid_from'])
                                elif condition['fieldType'] == 'c1Field':
                                    value_type = condition['valueType']['value']
                                    output['field_value_planned'] = emp[condition['fieldValue']['value']]['data'][value_type]
                                    try:
                                        if arrow.get(planned_field['lastModified']) >= arrow.get(test_condition_planned['valid_from']):
                                            output['valid_from_planned'] = planned_field['dataValidFrom']
                                            planned_field = emp[condition['fieldValue']['value']]['plannedChange']
                                            output['is_modified_planned'] = arrow.get(planned_field['lastModified']) > delta_date
                                            output['field_value_planned'] = planned_field['data'][value_type]
                                            output['valid_from_planned'] = planned_field['dataValidFrom']                                       
                                    except:
                                        pass

                                elif condition['fieldType'] == 'hardCoded':
                                    output['field_value_planned'] = condition['textValue']
                                elif condition['fieldType'] == 'calculated':
                                    calculated_values = calculated_output(condition['calculatedValue'],emp,delta_date)
                                    output['field_value_planned'] = str(calculated_values['field_value_planned'])
                                    output['valid_from_planned'] = calculated_values['valid_from_planned']
                                    output['is_modified_planned'] = calculated_values['is_modified_planned']
                        except Exception as e:
                            #logging.error(f'Planned change condition, get_field_values_from_cofig: {e}')
                            pass

        ### If field is from Org-dataprofile, swap the value with the value from the data-profile from the org-object. By doing this it's possible to get planned changes and valid from data profile fields
        if schema_field['fieldType'] == 'dataProfile':
            try:
                output['field_value'] = data_profiles[output['field_value']][schema_field['dataProfileField']['label']][original_value_type]
            except Exception as e:
                logging.error(f'Data profile error {e}')
                pass
            try:
                output['field_value_planned'] = data_profiles[output['field_value_planned']][schema_field['dataProfileField']['label']][original_value_type]
                output['is_modified_planned'] = True if output['field_value_planned'] != output['field_value'] else False
            except Exception as e:
                pass
            
            #Check if new data proile value is different from the original value
            try:
                previous_data_profile_value = data_profiles[emp[schema_field['c1Field']['value']]['timelineChange'][1]['data'][schema_field['valueType']['value']]][schema_field['dataProfileField']['label']][original_value_type]
                output['is_modified'] = True if previous_data_profile_value != output['field_value'] else False
            except Exception as e:
                pass
        return output
    except Exception as e:
        source_field = output['source_field']
        #logging.error(f'Failed to generate field {source_field}:  {e}')
        return output


def loop_condition_fields(emp, conditionFields,delta_date):
    condition_valid_froms = []
    output = {
        'is_modified': False,
        'valid_from': '',
        'pass_condition' : True,
        'batch_run_change': False
    }
    try:
        for conditionLogic in conditionFields:
            condition_field = emp[conditionLogic['field']['value']]
            try:
                if arrow.get(condition_field['lastModified']) > delta_date:
                    output['is_modified'] = True
                    if condition_field['lastModified'][11:15] == '04:0' and int(condition_field['lastModified'][15:16]) < 6:
                        output['batch_run_change'] = True
                if len(condition_valid_froms) == 0:
                    condition_valid_froms.append(arrow.get(condition_field['dataValidFrom']))
                else:
                    if arrow.get(condition_field['dataValidFrom']) > condition_valid_froms[0]:
                        condition_valid_froms[0] = arrow.get(condition_field['dataValidFrom'])
            except:
                pass
            check_values = []
            if conditionLogic['hasValueFromList']:
                for check_value in conditionLogic['listValues']:
                    check_values.append(check_value['value'])
            else:
                for text_value in conditionLogic['value'].split(','):
                    check_values.append(text_value)
            if not check_if_passes_condition(condition_field['data'], conditionLogic['operator']['value'], check_values,conditionLogic['hasValueFromList']):
                output['pass_condition'] = False
                break
    except Exception as e:
        logging.error(f'Error in loop_condition_fields: {e}')
        pass
    try:
        output['valid_from'] = str(condition_valid_froms[0].date())
    except:
        output['valid_from'] = ''
    return output
    

def check_if_passes_condition(value, operator, check_values,value_from_list):

    output = True
    if value_from_list:
        value = value['guid']
    else:
        value = value['value']
    if operator == '=':
        if value not in check_values:
            output = False
    elif operator == "!=":
        if value in check_values:
            output = False
    elif operator == "0":
        if value:
            output = False
    elif operator == "!0":
        if not value:
            output = False
    elif operator == ">=":
        try:
            output = arrow.get(check_values[0]) <= arrow.get(value)
        except Exception as e:
            output = False
    elif operator == "<=":
        try:
            output = arrow.get(check_values[0]) >= arrow.get(value)
        except Exception as e:
            output = False
    elif operator == "<":
        try:
            output = arrow.get(check_values[0]) > arrow.get(value)
        except Exception as e:
            output = False
    elif operator == ">":
        try:
            output = arrow.get(check_values[0]) < arrow.get(value)
        except Exception as e:
            output = False


    return output


def loop_condition_fields_planned(emp, conditionFields,delta_date):
    condition_valid_froms = []
    output = {
        'is_modified': False,
        'valid_from': '',
        'pass_condition' : True
    }
    try:
        for conditionLogic in conditionFields:
            try:
                condition_field = emp[conditionLogic['field']['value']]['plannedChange']
                if arrow.get(condition_field['lastModified']) > delta_date:
                    output['is_modified'] = True
            except:
                condition_field = emp[conditionLogic['field']['value']]
            
            if len(condition_valid_froms) == 0:
                condition_valid_froms.append(arrow.get(condition_field['dataValidFrom']))
            else:
                if arrow.get(condition_field['dataValidFrom']) > condition_valid_froms[0]:
                    condition_valid_froms[0] = arrow.get(condition_field['dataValidFrom'])
            check_values = []
            if conditionLogic['hasValueFromList']:
                for check_value in conditionLogic['listValues']:
                    check_values.append(check_value['value'])
            else:
                check_values.append(conditionLogic['value'])
            if not check_if_passes_condition(condition_field['data'], conditionLogic['operator']['value'], check_values,conditionLogic['hasValueFromList']):
                output['pass_condition'] = False
                break
    except:
        pass
    output['valid_from'] = str(condition_valid_froms[0].date())

    return output
def concat_value(emp, concated_fields,delta_date):
    output = {
        'is_modified': False,
        'valid_from': '',
        'field_value': "",
        'batch_run_change': False
    }
    valid_froms = []
    for field in concated_fields:

            if field['type'] == 'text':
                output['field_value'] += field['value']
            else:
                substring_start = int(field['substringStart']) if field['substringStart'] else 0
                substring_end = int(field['substringEnd']) if field['substringEnd'] else 500
                try:
                    value_type = field['valueType']['value']
                    output['field_value'] += emp[field['value']['value']]['data'][value_type][substring_start:substring_end]
                    if len(valid_froms) == 0:
                        valid_froms.append(arrow.get(emp[field['value']['value']]['dataValidFrom']))
                    elif arrow.get(emp[field['value']['value']]['dataValidFrom']) > valid_froms[0]:
                        valid_froms[0] = arrow.get(emp[field['value']['value']]['dataValidFrom'])
                    try:
                        if arrow.get(emp[field['value']['value']]['lastModified']) > delta_date:
                            output['is_modified'] = True
                            if emp[field['value']['value']]['lastModified'][11:15] == '04:0' and int(emp[field['value']['value']]['lastModified'][15:16]) < 6:
                                output['batch_run_change'] = True
                    except:
                        pass
                except Exception as e:
                    field_name = field['value']['label']
                    logging.warning(f"Missing field {field_name} for concat field")
    output['valid_from'] = str(valid_froms[0].date())
    return output

def concat_value_planned(emp, concated_fields,delta_date):
    output = {
        'is_modified': False,
        'valid_from': '',
        'field_value': ""
    }
    valid_froms = []
    for field in concated_fields:
        try:
            has_planned = False

            if field['type'] == 'text':
                output['field_value'] += field['value']
            else:
                value_type = field['valueType']['value']
                substring_start = int(field['substringStart']) if field['substringStart'] else 0
                substring_end = int(field['substringEnd']) if field['substringEnd'] else 500
                try:
                    planned_field = emp[field['value']['value']]['plannedChange']
                    try:
                        if arrow.get(planned_field['lastModified']) > delta_date:
                                output['is_modified'] = True
                                has_planned = True
                    except:
                        pass
                    output['field_value'] += planned_field['data'][value_type][substring_start:substring_end]
                    if len(valid_froms) == 0:
                        valid_froms.append(arrow.get(planned_field['dataValidFrom']))
                    elif arrow.get(planned_field['dataValidFrom']) > valid_froms[0]:
                        valid_froms[0] = arrow.get(planned_field['dataValidFrom'])

                except:
                    pass
                try:
                    if not has_planned:
                        output['field_value'] += emp[field['value']['value']]['data'][value_type][substring_start:substring_end]
                except Exception as e:
                    field_name = field['value']['label']
                    logging.warning(f"Missing field {field_name} for concat field")
        except Exception as e:
            pass

    output['valid_from'] = str(valid_froms[0].date())
    return output

def concat_value_planned_with_logic(emp, concated_fields,valid_from):
    output = ""
    for field in concated_fields:
        has_planned = False

        if field['type'] == 'text':
            output += field['value']
        else:
            value_type = field['valueType']['value']
            substring_start = int(field['substringStart']) if field['substringStart'] else 0
            substring_end = int(field['substringEnd']) if field['substringEnd'] else 500
            try:
                planned_field = emp[field['value']['value']]['plannedChange']
                if arrow.get(planned_field['dataValidFrom']) <= arrow.get(valid_from):
                    has_planned = True
                    output += planned_field['data'][value_type][substring_start:substring_end]
                else:
                    output += emp[field['value']['value']]['data'][value_type][substring_start:substring_end]
            except:
                pass
            try:
                if not has_planned:
                    output += emp[field['value']['value']]['data'][value_type][substring_start:substring_end]
            except Exception as e:
                field_name = field['value']['label']
                logging.warning(f"Missing field {field_name} for concat field")
    return output


def calculated_output(expression, emp,delta_date):
    field_ids = re.findall(r'#(\d+)', expression)
    field_values = get_field_values_calc(emp, field_ids,delta_date)
    expression_planned = expression

# Helper function to calculate expression within parentheses
    def evaluate_parentheses(sub_expression, field_values, planned):
        # Find and replace field IDs with their respective values
        value_type = 'value_planned' if planned else 'value'
        sub_expression = re.sub(r'#(\d+)', lambda x: str(field_values[x.group(1)][value_type]), sub_expression)
        
        # Evaluate the expression within parentheses
        return eval(sub_expression)

    # Replace field IDs with their respective values

    expression = re.sub(r'#(\d+)', lambda x: str(field_values[x.group(1)]['value']), expression)

    expression_planned = re.sub(r'#(\d+)', lambda x: str(field_values[x.group(1)]['value_planned']), expression_planned)


    # Regular expression to match parentheses
    pattern = re.compile(r'\(([^()]+)\)')

    # Evaluate expressions within parentheses recursively
    while re.search(pattern, expression):
        expression = re.sub(pattern, lambda x: str(evaluate_parentheses(x.group(1), field_values, False)), expression)

    while re.search(pattern, expression_planned):
        expression_planned = re.sub(pattern, lambda x: str(evaluate_parentheses(x.group(1), field_values, True)), expression_planned)

    # Evaluate the final expression
    output = {
        'field_value' : eval(expression),
        'field_value_planned': eval(expression_planned),
        'is_modified': field_values['is_modified'],
        'is_modified_planned': field_values['is_modified_planned'],
        'valid_from': field_values['valid_from'],
        'valid_from_planned': field_values['valid_from_planned'],
    }

    return output


def get_field_values_calc(emp, field_ids, delta_date):
    field_values = {
        'valid_from': '',
        'valid_from_planned': '',
        'is_modified': False,
        'is_modified_planned': False,
        'batch_run_change': False,
    }
    for field_id in field_ids:
        field_values[field_id]= {
            'value': float(emp[field_id]['data']['value'].replace('%', '')),
            'value_planned': '',
        }

        if not field_values['valid_from'] or arrow.get(emp[field_id]['dataValidFrom']) > arrow.get(field_values['valid_from']):
            field_values['valid_from'] = emp[field_id]['dataValidFrom']

        try:
            if arrow.get(emp[field_id]['lastModified']) > delta_date:
                field_values['is_modified'] = True
        except:
            pass

        try:
            field_planned = emp[field_id]['plannedChange']
            field_values[field_id]['value_planned'] = float(field_planned['data']['value'].replace('%', ''))
            if arrow.get(field_planned['lastModified']) > delta_date:
                field_values['is_modified_planned'] = True
                if field_planned['lastModified'][11:15] == '04:0' and int(field_planned['lastModified'][15:16]) < 6:
                    field_values['batch_run_change'] = True
            if not field_values['valid_from_planned'] or arrow.get(field_planned['dataValidFrom']) > arrow.get(field_values['valid_from_planned']) :
                field_values['valid_from_planned'] = field_planned['dataValidFrom']
        except:
            pass
            field_values[field_id]['value_planned'] = float(emp[field_id]['data']['value'].replace('%', ''))
        
        
    return field_values

def get_object_fields(emp, object_fields, delta_date):
    fields = {}
    is_modified = False
    has_value = False
    valid_from = ""
    batch_run_change = False
    try:
        for field in object_fields['fields']:
            if field['fieldType'] == 'c1Field':
                value_type = field['valueType']['value']
                field_id = field['c1Field']['value']
                value = emp[field_id]['data'][value_type]
            else:
                value = field['hardcodedValue']
            fields[field['sourceField']['value']] = value
            if value:
                has_value = True
            try:
                if arrow.get(emp[field_id]['lastModified']) > delta_date:
                    is_modified = True
                    if emp[field_id]['lastModified'][11:15] == '04:0' and int(c1Field['lastModified'][15:16]) < 6:
                        batch_run_change = True

            except:
                pass
            try:
                if not valid_from or arrow.get(emp[field_id]['dataValidFrom']) > arrow.get(valid_from):
                    valid_from = emp[field_id]['dataValidFrom']
            except:
                pass
            
        return {
            'fields': fields,
            "is_modified": is_modified ,
            'has_value': has_value,
            'valid_from': valid_from,
            'batch_run_change': batch_run_change
        }
    except Exception as e:
        logging.error(e)
        return {
            'fields': {},
            'is_modified': is_modified,
            'has_value': has_value,
            'valid_from': valid_from,
            'batch_run_change': batch_run_change
        }

