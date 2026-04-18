import unittest
from ed25519_orlp.ed25519 import ed25519_create_keypair, ed25519_sign, ed25519_verify, ed25519_key_exchange

class TestEd25519(unittest.TestCase):
    def test_keypair_creation(self):
        pub, prv, seed = ed25519_create_keypair()
        self.assertEqual(len(pub), 32)
        self.assertEqual(len(prv), 64)
        self.assertEqual(len(seed), 32)

    def test_sign_and_verify(self):
        pub, prv, seed = ed25519_create_keypair()
        message = b'foo'
        sig = ed25519_sign(message, pub, prv)
        
        # Valid signature
        self.assertTrue(ed25519_verify(sig, message, pub))
        
        # Invalid message
        self.assertFalse(ed25519_verify(sig, b'bar', pub))
        
        # Invalid signature (modified)
        bad_sig = bytearray(bytes(sig))
        bad_sig[0] ^= 0xFF
        self.assertFalse(ed25519_verify(bytes(bad_sig), message, pub))

    def test_key_exchange(self):
        pub1, prv1, seed1 = ed25519_create_keypair()
        pub2, prv2, seed2 = ed25519_create_keypair()
        
        ss1 = ed25519_key_exchange(pub2, prv1)
        ss2 = ed25519_key_exchange(pub1, prv2)
        
        self.assertEqual(len(ss1), 32)
        self.assertEqual(bytes(ss1), bytes(ss2))

if __name__ == "__main__":
    unittest.main()
