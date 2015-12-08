#!/bin/bash

scl=eclipse-neon
base_release=24
base_branch=master
base_root=fedora-rawhide-x86_64

function set_release {
	if [ "$base_release" != "$1" ] ; then
		base_release=$1
		base_branch=f$1
		base_root=fedora-$1-x86_64
	fi
}
