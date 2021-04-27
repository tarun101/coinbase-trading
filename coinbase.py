import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase


# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
	def __init__(self, api_key, secret_key, passphrase):
		self.api_key = api_key
		self.secret_key = secret_key
		self.passphrase = passphrase

	def __call__(self, request):
		timestamp = str(time.time())
		message = timestamp + request.method + request.path_url + (request.body or
																																																													b'').decode()
		hmac_key = base64.b64decode(self.secret_key)
		signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
		signature_b64 = base64.b64encode(signature.digest()).decode()

		request.headers.update({
			'CB-ACCESS-SIGN': signature_b64,
			'CB-ACCESS-TIMESTAMP': timestamp,
			'CB-ACCESS-KEY': self.api_key,
			'CB-ACCESS-PASSPHRASE': self.passphrase,
			'Content-Type': 'application/json'
		})
		return request


API_KEY = "d351638823e15ddb8a01fc6f9d476f53"
API_SECRET = "oGzWPTxcvwxC9z5+9xOxYQpBz1mWkZxsj01yE0LjzZn9ftOALfI/USR58G0TtQj9/Sr+kiYGP+PgxeXN9OdDTQ=="
API_PASS = "1chib7ilyp7"
api_url = 'https://api.pro.coinbase.com/'
auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)

r = requests.get("https://api.pro.coinbase.com/products/BTC-USD/book").json()
price = round(0.95 * float(r.get("bids")[0][0]), 2)
print (price)
size = round(500/(price),4)
print (size)
	
order = {
	'size': size,
	'price': price,
	'side': 'buy',
	'product_id': 'BTC-USD'
}
r = requests.post(api_url + 'orders', json=order, auth=auth)
print(r.json())
