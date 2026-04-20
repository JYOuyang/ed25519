all: lib test

test: lib
	$(warning NOTE: this is the original orlp C test, not the python module tests)
	$(CC) -L. -led25519 test.c -o test -Isrc/ed25519_orlp/csrc
	./test

clean:
	rm -f *.so *.o test

lib:
	$(CC) -shared -o libed25519.so -Isrc/ed25519_orlp/csrc src/ed25519_orlp/csrc/*.c
