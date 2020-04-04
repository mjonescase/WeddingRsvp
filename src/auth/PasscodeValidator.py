import hashlib


def hash_passcode(passcode: str) -> str:
    return hashlib.sha256(passcode.encode('utf-8')).hexdigest()


class PasscodeValidator:
    _hashed_passcode: str
    
    def __init__(self, hashed_passcode: str):
        self._hashed_passcode = hashed_passcode

    def is_valid_passcode(self, passcode: str) -> bool:
        return self._hashed_passcode == hash_passcode(passcode.lower())
        
    
