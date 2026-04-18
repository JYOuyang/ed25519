from setuptools import setup, Extension
import glob

# Collect all .c files in the source directory
c_sources = glob.glob('src/ed25519_orlp/csrc/*.c')

ed25519_extension = Extension(
    'ed25519_orlp.libed25519',
    sources=c_sources,
    include_dirs=['src/ed25519_orlp/csrc'],
)

setup(
    ext_modules=[ed25519_extension],
)
