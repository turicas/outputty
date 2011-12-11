test:	nosetest

clear_screen:
		@clear

run_nosetest:
		nosetests --with-coverage --cover-package outputty tests/test_*.py

run_unittest:
		python -m unittest discover -s tests

nosetest:  clear_screen clean run_nosetest

unittest:  clear_screen clean run_unittest

clean:
		find -regex '.*\.pyc' -exec rm {} \;
			find -regex '.*~' -exec rm {} \;

.PHONY: test clear_screen nosetest unittest clean run_unittest run_nosetest
