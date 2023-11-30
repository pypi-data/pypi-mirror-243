#!/bin/sh

set -ex

[ "$CI_PROJECT_DIR" ] && SOURCE_DIR="$CI_PROJECT_DIR" || SOURCE_DIR="/mnt/host/RQL"

mkdir -p dist
if ! test -e /.dockerenv && [ ! "$GITLAB_CI" ] ; then
  exec docker run --rm -it -v "$(pwd)":"$SOURCE_DIR" quay.io/pypa/manylinux_2_24_x86_64 sh "$SOURCE_DIR"/"$0"
fi

cd "$SOURCE_DIR"
VERSION=6.2.0

curl -L https://github.com/Gecode/gecode/archive/refs/tags/release-$VERSION.tar.gz | tar -xzf -

cd gecode-release-$VERSION
./configure --enable-examples=no --enable-flatzinc=no --enable-minimodel=no
make -j$(nproc)
make install

PYBINS="/opt/python/cp37*/bin /opt/python/cp38*/bin /opt/python/cp39*/bin"

mkdir -p /wheelhouse
# Compile wheels
for PYBIN in $PYBINS; do
    "${PYBIN}/pip" wheel "$SOURCE_DIR" -w /wheelhouse
done

# Bundle external shared libraries into the wheels
for whl in /wheelhouse/rql*.whl; do
    auditwheel repair "$whl" -w /wheelhouse
done

# Install packages and test
for PYBIN in $PYBINS; do
    "${PYBIN}/pip" install pytest
    "${PYBIN}/pip" install rql --no-index -f /wheelhouse
    echo "************  test on $PYBIN"
    (cd "$SOURCE_DIR"; "${PYBIN}/pytest" test)
done
mv /wheelhouse/rql*manylinux*.whl "$SOURCE_DIR"/dist/
