test:	nosetest

test-failures:	nosetest-ipdb-failures

clear-screen:
	@clear

run-nosetest:
	nosetests --ipdb --with-yanc --with-coverage --cover-package outputty \
	          tests/test_*.py

run-nosetest-ipdb-failures:
	nosetests --ipdb-failures --with-yanc --with-coverage \
	          --cover-package outputty tests/test_*.py

run-unittest:
	python -m unittest discover -s tests

nosetest:  clear-screen clean run-nosetest

nosetest-ipdb-failures:  clear-screen clean run-nosetest-ipdb-failures

unittest:  clear-screen clean run-unittest

clean:
	find -regex '.*\.pyc' -exec rm {} \;
	find -regex '.*~' -exec rm {} \;
	rm -rf reg-settings.py
	rm -rf examples/my-data.csv examples/nice-software.html examples/nice-software.txt
	rm -rf readme.html tutorial.html
	rm -rf MANIFEST dist

before-push:	clean test create-docs html-docs

create-docs:
	./create-docs.py

html-docs:
	markdown README.markdown > readme.html
	markdown tutorial.markdown > tutorial.html

pack:
	python setup.py sdist

.PHONY: test clear-screen nosetest unittest clean run-unittest run-nosetest \
        test-failures nosetest-ipdb-failures run-nosetest-ipdb-failures \
	before-push create-docs html-docs pack
