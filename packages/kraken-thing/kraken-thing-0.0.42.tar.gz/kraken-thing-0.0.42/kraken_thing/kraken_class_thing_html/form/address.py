
from kraken_thing.kraken_class_thing_html.form.form_maker import form_maker

def address(record={}, prefix=''):




    config = [
        {'name': '@type', 'title': '', 'auto': '', 'type': 'hidden'},
        {'name': '@id', 'title': '', 'auto': '', 'type': 'hidden'},
        {'name': 'streetAddress', 'title': 'Street', 'auto': 'street-address', 'type': 'text'},
        {'name': 'addressLocality', 'title': 'City', 'auto': 'address-line1', 'type': 'text'},
        {'name': 'addressRegion', 'title': 'Province', 'auto': 'address-line2', 'type': 'text'},
        {'name': 'addressCountry', 'title': 'Country', 'auto': 'address-line3', 'type': 'text'},
        {'name': 'postalCode', 'title': 'Postal Code', 'auto': 'postal-code', 'type': 'text'},

    ]


    return form_maker(config, record, prefix)
    
   




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

'''
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
'''