test:	
	@clear
	nosetests --with-coverage tests/test_*.py

clean:
	find -regex '.*\.pyc' -exec rm {} \;

.PHONY: test clean
