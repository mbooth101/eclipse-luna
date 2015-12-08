#!/usr/bin/bash

#
# This script builds a package for the SCL named below
#
# Should be run from a cloned dist-git repo of a package (instead of "fedpkg build")
#

script_dir="$( (cd $(dirname $(readlink -f "$0")) && pwd) )"
source $script_dir/scl_config.sh

if [ $# -ge 1 ] ; then
	set_release $1
fi

# Get the NVR of the package
VERREL=$(fedpkg --dist f$base_release verrel 2>/dev/null | grep $(basename $(pwd)))
VERREL=$(echo $VERREL | sed -e "s/^eclipse-metapackage/$scl/")

# Generate an SRPM
fedpkg --dist f$base_release srpm 2>/dev/null

# Build
mock -r $base_root --no-clean --no-cleanup-after --rebuild ${VERREL}.src.rpm

