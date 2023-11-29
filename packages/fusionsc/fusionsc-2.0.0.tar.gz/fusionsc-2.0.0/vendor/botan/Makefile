
# This makefile was generated using 'configure.py --minimized-build --enable-modules=auto_rng,blake2,sha2_32,sha2_64,system_rng --amalgamation --disable-shared --cc-bin C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.32.31326/bin/Hostx64/x64/cl.exe --cc msvc'

# Paths to relevant programs

CXX            = C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.32.31326/bin/Hostx64/x64/cl.exe
LINKER         = link
AR             = lib
AR_OPTIONS     = /nologo
PYTHON_EXE     = C:\Users\Knieps\AppData\Local\Programs\Python\Python310\python.exe

# Compiler Flags

ABI_FLAGS      =  
LANG_FLAGS     = /EHs /GR /D_WIN32_WINNT=0x0600
CXXFLAGS       = /MD /bigobj /O2 /Oi -DBOTAN_IS_BEING_BUILT
WARN_FLAGS     = /W4 /wd4250 /wd4251 /wd4275 /wd4127
LIB_FLAGS      = 
LDFLAGS        = 

EXE_LINK_CMD   = $(LINKER)

LIB_LINKS_TO        =  
BUILD_DIR_LINK_PATH = 
EXE_LINKS_TO        = .\botan.lib $(LIB_LINKS_TO) 

BUILD_FLAGS    = $(ABI_FLAGS) $(LANG_FLAGS) $(CXXFLAGS) $(WARN_FLAGS)

SCRIPTS_DIR    = C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/scripts
INSTALLED_LIB_DIR = c:\Botan\lib

# The primary target
all: libs cli tests docs

# Executable targets
CLI           = .\botan-cli.exe
TEST          = .\botan-test.exe
LIBRARIES     = .\botan.lib

cli: $(CLI)
tests: $(TEST)
libs: $(LIBRARIES)
docs: build\doc.stamp

# Misc targets


build\doc.stamp: C:/Users/Knieps/Documents/repos/fsc/vendor/botan\doc/*.rst C:/Users/Knieps/Documents/repos/fsc/vendor/botan\doc/api_ref/*.rst C:/Users/Knieps/Documents/repos/fsc/vendor/botan\doc/dev_ref/*.rst
	"$(PYTHON_EXE)" "$(SCRIPTS_DIR)/build_docs.py" --build-dir="build"

clean:
	"$(PYTHON_EXE)" "$(SCRIPTS_DIR)/cleanup.py" --build-dir="build"

distclean:
	"$(PYTHON_EXE)" "$(SCRIPTS_DIR)/cleanup.py" --build-dir="build" --distclean

install: libs cli docs
	"$(PYTHON_EXE)" "$(SCRIPTS_DIR)/install.py" --prefix="c:\Botan" --build-dir="build" --bindir="c:\Botan\bin" --libdir="c:\Botan\lib" --docdir="docs" --includedir="include"

check: tests
	"$(PYTHON_EXE)" "$(SCRIPTS_DIR)/check.py" --build-dir="build"

# Object Files
LIBOBJS = build\obj\lib\botan_all.obj

CLIOBJS = build\obj\cli\argon2.obj build\obj\cli\asn1.obj build\obj\cli\bcrypt.obj build\obj\cli\cc_enc.obj build\obj\cli\cli.obj build\obj\cli\cli_rng.obj build\obj\cli\codec.obj build\obj\cli\compress.obj build\obj\cli\encryption.obj build\obj\cli\entropy.obj build\obj\cli\hash.obj build\obj\cli\hmac.obj build\obj\cli\main.obj build\obj\cli\math.obj build\obj\cli\pbkdf.obj build\obj\cli\pk_crypt.obj build\obj\cli\psk.obj build\obj\cli\pubkey.obj build\obj\cli\roughtime.obj build\obj\cli\sandbox.obj build\obj\cli\speed.obj build\obj\cli\timing_tests.obj build\obj\cli\tls_client.obj build\obj\cli\tls_http_server.obj build\obj\cli\tls_proxy.obj build\obj\cli\tls_server.obj build\obj\cli\tls_utils.obj build\obj\cli\tss.obj build\obj\cli\utils.obj build\obj\cli\x509.obj build\obj\cli\zfec.obj

TESTOBJS = build\obj\test\main.obj build\obj\test\test_aead.obj build\obj\test\test_asn1.obj build\obj\test\test_bigint.obj build\obj\test\test_block.obj build\obj\test\test_blowfish.obj build\obj\test\test_c25519.obj build\obj\test\test_certstor.obj build\obj\test\test_certstor_flatfile.obj build\obj\test\test_certstor_system.obj build\obj\test\test_certstor_utils.obj build\obj\test\test_clang_bug.obj build\obj\test\test_compression.obj build\obj\test\test_cryptobox.obj build\obj\test\test_datastore.obj build\obj\test\test_dh.obj build\obj\test\test_dl_group.obj build\obj\test\test_dlies.obj build\obj\test\test_dsa.obj build\obj\test\test_ecc_pointmul.obj build\obj\test\test_ecdh.obj build\obj\test\test_ecdsa.obj build\obj\test\test_ecgdsa.obj build\obj\test\test_ecies.obj build\obj\test\test_eckcdsa.obj build\obj\test\test_ed25519.obj build\obj\test\test_elgamal.obj build\obj\test\test_entropy.obj build\obj\test\test_ffi.obj build\obj\test\test_filters.obj build\obj\test\test_fpe.obj build\obj\test\test_gf2m.obj build\obj\test\test_gost_3410.obj build\obj\test\test_hash.obj build\obj\test\test_hash_id.obj build\obj\test\test_kdf.obj build\obj\test\test_keywrap.obj build\obj\test\test_mac.obj build\obj\test\test_mceliece.obj build\obj\test\test_modes.obj build\obj\test\test_mp.obj build\obj\test\test_name_constraint.obj build\obj\test\test_newhope.obj build\obj\test\test_ocb.obj build\obj\test\test_ocsp.obj build\obj\test\test_octetstring.obj build\obj\test\test_oid.obj build\obj\test\test_os_utils.obj build\obj\test\test_otp.obj build\obj\test\test_package_transform.obj build\obj\test\test_pad.obj build\obj\test\test_passhash.obj build\obj\test\test_pbkdf.obj build\obj\test\test_pem.obj build\obj\test\test_pk_pad.obj build\obj\test\test_pkcs11_high_level.obj build\obj\test\test_pkcs11_low_level.obj build\obj\test\test_psk_db.obj build\obj\test\test_pubkey.obj build\obj\test\test_rfc6979.obj build\obj\test\test_rng.obj build\obj\test\test_rng_kat.obj build\obj\test\test_roughtime.obj build\obj\test\test_rsa.obj build\obj\test\test_runner.obj build\obj\test\test_simd.obj build\obj\test\test_siv.obj build\obj\test\test_sm2.obj build\obj\test\test_sodium.obj build\obj\test\test_srp6.obj build\obj\test\test_stream.obj build\obj\test\test_tests.obj build\obj\test\test_thread_utils.obj build\obj\test\test_tls.obj build\obj\test\test_tls_messages.obj build\obj\test\test_tls_stream_integration.obj build\obj\test\test_tpm.obj build\obj\test\test_tss.obj build\obj\test\test_uri.obj build\obj\test\test_utils.obj build\obj\test\test_workfactor.obj build\obj\test\test_x509_dn.obj build\obj\test\test_x509_path.obj build\obj\test\test_xmss.obj build\obj\test\test_zfec.obj build\obj\test\tests.obj build\obj\test\unit_asio_stream.obj build\obj\test\unit_ecc.obj build\obj\test\unit_ecdh.obj build\obj\test\unit_ecdsa.obj build\obj\test\unit_tls.obj build\obj\test\unit_tls_policy.obj build\obj\test\unit_x509.obj

# Executable targets

$(CLI): $(LIBRARIES) $(CLIOBJS)
	$(EXE_LINK_CMD) $(ABI_FLAGS) $(CLIOBJS) $(BUILD_DIR_LINK_PATH) $(LDFLAGS) $(EXE_LINKS_TO) /OUT:$@

$(TEST): $(LIBRARIES) $(TESTOBJS)
	$(EXE_LINK_CMD) $(ABI_FLAGS) $(TESTOBJS) $(BUILD_DIR_LINK_PATH) $(LDFLAGS) $(EXE_LINKS_TO) /OUT:$@



# Library targets


./botan.lib: $(LIBOBJS)
	$(AR) $(AR_OPTIONS) /OUT:$@ $(LIBOBJS)



# Build Commands

build\obj\lib\botan_all.obj: botan_all.cpp
	$(CXX) $(LIB_FLAGS) $(BUILD_FLAGS)  /Ibuild\include /nologo /c botan_all.cpp /Fo$@



build\obj\cli\argon2.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/argon2.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/argon2.cpp /Fo$@

build\obj\cli\asn1.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/asn1.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/asn1.cpp /Fo$@

build\obj\cli\bcrypt.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/bcrypt.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/bcrypt.cpp /Fo$@

build\obj\cli\cc_enc.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/cc_enc.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/cc_enc.cpp /Fo$@

build\obj\cli\cli.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/cli.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/cli.cpp /Fo$@

build\obj\cli\cli_rng.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/cli_rng.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/cli_rng.cpp /Fo$@

build\obj\cli\codec.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/codec.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/codec.cpp /Fo$@

build\obj\cli\compress.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/compress.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/compress.cpp /Fo$@

build\obj\cli\encryption.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/encryption.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/encryption.cpp /Fo$@

build\obj\cli\entropy.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/entropy.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/entropy.cpp /Fo$@

build\obj\cli\hash.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/hash.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/hash.cpp /Fo$@

build\obj\cli\hmac.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/hmac.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/hmac.cpp /Fo$@

build\obj\cli\main.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/main.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/main.cpp /Fo$@

build\obj\cli\math.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/math.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/math.cpp /Fo$@

build\obj\cli\pbkdf.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/pbkdf.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/pbkdf.cpp /Fo$@

build\obj\cli\pk_crypt.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/pk_crypt.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/pk_crypt.cpp /Fo$@

build\obj\cli\psk.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/psk.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/psk.cpp /Fo$@

build\obj\cli\pubkey.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/pubkey.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/pubkey.cpp /Fo$@

build\obj\cli\roughtime.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/roughtime.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/roughtime.cpp /Fo$@

build\obj\cli\sandbox.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/sandbox.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/sandbox.cpp /Fo$@

build\obj\cli\speed.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/speed.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/speed.cpp /Fo$@

build\obj\cli\timing_tests.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/timing_tests.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/timing_tests.cpp /Fo$@

build\obj\cli\tls_client.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/tls_client.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/tls_client.cpp /Fo$@

build\obj\cli\tls_http_server.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/tls_http_server.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/tls_http_server.cpp /Fo$@

build\obj\cli\tls_proxy.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/tls_proxy.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/tls_proxy.cpp /Fo$@

build\obj\cli\tls_server.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/tls_server.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/tls_server.cpp /Fo$@

build\obj\cli\tls_utils.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/tls_utils.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/tls_utils.cpp /Fo$@

build\obj\cli\tss.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/tss.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/tss.cpp /Fo$@

build\obj\cli\utils.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/utils.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/utils.cpp /Fo$@

build\obj\cli\x509.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/x509.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/x509.cpp /Fo$@

build\obj\cli\zfec.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/zfec.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/cli/zfec.cpp /Fo$@



build\obj\test\main.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/main.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/main.cpp /Fo$@

build\obj\test\test_aead.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_aead.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_aead.cpp /Fo$@

build\obj\test\test_asn1.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_asn1.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_asn1.cpp /Fo$@

build\obj\test\test_bigint.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_bigint.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_bigint.cpp /Fo$@

build\obj\test\test_block.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_block.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_block.cpp /Fo$@

build\obj\test\test_blowfish.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_blowfish.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_blowfish.cpp /Fo$@

build\obj\test\test_c25519.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_c25519.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_c25519.cpp /Fo$@

build\obj\test\test_certstor.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_certstor.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_certstor.cpp /Fo$@

build\obj\test\test_certstor_flatfile.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_certstor_flatfile.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_certstor_flatfile.cpp /Fo$@

build\obj\test\test_certstor_system.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_certstor_system.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_certstor_system.cpp /Fo$@

build\obj\test\test_certstor_utils.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_certstor_utils.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_certstor_utils.cpp /Fo$@

build\obj\test\test_clang_bug.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_clang_bug.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_clang_bug.cpp /Fo$@

build\obj\test\test_compression.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_compression.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_compression.cpp /Fo$@

build\obj\test\test_cryptobox.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_cryptobox.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_cryptobox.cpp /Fo$@

build\obj\test\test_datastore.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_datastore.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_datastore.cpp /Fo$@

build\obj\test\test_dh.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_dh.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_dh.cpp /Fo$@

build\obj\test\test_dl_group.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_dl_group.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_dl_group.cpp /Fo$@

build\obj\test\test_dlies.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_dlies.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_dlies.cpp /Fo$@

build\obj\test\test_dsa.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_dsa.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_dsa.cpp /Fo$@

build\obj\test\test_ecc_pointmul.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_ecc_pointmul.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_ecc_pointmul.cpp /Fo$@

build\obj\test\test_ecdh.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_ecdh.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_ecdh.cpp /Fo$@

build\obj\test\test_ecdsa.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_ecdsa.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_ecdsa.cpp /Fo$@

build\obj\test\test_ecgdsa.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_ecgdsa.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_ecgdsa.cpp /Fo$@

build\obj\test\test_ecies.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_ecies.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_ecies.cpp /Fo$@

build\obj\test\test_eckcdsa.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_eckcdsa.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_eckcdsa.cpp /Fo$@

build\obj\test\test_ed25519.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_ed25519.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_ed25519.cpp /Fo$@

build\obj\test\test_elgamal.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_elgamal.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_elgamal.cpp /Fo$@

build\obj\test\test_entropy.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_entropy.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_entropy.cpp /Fo$@

build\obj\test\test_ffi.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_ffi.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_ffi.cpp /Fo$@

build\obj\test\test_filters.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_filters.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_filters.cpp /Fo$@

build\obj\test\test_fpe.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_fpe.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_fpe.cpp /Fo$@

build\obj\test\test_gf2m.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_gf2m.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_gf2m.cpp /Fo$@

build\obj\test\test_gost_3410.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_gost_3410.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_gost_3410.cpp /Fo$@

build\obj\test\test_hash.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_hash.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_hash.cpp /Fo$@

build\obj\test\test_hash_id.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_hash_id.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_hash_id.cpp /Fo$@

build\obj\test\test_kdf.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_kdf.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_kdf.cpp /Fo$@

build\obj\test\test_keywrap.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_keywrap.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_keywrap.cpp /Fo$@

build\obj\test\test_mac.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_mac.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_mac.cpp /Fo$@

build\obj\test\test_mceliece.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_mceliece.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_mceliece.cpp /Fo$@

build\obj\test\test_modes.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_modes.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_modes.cpp /Fo$@

build\obj\test\test_mp.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_mp.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_mp.cpp /Fo$@

build\obj\test\test_name_constraint.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_name_constraint.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_name_constraint.cpp /Fo$@

build\obj\test\test_newhope.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_newhope.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_newhope.cpp /Fo$@

build\obj\test\test_ocb.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_ocb.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_ocb.cpp /Fo$@

build\obj\test\test_ocsp.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_ocsp.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_ocsp.cpp /Fo$@

build\obj\test\test_octetstring.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_octetstring.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_octetstring.cpp /Fo$@

build\obj\test\test_oid.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_oid.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_oid.cpp /Fo$@

build\obj\test\test_os_utils.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_os_utils.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_os_utils.cpp /Fo$@

build\obj\test\test_otp.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_otp.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_otp.cpp /Fo$@

build\obj\test\test_package_transform.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_package_transform.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_package_transform.cpp /Fo$@

build\obj\test\test_pad.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_pad.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_pad.cpp /Fo$@

build\obj\test\test_passhash.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_passhash.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_passhash.cpp /Fo$@

build\obj\test\test_pbkdf.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_pbkdf.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_pbkdf.cpp /Fo$@

build\obj\test\test_pem.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_pem.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_pem.cpp /Fo$@

build\obj\test\test_pk_pad.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_pk_pad.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_pk_pad.cpp /Fo$@

build\obj\test\test_pkcs11_high_level.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_pkcs11_high_level.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_pkcs11_high_level.cpp /Fo$@

build\obj\test\test_pkcs11_low_level.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_pkcs11_low_level.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_pkcs11_low_level.cpp /Fo$@

build\obj\test\test_psk_db.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_psk_db.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_psk_db.cpp /Fo$@

build\obj\test\test_pubkey.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_pubkey.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_pubkey.cpp /Fo$@

build\obj\test\test_rfc6979.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_rfc6979.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_rfc6979.cpp /Fo$@

build\obj\test\test_rng.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_rng.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_rng.cpp /Fo$@

build\obj\test\test_rng_kat.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_rng_kat.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_rng_kat.cpp /Fo$@

build\obj\test\test_roughtime.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_roughtime.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_roughtime.cpp /Fo$@

build\obj\test\test_rsa.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_rsa.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_rsa.cpp /Fo$@

build\obj\test\test_runner.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_runner.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_runner.cpp /Fo$@

build\obj\test\test_simd.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_simd.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_simd.cpp /Fo$@

build\obj\test\test_siv.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_siv.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_siv.cpp /Fo$@

build\obj\test\test_sm2.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_sm2.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_sm2.cpp /Fo$@

build\obj\test\test_sodium.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_sodium.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_sodium.cpp /Fo$@

build\obj\test\test_srp6.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_srp6.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_srp6.cpp /Fo$@

build\obj\test\test_stream.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_stream.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_stream.cpp /Fo$@

build\obj\test\test_tests.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_tests.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_tests.cpp /Fo$@

build\obj\test\test_thread_utils.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_thread_utils.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_thread_utils.cpp /Fo$@

build\obj\test\test_tls.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_tls.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_tls.cpp /Fo$@

build\obj\test\test_tls_messages.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_tls_messages.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_tls_messages.cpp /Fo$@

build\obj\test\test_tls_stream_integration.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_tls_stream_integration.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_tls_stream_integration.cpp /Fo$@

build\obj\test\test_tpm.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_tpm.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_tpm.cpp /Fo$@

build\obj\test\test_tss.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_tss.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_tss.cpp /Fo$@

build\obj\test\test_uri.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_uri.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_uri.cpp /Fo$@

build\obj\test\test_utils.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_utils.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_utils.cpp /Fo$@

build\obj\test\test_workfactor.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_workfactor.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_workfactor.cpp /Fo$@

build\obj\test\test_x509_dn.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_x509_dn.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_x509_dn.cpp /Fo$@

build\obj\test\test_x509_path.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_x509_path.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_x509_path.cpp /Fo$@

build\obj\test\test_xmss.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_xmss.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_xmss.cpp /Fo$@

build\obj\test\test_zfec.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_zfec.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/test_zfec.cpp /Fo$@

build\obj\test\tests.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/tests.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/tests.cpp /Fo$@

build\obj\test\unit_asio_stream.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/unit_asio_stream.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/unit_asio_stream.cpp /Fo$@

build\obj\test\unit_ecc.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/unit_ecc.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/unit_ecc.cpp /Fo$@

build\obj\test\unit_ecdh.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/unit_ecdh.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/unit_ecdh.cpp /Fo$@

build\obj\test\unit_ecdsa.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/unit_ecdsa.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/unit_ecdsa.cpp /Fo$@

build\obj\test\unit_tls.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/unit_tls.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/unit_tls.cpp /Fo$@

build\obj\test\unit_tls_policy.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/unit_tls_policy.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/unit_tls_policy.cpp /Fo$@

build\obj\test\unit_x509.obj: C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/unit_x509.cpp
	$(CXX) $(BUILD_FLAGS)  /Ibuild\include /nologo /c C:/Users/Knieps/Documents/repos/fsc/vendor/botan/src/tests/unit_x509.cpp /Fo$@





