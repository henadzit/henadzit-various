require 'httpclient'

http = HTTPClient.new
http.get('http://test.com:8000')
