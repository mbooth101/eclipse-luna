#!/bin/bash

# This script naïvely adds some SCL-isation to a spec file

SPEC=$(ls *.spec)

N=$(rpmspec --srpm $SPEC -q --queryformat "%{N}")

sed -i \
  -e "1i%{?scl:%scl_package $N}\n%{!?scl:%global pkg_name %{name}}\n" \
  -e "/^Name:/ s|$N|%{?scl_prefix}$N|" \
  -e "/^\(URL:\|Source[0-9]*:\|Patch[0-9]*:\)/ s|%{name}|%{pkg_name}|g" \
  -e "/^%\(setup\|autosetup\)/ s|%{name}|%{pkg_name}|g" \
  $SPEC

rpmdev-bumpspec -r -c "SCL-ise" $SPEC
