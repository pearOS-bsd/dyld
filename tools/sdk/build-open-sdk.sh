#!/bin/sh
# the whole chain on FreeBSD, no Mac: open sources -> migcom -> MIG headers -> header tree -> /open/AppKit, /open/Cocoa, /open/stub-*   (needs the llvm package: clang + ld64.lld)
#   sh tools/sdk/build-open-sdk.sh WORK TREE OUT     TREE: a directory with the repositories as siblings (AppKit WindowServer SkyLight CoreUI Foundation CoreGraphics dyld darwinator open)
set -e
W="${1:?work dir}"; T="${2:?tree of repositories}"; O="${3:?output dir}"; H="$(cd "$(dirname "$0")" && pwd)"
sh "$H/fetch-sources.sh" "$W"; sh "$H/build-migcom.sh" "$W"; sh "$H/gen-headers.sh" "$W/inc"; sh "$H/assemble-sdk.sh" "$W"       # gen-headers: sys/_symbol_aliasing.h (xnu makes it from the SDK of Xcode); without it every program that includes <sys/cdefs.h> fails to compile (the ISO build of 2026-11-19: /open and the Control Center did not build)
SDK_WORK="$W" sh "$T/open/build-appkit-bsd.sh" "$O"
