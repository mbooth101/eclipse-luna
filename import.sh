#!/bin/bash

script_dir="$( (cd $(dirname $(readlink -f "$0")) && pwd) )"
source $script_dir/scl_config.sh

if [ $# -ge 1 ] ; then
	scl_pkgs=( "$@" )
else
	if [ -e scl_pkgs ] ; then
		scl_pkgs=( $(cat scl_pkgs) )
	else
		echo "No packages specified on command line or in scl_pkgs file."
		exit 1
	fi
fi

function get_provides {
	# Generate a dnf configuration
	cat <<EOF >/tmp/$scl-dnf.conf
[main]
debuglevel=2
reposdir=/dev/null

[$scl]
name=$scl
baseurl=https://copr-be.cloud.fedoraproject.org/results/mbooth/$scl/$base_root/
skip_if_unavailable=True
gpgcheck=1
gpgkey=https://copr-be.cloud.fedoraproject.org/results/mbooth/$scl/pubkey.gpg
enabled=1
EOF
	# Interrogate dnf for provides
	dnf -c /tmp/$scl-dnf.conf clean all &>/dev/null
	dnf -c /tmp/$scl-dnf.conf repoquery --provides $scl-\* | \
		grep -v -e "^Last metadata expiration" | \
		grep -v -e "^Using metadata from" | \
		sed -e "s/^$scl-//" -e "s/ = .*$//" | sort | uniq
}

get_provides >/tmp/$scl-provides

for scl_pkg in "${scl_pkgs[@]}" ; do
	if [ ! -e ${scl_pkg} ] ; then
		git clone ssh://mbooth@pkgs.fedoraproject.org/${scl_pkg}.git ${scl_pkg}
	fi
	pushd ${scl_pkg} &>/dev/null
		if [ -z "$(git branch -a | grep -e "$scl$")" ] ; then
			# Create a branch for the SCL
			git checkout $base_branch
			git branch $scl
			git checkout $scl
			# SCL-ise
			$script_dir/spec2scl/try-spec2scl -i -l /tmp/$scl-provides -k "handle_configure_make" ${scl_pkg}.spec
			~/DTS_DEV/rpmdevtools/rpmdev-bumpspec -r -p -c "SCL-ise based on f$base_release branch" ${scl_pkg}.spec
			# Commit changes
			git add ${scl_pkg}.spec
			fedpkg --dist=f$base_release clog
			git commit -F clog
			rm clog
		else
			# Use existing branch for SCL
			git checkout $scl
		fi
		fedpkg --dist=f$base_release sources
	popd &>/dev/null
done
