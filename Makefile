ONLY=*
TEST_RUNNER=nosetests --with-coverage --cover-package outputty

# `make test` will execute:
#  nosetests --with-coverage tests.test_*
#
# `make test ONLY=Table_csv TEST_RUNNER='python -m unittest'` will execute:
#  python -m unittest tests.test_Table_csv

test:	
	@clear
	${TEST_RUNNER} tests.test_${ONLY}

clean:
	find -regex '.*\.pyc' -exec rm {} \;

.PHONY: test clean
