#!/bin/sh

# Test this script locally as follows (rerun `docker pull simgrid/unstable` to get a fresh version).
# cd (simgrid)/tools/jenkins
# docker run -it --rm --volume `pwd`:/source simgrid/unstable /source/ci-bigdft.sh

set -ex

echo "XXXXXXXXXXXXXXXX Install APT dependencies"
SUDO="" # to ease the local testing
$SUDO apt-get -y update
$SUDO apt-get -y install python-is-python3 python3-setuptools libboost-dev libeigen3-dev
$SUDO apt-get -y install --only-upgrade ca-certificates

echo "XXXXXXXXXXXXXXXX build and test BigDFT (git version)"
git clone --depth=1 https://gitlab.com/l_sim/bigdft-suite.git
cd bigdft-suite

WORKSPACE=$PWD
mkdir build && cd build
export PATH=$PWD/simgrid-dev/smpi_script/bin/:$PATH
export LD_LIBRARY_PATH=$PWD/simgrid-dev/lib/:$LD_LIBRARY_PATH
export JHBUILD_RUN_AS_ROOT=1

#workaround issue with ntpoly 3.0.0
sed -i 's|repository type="tarball" name="ntpoly" href="https://github.com/william-dawson/NTPoly/archive/"|repository type="git" name="ntpoly" href="https://github.com/william-dawson/"|' ../modulesets/hpc-upstream.modules
sed -i 's|module="ntpoly-v3.0.0.tar.gz"|module="ntpoly"|' ../modulesets/hpc-upstream.modules

../Installer.py autogen -y

../Installer.py -f ../../tools/jenkins/gfortran-simgrid.rc -y build

export OMP_NUM_THREADS=1
#workaround issue with profiling optimization (for fugaku) which prevent f_free_ptr to use the simgrid version. Fix pending.
export FUTILE_PROFILING_DEPTH=-1

#cubic version
cd ../bigdft/tests/DFT/cubic/C
smpirun -hostfile $WORKSPACE/simgrid-dev/examples/smpi/hostfile -platform $WORKSPACE/simgrid-dev/examples/platforms/small_platform.xml -np 8 $WORKSPACE/build/install/bin/bigdft -l no

#Psolver checking with smpi_shared_malloc
cd $WORKSPACE/build/psolver/tests
make FC=smpif90 PS_Check
smpirun -hostfile $WORKSPACE/simgrid-dev/examples/smpi/hostfile -platform $WORKSPACE/simgrid-dev/examples/platforms/small_platform.xml -np 4 ./PS_Check -n [57,48,63] -g F

#linear scaling version (heavy, might swap)
cd $WORKSPACE/bigdft/tests/DFT/linear/surface
smpirun -hostfile $WORKSPACE/simgrid-dev/examples/smpi/hostfile -platform $WORKSPACE/simgrid-dev/examples/platforms/small_platform.xml -np 4 $WORKSPACE/build/install/bin/bigdft -n graphene -l no

cd $WORKSPACE/build
../Installer.py -f ../../tools/jenkins/gfortran-simgrid.rc -y clean
