test:	nosetest

test_failures:	nosetest_ipdb_failures

clear_screen:
	@clear

run_nosetest:
	nosetests --ipdb --with-yanc --with-coverage --cover-package outputty \
	          tests/test_*.py

run_nosetest_ipdb_failures:
	nosetests --ipdb-failures --with-yanc --with-coverage \
	          --cover-package outputty tests/test_*.py

run_unittest:
	python -m unittest discover -s tests

nosetest:  clear_screen clean run_nosetest

nosetest_ipdb_failures:  clear_screen clean run_nosetest_ipdb_failures

unittest:  clear_screen clean run_unittest

clean:
	find -regex '.*\.pyc' -exec rm {} \;
	find -regex '.*~' -exec rm {} \;

.PHONY: test clear_screen nosetest unittest clean run_unittest run_nosetest \
        test_failures nosetest_ipdb_failures run_nosetest_ipdb_failures
