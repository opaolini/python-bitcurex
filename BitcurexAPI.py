import math
import time
import simplejson
import urllib
import urllib2
import hmac,hashlib
__version__ = '0.0.1'
def microtime():
  """
  Returns current Unix timestamp with microseconds

  """
  return '%f %d' % math.modf(time.time())

class BitcurexAPI(object):
  """
  API PLN

  API umozliwia kontrole wlasnego konta, poprzez zewnetrzne aplikacje, napisane przez uzytkownikow (np. boty transakcyjne). API posiada adres: https://pln.bitcurex.com/api/0/
  
  API publiczne
  
  https://pln.bitcurex.com/data/orderbook.json
  lista biezacych ofert kupna i sprzedazy
  
  https://pln.bitcurex.com/data/trades.json
  lista transakcji z ostatnich 3 dni
  
  https://pln.bitcurex.com/data/ticker.json
  stan rynku: ticker
  
  Metody prywatnego API
  
  getFunds - pobiera aktualne saldo dostepne konta i adres zasilen BTC
  POST: nonce=#, zwrot: plns, btcs, address
  
  getOrders - pobiera aktualnie zlozone oferty i saldo
  POST: nonce=#, zwrot: plns, btcs, orders
  
  buyBTC - ustawia zlecenie skupu BTC (BID)
  POST: nonce=#&amount=#&price=#, zwrot: plns, btcs, orders
  
  sellBTC - ustawia zlecenie sprzedazy BTC (ASK)
  POST: nonce=#&amount=#&price=#, zwrot: plns, btcs, orders
  
  cancelOrder - usuwa zlecenie kupna / sprzedazy
  POST: nonce=#&oid=#&type=#, zwrot: plns, btcs, orders
  
  getTransactions - zwraca liste ostatnich 100 transakcji wlasnych
  POST: nonce=#&oid=#&type=#, zwrot: plns, btcs, transactions
  
  withdraw - zleca wyplate BTC/PLN na wskazane w systemie konto
  POST: nonce=#&type=#amount=#, zwrot: plns, btcs
  
  Legenda
  
  plns - ilosc PLN
  btcs - ilosc BTC
  address - adres do zasilen Bitcoin
  orders - oferty, zawieraja: oid, amount, price, type (1=ASK, 2=BID)
  oid - identyfikator oferty
  amount - ilosc BTC (lub PLN przy withdraw)
  price - cena PLN
  type - BTC lub PLN (typ wyplaty)

  """


  _api_key = None
  _api_secret = None
  _api_base = 'https://pln.bitcurex.com/api/0/'

  def __init__(self, api_key, api_secret):
    self._api_key = api_key
    self._api_secret = api_secret
  
  
  def _query(self, path, data={} ):
    """
    Queries BitCurex API endpoints
    """
    mt = microtime().split()
    nonce = mt[1] + mt[0][2:]
    data['nonce'] = nonce
    post_data = urllib.urlencode( data )
    sign = hmac.new( self._api_secret.decode('base64'), post_data, hashlib.sha512 ).digest()
    headers = {'Rest-Key' : self._api_key,
               'Rest-Sign': sign.encode('base64').strip().replace('\n',''), #Fix newline
               'User-Agent' : '%s python-bitcurex' % (__version__),
                'Content-type': 'application/x-www-form-urlencoded'}
    url = self._api_base + path
    req = urllib2.Request( url, post_data, headers )
    response = urllib2.urlopen(req)
    return simplejson.loads(response.read())
  
  def getFunds(self):

    return self._query('getFunds')

  def getOrders(self):

    return self._query('getOrders')

  def buyBTC(self,amount,price):

    return self._query('buyBTC',{'amount':amount,'price':price})

  def sellBTC(self,amount,price):

    return self._query('sellBTC',{'amount':amount,'price':price})

  def cancelOrder(self,oid,Type):

    return self._query('cancelOrder',{'Type':Type.upper(),'oid':oid})

  def getTransactions(self,Type):

    return self._query('getTransactions',{'type' : Type.upper()})

  def withdraw(self,Type,amount):

    return self._query('withdraw',{'type' :Type.upper(),'amount':amount})


