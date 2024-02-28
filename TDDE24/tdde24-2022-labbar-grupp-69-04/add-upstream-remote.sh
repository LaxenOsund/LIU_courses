#!/bin/bash

# Detta script uppdaterar det lokala Git-arkivet med eventuella
# ändringar som har gjorts "centralt", i upstream-arkivet, efter att
# ditt eget arkiv skapades.  Om du behöver köra scriptet kommer vi att
# säga till!

# Exit script upon failure
set -e

# Is the upstream already set? If not, add it.
# The upstream is the base repo that this archive was originally
# forked from.
git config remote.upstream.url || git remote add upstream git@gitlab.liu.se:tdde23-24/python-tdde24-base.git

# Update from the "upstream" repo defined above
git checkout main
git fetch upstream

# Don't start an editor to edit a merge message.
# Too confusing and not so meaningful in this case.
git pull upstream main --no-edit

# Push updates to gitlab
git push origin main

