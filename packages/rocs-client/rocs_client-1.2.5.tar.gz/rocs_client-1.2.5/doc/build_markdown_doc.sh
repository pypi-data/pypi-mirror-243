FILE_FULL_PATH=$0
FILE_NAME=${FILE_FULL_PATH##*/}
FILE_PATH=$(find -name "$FILE_NAME" | awk '{print $1}')
cd $(dirname "$FILE_PATH")

rm -rf source
rm -rf build

mkdir build
mkdir source

cp conf.py ./source/
cp index.rst ./source/

sphinx-apidoc -o source ../
make dirhtml
make markdown