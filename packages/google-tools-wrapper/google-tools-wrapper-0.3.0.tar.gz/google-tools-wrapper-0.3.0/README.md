# An unofficial Google Tools wrapper

## GoogleTools

This library provides a simple interface for accessing Google features.

### Installation
```bash
pip install google-tools-wrapper==0.3.0
```

## Currency Conversion Usage
```python
from google_tools import GoogleTools as tools

# `only_float=True`
>>> result = tools.currency_conversion(base_currency='USD', target_currency='BRL')
>>> print(result)
4.9024

# `only_float=False`
>>> result = tools.currency_conversion(base_currency='USD', target_currency='BRL', only_float=False)
>>> print(result) # don't looks like it on terminal, just prettyfied it
{
    'conversion': [
        '1 USD',
        '4.90 BRL'
    ],
    'float': 4.9024,
    'last_update': 'Nov 25, 4:38:00 PM UTC'
}
```

## Translater Usage
```python
from google_tools import GoogleTools as tools

>>> result = tools.translater(source_language='pt', target_language='en', text='Olá Mundo!')
>>> print(result) # maybe it take around 5-10 seconds to respond, depends on your cpu, selenium is a bit slow '-'
Hello World!
```

### Disclaimer
This library is provided for educational purposes only and should not be used in production environments. It is not affiliated with Google and may not always provide accurate or up-to-date currency conversion rates. For real-time currency conversion services, please refer to official financial sources.
