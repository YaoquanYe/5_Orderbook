import web_auth_helper

SECRET = 'HappyNewYear'

Apikey = 'zFcjUaFfDs4ckUyof5dcY0wRxNQOIu7OOrTaLLChv4PnWuH2aI0krrK46JlzERYp'
ApiSecret = '4Nf6QZcnDCr4Ir6PhhbKM4ylc7HN2fEfjMpSgge2AC4NersIG4zKhVp8h5VuHMSZ'

# The encoded message.
Apikey_encoded = web_auth_helper.encode(Apikey, SECRET)
ApiSecret_encoded = web_auth_helper.encode(ApiSecret, SECRET)