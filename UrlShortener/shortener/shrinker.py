from .models import URL, AdminConfig

from math import floor, ceil

import urllib
import hashlib


constRatio = 0.671795116

def ConvertToBase62(n):
    adminConfig = AdminConfig.objects.get(pk=1)
    
    _ALPHABET = []
    if adminConfig.allow_digits:
        for i in range(10):
            _ALPHABET.append(chr(ord('0') + i))
    if adminConfig.allow_uppercase:
        for i in range(26):
            _ALPHABET.append(chr(ord('A') + i))
    if adminConfig.allow_lowercase:
        for i in range(26):
            _ALPHABET.append(chr(ord('a') + i))

    base = len(_ALPHABET)
    
    s = ""
    while n > 0:
        r = n % base
        s += _ALPHABET[r]
        n //= base

    if len(s) > adminConfig.max_url_length:
        s = s[:adminConfig.max_url_length]
        
    return s
    
def shrink(url):
    adminConfig = AdminConfig.objects.get(pk=1)

    hashed = hashlib.md5(url.encode('utf-8'))
    hexdig = hashed.hexdigest()

    size = len(hexdig) // 3 + 2
    size = min(size, ceil(adminConfig.max_url_length / constRatio))
    size = max(size, floor(adminConfig.min_url_length / constRatio))
    
    chunck1 = int(hexdig[:size], 16)
    chunck2 = int(hexdig[size:min(size * 2, len(hexdig))], 16)
    chunck3 = int(hexdig[size * 2:min(size * 3, len(hexdig))], 16)
    xor = chunck1 ^ chunck2 ^ chunck3

    shortenedURL = ConvertToBase62(xor)

    shortenedURL = adminConfig.myDomain + adminConfig.prefix + shortenedURL + adminConfig.suffix
    
    return shortenedURL
