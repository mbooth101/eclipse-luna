#!/usr/bin/bash
set -e

#
# This script builds a package for the Eclipse Luna SCL
#
# Should be run from a cloned dist-git repo of a package (instead of "fedpkg build")
#

echo "%scl eclipse-luna" > macros.eclipse-luna-config
echo "%scl_vendor rh" >> macros.eclipse-luna-config
sudo mv macros.eclipse-luna-config /etc/rpm/macros.eclipse-luna-config

# Get an NVR with the SCL name prefixed
VERREL=$(fedpkg --dist f21 verrel 2>/dev/null | grep $(basename $(pwd)))
VERREL=eclipse-luna-${VERREL#eclipse-luna-}

# Generate an SRPM
fedpkg --dist f21 srpm 2>/dev/null

# Upload and build
scp ${VERREL}.src.rpm ${USER}@fedorapeople.org:~/public_html/copr/.
copr-cli build --nowait "mbooth/eclipse-luna" http://${USER}.fedorapeople.org/copr/${VERREL}.src.rpm

sudo rm /etc/rpm/macros.eclipse-luna-config
