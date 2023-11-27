# kraken datatype

## Overview
Library to extract, validate and normalize datatypes. 

datatypes:
- email
- url
- date
- country
- address
- telephone
- bool
- currency
- domain


## github
https://github.com/tactik8/krakcn_class_thing_v4

## pypi
https://pypi.org/project/kraken-thing/


## classes:
- Thing: representation of a schema.org thing
- Things: a collection of Thing
- Observation: Data points making up a thing


## How to use:

### Basics
```
from kraken_thing.kraken_class_thing.kraken_class_thing import Thing
from kraken_thing import Thing

t = Thing()
t.url = 'https://www.test.com'
print(t.url)

print(t.record)

```
### Metadata

Metadata can be provided in json record using @metadata

```
{ 
    "@type": "person",
    "@id": "abc123",
    "name": "Bob Smith",
    "@metadata": {
        "measuredPropertyContext": "",
        "language": "EN",
        "observationCredibility": 0.5,
        "observationDate": "2023-03-01",
        "validFrom": "2023-03-01",
        "validThrough": "",
        "observationAbout": "",
        "source": {
                    "@type": "WebAPI",
                    "url": "https://someapi.com",
                    "name": "data scraper"
                    },
        "instrument": "",
        "agent": ""
    }
}

```




### HTML

thing.html.xxx return html formats of the thing

print(thing.html.__doc__) for full list

- record() : returns dict with enhanced values (link, etc)
- full() : Returns a 2 column table with key / values
- card() : returns a card
- media() : returns the media (video or pic)
- video() : returns video
- image() : returns image
- link () : returns link with internal value
- record_ref(): returns link with record_ref


### Using api

```
# Set url for the api (only has to do it once)
t = Thing()
t.set_api_url('https://api_url.com')

# Save record tp api
t = Thing('test', 'abc1234')
t.url = 'https://www.test.com'
t.api_post()


# Load record from api
t.api_get()

print(t)

```


## Attributes



## Methods


