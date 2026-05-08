import glob
import sys

from setuptools import Extension, find_packages, setup
from setuptools.command.bdist_wheel import bdist_wheel


# The extension has no Python C API linkage (loaded via ctypes), so the wheel
# is compatible with any Python 3 on a given platform. Setuptools assumes any
# ext module implies a CPython ABI and would tag the wheel `cpXY-cpXY-<plat>`,
# forcing a rebuild per Python version. Override to emit `py3-none-<plat>`.
class bdist_wheel_abi_none(bdist_wheel):
    def finalize_options(self):
        super().finalize_options()
        self.root_is_pure = False

    def get_tag(self):
        _, _, plat = super().get_tag()
        return "py3", "none", plat


ed25519_extension = Extension(
    "ed25519_orlp.libed25519",
    sources=glob.glob("src/ed25519_orlp/csrc/*.c"),
    include_dirs=["src/ed25519_orlp/csrc"],
    define_macros=[("ED25519_BUILD_DLL", "1")],
    libraries=["advapi32"] if sys.platform == "win32" else [],
)

setup(
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    ext_modules=[ed25519_extension],
    package_data={"ed25519_orlp": ["csrc/*"]},
    cmdclass={"bdist_wheel": bdist_wheel_abi_none},
)
