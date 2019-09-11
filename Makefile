static:
	g++ --static -o togmus togmus.cpp -lz
	cd muser2-dir/src/wraps && $(MAKE) -j4
	cd muser2-dir/src/clset && $(MAKE) -j4
	cd muser2-dir/src/wraps-2 && $(MAKE) -j4
	cd muser2-dir/src/tools/muser2 && CPPFLAGS="--static" $(MAKE)

all:
	g++  -o togmus togmus.cpp -lz
	cd muser2-dir/src/wraps && $(MAKE) -j4
	cd muser2-dir/src/clset && $(MAKE) -j4
	cd muser2-dir/src/wraps-2 && $(MAKE) -j4
	cd muser2-dir/src/tools/muser2 && $(MAKE) -j4
clean:
	cd muser2-dir/src/wraps && $(MAKE) clean
	cd muser2-dir/src/clset && $(MAKE) clean
	cd muser2-dir/src/wraps-2 && $(MAKE) clean
	cd muser2-dir/src/tools/muser2 && $(MAKE) clean
	find . -type f -name *.o -delete
	find . -type f -name *.so -delete
	find . -type f -name *.a -delete
	rm -f muser2-dir/src/tools/muser2/muser2
	rm -f togmus
	rm -f muser2
