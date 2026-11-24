# Building dyld-1378 from source: first attempt (2026-11-24)

Goal: roadmap step 2 (`docs/development/NO-MAC-ROADMAP.md`): our own dyld instead of the Mac's `/usr/lib/dyld`; and a place to add a guard and a message for re-export cycles
(`Loader::hasExportedSymbol` recurses without end when a symbol is re-exported back and forth and `alreadySearched` is null).

Where: FreeBSD VM (`/root/oss` has dyld-1378, xnu, Libc ... and the assembled header tree `/root/oss/sdk/usr/include` from `tools/sdk/*.sh`), `llvm21` (`clang++`, `ld64.lld`).
Command (syntax only): `clang++ --target=x86_64-apple-macosx14.0 -std=c++20 -fsyntax-only -nostdinc -nostdinc++ -isystem /usr/include/c++/v1 -isystem <clang resource dir> -isystem /root/oss/sdk/usr/include -I. -Idyld -Icommon -Iinclude -Imach_o -DBUILDING_DYLD=1 -DSUPPORT_VM_LAYOUT=1 -w FILE`

Results, in the order the errors appear:
1. `<span>`, `<array>` not found: dyld includes libc++; the SDK tree has none. Using FreeBSD's `/usr/include/c++/v1` gets past this.
2. `nl_types.h` not found (libc++ locale code), and `xlocale_refcounted *` vs `void *` errors: FreeBSD's libc++ expects FreeBSD's libc; use libc++ from Apple's open source (`apple-oss-distributions/libcxx`) or LLVM's, and bring `nl_types.h` from Libc.
3. `System/sys/reason.h` not found (`DyldRuntimeState.cpp`): an xnu header that dyld includes under the `System/` prefix; add `System/sys` -> `sys` to the tree.
Not yet tried: the other ~14 files of `dyld/`, `common/`, `mach_o/`, the link with `ld64.lld`, running the result on darwinator.
