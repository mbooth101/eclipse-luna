#!/usr/bin/bash
set -e

#
# This script builds a package for the SCL named below
#
# Should be run from a cloned dist-git repo of a package (instead of "fedpkg build")
#

# Name of the collection we are building for
COLLECTION=eclipse-mars

# Set some build-time macros for the SCL
BUILD_MACRO_FILE=macros.eclipse-metapackage-config
echo "%scl $COLLECTION" > $BUILD_MACRO_FILE
echo "%scl_vendor rh" >> $BUILD_MACRO_FILE
sudo mv $BUILD_MACRO_FILE /etc/rpm/$BUILD_MACRO_FILE

# Get an NVR with the SCL name prefixed
VERREL=$(fedpkg --dist f21 verrel 2>/dev/null | grep $(basename $(pwd)))
VERREL=${VERREL#eclipse-metapackage-}
VERREL=$COLLECTION-${VERREL#$COLLECTION-}

# Generate an SRPM
fedpkg --dist f21 srpm 2>/dev/null

# Remove macros
sudo rm /etc/rpm/$BUILD_MACRO_FILE

# Upload and build
mock -r $COLLECTION --no-clean --no-cleanup-after --rebuild ${VERREL}.src.rpm

