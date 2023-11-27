



def form_input(name, label, default_value=None, autocomplete_field='', help_message='', input_type='text'):
    

    label_content = f'<label for="{name}" class="form-label" >{label}</label>'

    input_content = f'''<input type="{input_type}" autocomplete="{autocomplete_field}" class="form-control" id="{name}" name="{name}" aria-describedby="{name}Help" value="{str(default_value) if default_value else ''}">'''
    
    content = f'''
      <div class="mb-3">
        {label_content if label else ''}
        {input_content}
        <div id="{name}Help" class="form-text">{help_message}</div>
      </div>

    '''

    return content




def form_input_text(name, label, default_value=None, autocomplete_field='', help_message=''):
    input_type = 'text'
    return form_input(name, label, default_value, autocomplete_field, help_message, input_type)

def form_input_date(name, label, default_value=None,autocomplete_field='',  help_message=''):
    input_type = 'date'
    return form_input(name, label, default_value,autocomplete_field,  help_message, input_type)

def form_input_email(name, label, default_value=None, autocomplete_field='',  help_message=''):
    input_type = 'email'
    return form_input(name, label, default_value,autocomplete_field,  help_message, input_type)

def form_input_password(name, label, default_value=None, autocomplete_field='',  help_message=''):
    input_type = 'password'
    return form_input(name, label, default_value,autocomplete_field, help_message, input_type)

def form_input_tel(name, label, default_value=None, autocomplete_field='',  help_message=''):
    input_type = 'tel'
    return form_input(name, label, default_value,autocomplete_field, help_message, input_type)

def form_input_url(name, label, default_value=None, autocomplete_field='',  help_message=''):
    input_type = 'url'
    return form_input(name, label, default_value,autocomplete_field,  help_message, input_type)

def form_input_search(name, label, default_value=None, autocomplete_field='',  help_message=''):
    input_type = 'search'
    return form_input(name, label, default_value, autocomplete_field, help_message, input_type)


def form_input_two(name, label, default_value='', autocomplete_field='', name2='', label2='', default_value2='', autocomplete_field2='', help_message='', input_type='text'):
    
    
    content = f'''
      <div class="row mb-3">
        <div class="col">
            <label for="{name}" class="form-label">{label}</label>
            <input type="{input_type}" autocomplete="{autocomplete_field}" class="form-control" id="{name}" name="{name}" aria-describedby="{name}Help" value="{str(default_value) if default_value else ''}">
        
        </div>
        <div class="col">
            <label for="{name2}" class="form-label">{label2}</label>
            <input type="{input_type}" autocomplete="{autocomplete_field2}" class="form-control" id="{name2}" name="{name2}" aria-describedby="{name2}Help" value="{str(default_value2) if default_value2 else ''}">
        </div>
        <div id="{name}Help" class="form-text">{help_message}</div>
        
      </div>

    '''

    return content



"""
<input type="button">
<input type="checkbox">
<input type="color">
<input type="date">
<input type="datetime-local">
<input type="email">
<input type="file">
<input type="hidden">
<input type="image">
<input type="month">
<input type="number">
<input type="password">
<input type="radio">
<input type="range">
<input type="reset">
<input type="search">
<input type="submit">
<input type="tel">
<input type="text">
<input type="time">
<input type="url">
<input type="week">
"""


'''
"name"
"honorific-prefix"
"given-name"
"additional-name"
"family-name"
"honorific-suffix"
"nickname"
"username"
"new-password"
"current-password"
"one-time-code"
"organization-title"
"organization"
"street-address"
"address-line1"
"address-line2"
"address-line3"
"address-level4"
"address-level3"
"address-level2"
"address-level1"
"country"
"country-name"
"postal-code"
"cc-name"
"cc-given-name"
"cc-additional-name"
"cc-family-name"
"cc-number"
"cc-exp"
"cc-exp-month"
"cc-exp-year"
"cc-csc"
"cc-type"
"transaction-currency"
"transaction-amount"
"language"
"bday"
"bday-day"
"bday-month"
"bday-year"
"sex"
"url"
"photo"


'''