#!/bin/bash

USAGE="Usage: ./release-to-pypi.sh [-s] [-v version]"
# -s: skip the check for required python packages
# -v: provide the version number on the command line

SKIP_REQS=
VERSION=

while getopts "sv:" opt; do
    case $opt in
        s)
            SKIP_REQS=1 ;;
        v)
            VERSION=$OPTARG ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            echo $USAGE
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

if [[ -z "$SKIP_REQS" ]]; then
    echo "----- checking for required python packages"
    for pkg in build twine hatch; do
        pip show $pkg >& /dev/null || pip install $pkg
    done
fi

echo "----- Current version is: $(hatch version)"

# if CHANGELOG.md is found, let us display
# its differences
if [ -f CHANGELOG.md ]; then
    echo "----- diffs in CHANGELOG.md"
    git diff CHANGELOG.md
fi

# prompt user for version number
if [[ -z "$VERSION" ]]; then
    echo -n "----- Enter new version number: "
    read version
else
    echo "----- Using version number $VERSION"
fi

# hatch has the nasty effect of reformatting package.json
#hatch version $VERSION
echo "----- bumping version to $VERSION"
sed -i.version -e 's/\("version": "\)[^"]*/\1'$VERSION'/' package.json

echo "----- diffing package.json"
git diff package.json
echo -n "want to go on ? (ctrl-c to abort)"
read answer

# commit and tag
# do it early so life can go on before the build is done
echo "----- committing and tagging"
git add package.json
git commit -m "release $VERSION"
git tag "v$VERSION"

echo "----- cleaning dist/, and rebuilding"
jlpm clean:labextension
rm -rf dist/*
python -m build

echo -n "publish to pypi (ctrl-c to abort) ? "
read answer
python -m twine upload dist/*
