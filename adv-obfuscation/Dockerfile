FROM gcc:10.3-buster

# package install list copied from Dockerfile in GHCC-master

RUN apt-get update && apt-get install -y build-essential

# Install necessary packages.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libboost-all-dev \
    python3.7 \
    ca-certificates \
    curl \
    python3-dev \
    libpython3.7-dev \
    less \
    vim \
    bmake \
    binutils-dev \
    bison \
    check \
    dialog \
    flex \
    flite1-dev \
    freeglut3-dev \
    guile-2.0-dev \
    lib3ds-dev \
    liba52-0.7.4-dev \
    libaa1-dev \
    libacl1-dev \
    libaio-dev \
    libao-dev \
    libargtable2-dev \
    libasound2-dev \
    libatlas-base-dev \
    libatm1-dev \
    libattr1-dev \
    libaubio-dev \
    libaudio-dev \
    libaudit-dev \
    libauparse-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavfilter-dev \
    libavresample-dev \
    libavutil-dev \
    libbam-dev \
    libbdd-dev \
    libbluetooth-dev \
    libbluray-dev \
    libboost-regex-dev \
    libboost-serialization-dev \
    libboost-system-dev \
    libboost-thread-dev \
    libbrlapi-dev \
    libbs2b-dev \
    libbsd-dev \
    libbtbb-dev \
    libbwa-dev \
    libcaca-dev \
    libcap-dev \
    libcap-ng-dev \
    libcdb-dev \
    libcdio-cdda-dev \
    libcdio-dev \
    libcdio-paranoia-dev \
    libcfg-dev \
    libcfitsio-dev \
    libchewing3-dev \
    libcjson-dev \
    libcmap-dev \
    libcmph-dev \
    libcodec2-dev \
    libcomedi-dev \
    libconfig-dev \
    libconfuse-dev \
    libcpg-dev \
    libcpufreq-dev \
    libcrack2-dev \
    libcrmcommon-dev \
    libcunit1-dev \
    libcups2-dev \
    libczmq-dev \
    libdbi-dev \
    libdca-dev \
    libdebconfclient0-dev \
    libdebian-installer4-dev \
    libdirectfb-dev \
    libdlm-dev \
    libdlmcontrol-dev \
    libdnet-dev \
    libdrm-dev \
    libdts-dev \
    libdv4-dev \
    libdw-dev \
    libdwarf-dev \
    libedit-dev \
    libelf-dev \
    libenca-dev \
    libepoxy-dev \
    libev-dev \
    libewf-dev \
    libext2fs-dev \
    libf2c2-dev \
    libfaad-dev \
    libfcgi-dev \
    libfdt-dev \
    libfftw3-dev \
    libfiu-dev \
    libflac-dev \
    libfluidsynth-dev \
    libforms-dev \
    libfreecell-solver-dev \
    libfreeimage-dev \
    libfreenect-dev \
    libftdi-dev \
    libftdi1-dev \
    libftgl-dev \
    libftp-dev \
    libfuse-dev \
    libgadu-dev \
    libgbm-dev \
    libgc-dev \
    libgcrypt20-dev \
    libgd-dev \
    libgenometools0-dev \
    libgeoip-dev \
    libgif-dev \
    libgit2-dev \
    libglew-dev \
    libglfw3-dev \
    libgnustep-base-dev \
    libgpac-dev \
    libgpm-dev \
    libgps-dev \
    libgraphicsmagick1-dev \
    libgsl-dev \
    libgsm1-dev \
    libgtkdatabox-dev \
    libharfbuzz-dev \
    libhiredis-dev \
    libiberty-dev \
    libibmad-dev \
    libibnetdisc-dev \
    libibumad-dev \
    libibverbs-dev \
    libidn11-dev \
    libigraph0-dev \
    libiksemel-dev \
    libimlib2-dev \
    libimobiledevice-dev \
    libiniparser-dev \
    libiodbc2-dev \
    libiptc-dev \
    libircclient-dev \
    libiscsi-dev \
    libisl-dev \
    libisns-dev \
    libiso9660-dev \
    libiw-dev \
    libixp-dev \
    libjack-dev \
    libjansson-dev \
    libjbig2dec0-dev \
    libjemalloc-dev \
    libjim-dev \
    libjpgalleg4-dev \
    libjson-c-dev \
    libjudy-dev \
    libkaz-dev \
    libkmod-dev \
    liblapack-dev \
    libldap2-dev \
    libldns-dev \
    libleveldb-dev \
    liblivemedia-dev \
    liblo-dev \
    liblua5.1-0-dev \
    liblua5.2-dev \
    liblua50-dev \
    liblualib50-dev \
    liblz4-dev \
    liblzo2-dev \
    libmad0-dev \
    libmagic-dev \
    libmarkdown2-dev \
    libmatheval-dev \
    libmbedtls-dev \
    libmcrypt-dev \
    libmd-dev \
    libmemcached-dev \
    libmetis-dev \
    libmhash-dev \
    libmicrohttpd-dev \
    libminiupnpc-dev \
    libmlt-dev \
    libmng-dev \
    libmnl-dev \
    libmodbus-dev \
    libmodplug-dev \
    libmowgli-2-dev \
    libmp3lame-dev \
    libmpc-dev \
    libmpcdec-dev \
    libmpfr-dev \
    libmpg123-dev \
    libmtp-dev \
    libmunge-dev \
    libneon27-dev \
    libnet1-dev \
    libnetcdf-dev \
    libnetfilter-conntrack-dev \
    libnetfilter-queue-dev \
    libnetpbm10-dev \
    libnewt-dev \
    libnfnetlink-dev \
    libnids-dev \
    libnl-3-dev \
    libnl-genl-3-dev \
    libnl-nf-3-dev \
    libnlopt-dev \
    libnorm-dev \
    libnotify-dev \
    libnuma-dev \
    liboauth-dev \
    libopenal-dev \
    libopencc-dev \
    libopencore-amrnb-dev \
    libopencore-amrwb-dev \
    libopencv-core-dev \
    libopencv-flann-dev \
    libopencv-imgproc-dev \
    libopenhpi-dev \
    libopenr2-dev \
    libosip2-dev \
    libpam0g-dev \
    libpapi-dev \
    libparted-dev \
    libpcap-dev \
    libpci-dev \
    libpciaccess-dev \
    libpcl1-dev \
    libpcp-pmda3-dev \
    libpcp3-dev \
    libpcsclite-dev \
    libperl-dev \
    libpfm4-dev \
    libpgm-dev \
    libpopt-dev \
    libportmidi-dev \
    libpri-dev \
    libproj-dev \
    libpsl-dev \
    libpth-dev \
    libpulse-dev \
    libpython2.7-dev \
    libqrencode-dev \
    libquicktime-dev \
    libquorum-dev \
    librabbitmq-dev \
    librados-dev \
    librbd-dev \
    librdf0-dev \
    librdkafka-dev \
    librdmacm-dev \
    librrd-dev \
    librtmp-dev \
    libs3-dev \
    libsamplerate0-dev \
    libsasl2-dev \
    libsctp-dev \
    libsdl-gfx1.2-dev \
    libsdl-image1.2-dev \
    libsdl-mixer1.2-dev \
    libsdl-ttf2.0-dev \
    libsdl2-mixer-dev \
    libsdl2-net-dev \
    libsgutils2-dev \
    libshout3-dev \
    libsigsegv-dev \
    libslang2-dev \
    libsmbclient-dev \
    libsmi2-dev \
    libsnappy-dev \
    libsndfile1-dev \
    libsndio-dev \
    libsocks4 \
    libsodium-dev \
    libsoil-dev \
    libspandsp-dev \
    libspectrum-dev \
    libspeex-dev \
    libspeexdsp-dev \
    libspiro-dev \
    libsprng2-dev \
    libsqlite0-dev \
    libss7-dev \
    libssh-dev \
    libssh2-1-dev \
    libst-dev \
    libstrophe-dev \
    libswresample-dev \
    libswscale-dev \
    libsysfs-dev \
    libtalloc-dev \
    libtar-dev \
    libtcc-dev \
    libtcl8.6 \
    libtdb-dev \
    libtheora-dev \
    libtokyocabinet-dev \
    libtokyotyrant-dev \
    libtommath-dev \
    libtonezone-dev \
    libtpm-unseal-dev \
    libtrace3-dev \
    libtre-dev \
    libtrio-dev \
    libtspi-dev \
    libtwolame-dev \
    libucl-dev \
    libudev-dev \
    libunbound-dev \
    libunwind-dev \
    liburcu-dev \
    libusb-1.0-0-dev \
    libusb-dev \
    libusbmuxd-dev \
    libuv1-dev \
    libvdeplug-dev \
    libvdpau-dev \
    libvirt-dev \
    libvncserver-dev \
    libvo-amrwbenc-dev \
    libvorbis-dev \
    libvpx-dev \
    libwavpack-dev \
    libwbclient-dev \
    libwebsockets-dev \
    libwrap0-dev \
    libx264-dev \
    libxaw7-dev \
    libxcb-icccm4-dev \
    libxcb-randr0-dev \
    libxcb-xinerama0-dev \
    libxerces-c-dev \
    libxft-dev \
    libxi-dev \
    libxmltok1-dev \
    libxmu-dev \
    libxnvctrl-dev \
    libxosd-dev \
    libxpm-dev \
    libxtables-dev \
    libxtst-dev \
    libxvidcore-dev \
    libxxf86dga-dev \
    libxxhash-dev \
    libyajl-dev \
    libzdb-dev \
    libzip-dev \
    libzmq3-dev \
    libzstd-dev \
    nasm \
    ocl-icd-opencl-dev \
    opt \
    portaudio19-dev \
    tcl-dev \
    vstream-client-dev \
    libgtk2.0-dev \
    pkg-config \
    ruby-full

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py

# Install packages for compilation & ease-of-use.

# copy library of headers over, and python script
COPY ./ADVobfuscator/Lib /Lib
COPY ./adv_string_obfuscation.py ./adv_string_obfuscation.py
COPY ./headers.c /headers.c

# create directory to copy repos and put binaries in
RUN mkdir /repos

# add gcc to path in front of everything else
RUN export PATH=/compiler:$PATH

RUN git config --global user.email "adv_obfuscator"
RUN git config --global user.name "ADV Obfuscator"

ENTRYPOINT ["python3", "adv_string_obfuscation.py"]
