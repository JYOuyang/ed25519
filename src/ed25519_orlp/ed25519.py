"""Python wrapper for Orson Peters' Ed25519 implementation.

This library is intended only for situations where interoperability with
keys generated from the original library is required (or the Node
package @noble/ed25519, which uses a WASM compilation of it).

Peters' private key representation is not compatible with that used by
more modern implementations; loosely speaking, the orlp keys are the
output of a sha512 operation from what modern approaches use, so it can't
be converted.

If you need ed25119 for any other purpose, consider pynacl.
"""

from pathlib import Path
from ctypes import cdll, create_string_buffer
import secrets


def _load_lib():
    """Locate and load the ed25519 shared library."""
    # Try to find the compiled library in the package directory
    pkg_dir = Path(__file__).parent

    # Look for the library with various possible names
    patterns = [
        "libed25519.so",
        "libed25519.dylib",
        "libed25519*.so",
        "libed25519*.pyd",
    ]

    for pattern in patterns:
        for match in pkg_dir.glob(pattern):
            try:
                return cdll.LoadLibrary(str(match))
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
    """Generate a random 32-byte seed."""
    return secrets.token_bytes(32)


def ed25519_create_keypair(seed: bytes | None = None) -> tuple[bytes, bytes, bytes]:
    """
    Create a new ed25519 keypair.

    Args:
        seed: An optional 32-byte random seed.  If not supplied,
            a random seed will be generated.

    Returns:
        A tuple of (public_key, private_key, seed), where:
        - public_key is 32 bytes
        - private_key is 64 bytes
        - seed is 32 bytes

        If you need keypairs generated with this library to work
        in any other ed25519 implementation, you should preserve
        the seed; the keypair alone is not compatible with any
        more modern implementation and the private key cannot
        be converted to a modern form.  However, the seed should
        work with modern libraries like pynacl.
    """
    pubkey = create_string_buffer(32)
    prvkey = create_string_buffer(64)
    if not seed:
        seed = gen_seed()
    if seed and len(seed) != 32:
        raise ValueError("Seed must be exactly 32 bytes")

    cl.ed25519_create_keypair(pubkey, prvkey, seed)
    return (bytes(pubkey), bytes(prvkey), bytes(seed))


def ed25519_sign(message: bytes, pubkey: bytes, prvkey: bytes) -> bytes:
    """
    Sign a message using the provided public and private keys.

    Args:
        message: The message to be signed (bytes).
        pubkey: The 32-byte public key.
        prvkey: The 64-byte private key.

    Returns:
        A 64-byte signature.
    """
    sig = create_string_buffer(64)
    cl.ed25519_sign(sig, message, len(message), pubkey, prvkey)
    return bytes(sig)


def ed25519_verify(signature: bytes, message: bytes, pubkey: bytes) -> bool:
    """
    Verify a signature for a message using a public key.

    Args:
        signature: The 64-byte signature to verify.
        message: The message that was signed (bytes).
        pubkey: The 32-byte public key of the signer.

    Returns:
        True if the signature is valid, False otherwise.
    """
    return cl.ed25519_verify(signature, message, len(message), pubkey) == 1


def ed25519_key_exchange(pubkey: bytes, prvkey: bytes) -> bytes:
    """
    Perform a key exchange to produce a shared secret.

    Args:
        pubkey: The 32-byte public key of the other party.
        prvkey: Your own 64-byte private key.

    Returns:
        A 32-byte shared secret.
    """
    secret = create_string_buffer(32)
    cl.ed25519_key_exchange(secret, pubkey, prvkey)
    return bytes(secret)
