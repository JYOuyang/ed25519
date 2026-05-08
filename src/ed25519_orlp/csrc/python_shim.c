#ifdef _WIN32
/**
 * Satisfy the Windows linker which expects an entry point for a C extension.
 * Since we load this via ctypes, this function is never actually called,
 * but MSVC refuses to link the DLL without it.
 *
 * We avoid including Python.h here to minimize dependencies and avoid
 * linking against a specific Python DLL if possible, though setuptools
 * may still force it.
 */
__declspec(dllexport) void* PyInit_libed25519(void) {
    return 0;
}
#endif
