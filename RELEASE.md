How to make a release
=====================

Merge in all the changes, make sure master is happy and the current working
directory clean.

Bump the version in raven-cron/version.py following
[semver](http://semver.org). Let's call it $NEW_VERSION.

Run `git changelog` from the git-extras package to update the changelog.
Format accordingly and set the $NEW_VERSION.

Then make a commit called "Release v$NEW_VERSION"
And `git tag v$NEW_VERSION`

Run `git push && git push --tags`

run `make release`

