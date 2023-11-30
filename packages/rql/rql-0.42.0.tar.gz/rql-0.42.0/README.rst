This package provides base library for the Relationship Query Language

INSTALL
-------

the standard way:

python setup.py install

building rql binary extension in place:

python setup.py build_ext --inplace

DOCUMENTATION
-------------

Documentation is available at https://rql.readthedocs.io

HOW TO RELEASE?
---------------

Bump version number in __pkginfo__.py, then update the debian changelog with::

	dch -v <version>-1 -D unstable

Commit with ``hg commit -m "[pkg] Version <version>"`` and tag with ``hg tag
<version> debian/<version>-1``.

Ensure you have a clean working directory before upload to pypi by running
``hg clean --all --dirs --files`` (warning: this will remove all untracked
files).

Generate the source distribution with ``python3 setup.py sdist``.

rql has a faster implementation using libgecode. To make this available to
users using pip and not having libgecode installed, we publish manylinux
wheels to pypi.

To build a manylinux package for rql we use quay.io/pypa/manylinux1_x86_64
docker image and a custom script `build_wheel.sh` so you just have to execute
it and it will pull docker image and execute script in this image ::

	docker pull quay.io/pypa/manylinux_2_24_x86_64
	./build_wheel.sh

Then upload source dist and wheels to pypi using twine::

	twine upload dist/*.tar.gz dist/*.whl
