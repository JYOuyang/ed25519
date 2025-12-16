all: lib test

test: lib
	$(CC) -L. -led25519 test.c -o test
	./test

clean:
	rm -f *.so *.o

lib:
	$(CC) -shared -o libed25519.so -Isrc src/*.c
