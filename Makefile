all: lib test

test: lib
	$(CC) -L. -led25519 test.c -o test -Isrc/ed25519_orlp/csrc
	./test

clean:
	rm -f *.so *.o test

lib:
	$(CC) -shared -o libed25519.so -Isrc/ed25519_orlp/csrc src/ed25519_orlp/csrc/*.c
