# dyld

The loader side of running Mac programs on FreeBSD (the kernel module is `darwinator`).

- `machrun/` — `machrun`, a user-space loader for Mach-O programs (the older path: Objective-C 2 metadata to the GNU runtime, Foundation/AppKit from GNUstep), `libmachcompat.so`, `libexctrace.so`.
- `tools/` — `macapp` (`macapp APP.app`), `macapp-install`, `wrapapp.sh`, `maccli`, `macprobe`, `fwskel.py` (symlink skeleton for framework paths; `--tree ROOT` makes the aliases of every framework of an image), `stackdump.c` (DYLD_INSERT_LIBRARIES dylib: `kill -USR2` prints every thread's stack, symbolised; on pearOS needs darwinator's thread_get_state of other threads), `framework-paths.txt`, `symbolize-trace.py`, `annotate-sel.py`, `migids.py`, `elf2macho.py`, `mkmacho.py`, `shims/`, `sdk/` (MIG tools).
- `docs/` — notes on the real dyld (`REALDYLD.md`), the tools, compatibility, the toolchain.

Today the real `dyld` of the Mac (`/usr/lib/dyld`) and the cache come from your own Mac (`macdeps`).  Plan: build dyld from the public source (`apple-oss-distributions/dyld`, APSL 2.0) and keep it here, with the licence and our changes marked.
