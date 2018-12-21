all:
	g++  -o togmus togmus.cpp -lz
	cd muser2-dir/src/tools/muser2 && $(MAKE)
	cp muser2-dir/src/tools/muser2/muser2 .
clean:
	cd muser2-dir/src/tools/muser2 && $(MAKE) clean
	rm togmus
	rm muser2
