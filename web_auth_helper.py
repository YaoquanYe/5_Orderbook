import base64
import hmac
import pickle

class DecodeException(Exception):
    def __init__(self, value="Decode failed."):
        self.value = value

    def __str__(self):
        return repr(self.value)

def encode(object_to_encode, key):
    serialized_obj_str = pickle.dumps(object_to_encode)
    hmac_obj = hmac.new(key, msg=serialized_obj_str)
    signed_request = base64.b64encode(hmac_obj.digest()) + '.' + \
                     base64.b64encode(serialized_obj_str)
    return signed_request

def decode(signed_request, key):
    # Split the signature and the data.
    try:
        sig, payload = signed_request.split('.', 1)
    except ValueError:
        raise DecodeException()
    
    # Decode the data back as serialized object.
    try:
        decoded_obj_str = base64.b64decode(payload)
    except TypeError:
        raise DecodeException()
    
    # Get the signature generated using the serialized object and
    # the key.
    expected_sig = base64.b64encode(hmac.new(key, msg=decoded_obj_str).digest())
    
    # If both the signatures matches.
    if sig == expected_sig:
        try:
            return pickle.loads(decoded_obj_str)
        except:
            raise DecodeException()
    # The signatures doesn't match.
    else:
        raise DecodeException()