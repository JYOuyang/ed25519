import os
import sys
import glob
from ctypes import cdll, create_string_buffer
import secrets

def _load_lib():
    # Try to find the compiled library in the package directory
    pkg_dir = os.path.dirname(__file__)

    # Look for the library with various possible names
    patterns = [
        "libed25519.so",
        "libed25519.dylib",
        "libed25519*.so",
        "libed25519*.pyd",
    ]

    for pattern in patterns:
        matches = glob.glob(os.path.join(pkg_dir, pattern))
        if matches:
            try:
                return cdll.LoadLibrary(matches[0])
            except OSError:
                continue

    # Fallback for local development/manual build
    try:
        return cdll.LoadLibrary("libed25519.so")
    except OSError:
        pass

    raise ImportError("Could not find the ed25519 shared library. Please ensure the package is correctly installed.")

cl = _load_lib()

def gen_seed() -> bytes:
    return secrets.token_bytes(32)

def ed25519_create_keypair(seed: bytes | None = None) -> (bytes, bytes, bytes):
    pubkey = create_string_buffer(32)
    prvkey = create_string_buffer(64)
    if not seed or len(seed) != 32 or all(b == 0 for b in seed):
        seed = gen_seed()
    
    cl.ed25519_create_keypair(pubkey, prvkey, seed)
    return (bytes(pubkey), bytes(prvkey), bytes(seed))

def ed25519_sign(message: bytes, pubkey: bytes, prvkey: bytes) -> bytes:
    sig = create_string_buffer(64)
    cl.ed25519_sign(sig, message, len(message), pubkey, prvkey)
    return bytes(sig)

def ed25519_verify(signature: bytes, message: bytes, pubkey: bytes) -> bool:
    return cl.ed25519_verify(signature, message, len(message), pubkey) == 1

def ed25519_key_exchange(pubkey: bytes, prvkey: bytes) -> bytes:
    secret = create_string_buffer(32)
    cl.ed25519_key_exchange(secret, pubkey, prvkey)
    return bytes(secret)
