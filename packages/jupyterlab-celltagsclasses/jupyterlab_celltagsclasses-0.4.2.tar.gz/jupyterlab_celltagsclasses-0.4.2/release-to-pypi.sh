#!/bin/bash

echo "----- checking for required python packages"
for pkg in build twine hatch; do
    pip show $pkg >& /dev/null || pip install $pkg
done

echo "----- Current version is: $(hatch version)"

# if CHANGELOG.md is found, let us display
# its differences
if [ -f CHANGELOG.md ]; then
    echo "----- diffs in CHANGELOG.md"
    git diff CHANGELOG.md
fi

# prompt user for version number
echo -n "----- Enter new version number: "
read version

# hatch has the nasty effect of reformatting package.json
#hatch version $version
echo "----- bumping version to $version"
sed -i.version -e 's/\("version": "\)[^"]*/\1'$version'/' package.json

echo "----- diffing package.json"
git diff package.json
echo -n "want to go on ? (ctrl-c to abort)"
read answer

# commit and tag
# do it early so life can go on before the build is done
echo "----- committing and tagging"
git add package.json
git commit -m "release $version"
git tag "v$version"

echo "----- cleaning dist/, and rebuilding"
rm -rf dist/*
python -m build

echo -n "publish to pypi (ctrl-c to abort) ? "
python -m twine upload dist/*
