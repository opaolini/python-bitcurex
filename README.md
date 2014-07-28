python-bitcurex
===============

Python wrapper for Bitcurex.pl's bitcoin exchange API

Example Usage
===============
```python
import BitcurexAPI

API_KEY ='Your key'
API_SECRET = 'Your secret'

conn = BitcurexAPI.BitcurexAPI(API_KEY, API_SECRET)

conn.getFunds()
```