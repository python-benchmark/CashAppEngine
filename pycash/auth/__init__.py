    
def generate_key(token, token_key):
    import hashlib
    from datetime import datetime
    today = datetime.utcnow()
    value = token+':'+token_key+':'+today.strftime('%Y%j%H%M')
    return hashlib.sha256(value).hexdigest()