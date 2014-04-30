#!/usr/bin/bash

VERREL=`fedpkg verrel 2>/dev/null`
fedpkg srpm 2>/dev/null

scp ${VERREL}.src.rpm ${USER}@fedorapeople.org:~/public_html/copr/.
copr-cli build --nowait eclipse-luna http://${USER}.fedorapeople.org/copr/${VERREL}.src.rpm

