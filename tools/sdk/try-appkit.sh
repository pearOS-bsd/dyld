#!/bin/sh
# syntax-only compile of the AppKit sources (AppKit/decompiled/src/*.m) for macOS (Apple runtime, deployment target 14) on FreeBSD, against the header tree of assemble-sdk.sh and the
# headers of ravynOS' Foundation / CoreGraphics (MIT) patched by patch-foundation-headers.py:  sh tools/sdk/try-appkit.sh [WORK] [APPKIT_DIR] [N]
W="${1:-/root/oss}"; A="${2:-$HOME/AppKit}"; N="${3:-1000}"; I="$W/sdk/usr/include"; H="$(cd "$(dirname "$0")" && pwd)"; P="$(dirname "$(dirname "$H")")/.."
RES=$(ls -d /usr/local/llvm*/lib/clang/*/include 2>/dev/null | tail -1); R="$W/sdk/ravyn"; rm -rf "$R"; mkdir -p "$R/Foundation" "$R/CoreGraphics" "$W/sdk/stubs/CoreText" "$W/sdk/stubs/CoreImage" "$W/sdk/stubs/CoreServices"
cp -R "${FOUNDATION_HEADERS:-$P/Foundation/upstream/ravynos-Foundation/Headers/Foundation}"/* "$R/Foundation/"; cp "${CG_HEADERS:-$P/CoreGraphics/upstream/ravynos-CoreGraphics}"/*.h "$R/CoreGraphics/"
python3 "$H/patch-foundation-headers.py" "$R" >/dev/null
cp "$H/stubs/CoreText/CoreText.h" "$W/sdk/stubs/CoreText/CoreText.h"; for h in CoreServices/CoreServices.h objc_size_alignment.h; do echo "/* stub */" > "$W/sdk/stubs/$h"; done; cp "$H/stubs/CoreImage.h" "$W/sdk/stubs/CoreImage/CoreImage.h"
S="$A/decompiled/src"; n=0; ok=0; : > "$W/sdk/appkit-errors.txt"
for f in $(ls "$S"/*.m | head -"$N"); do n=$((n+1))
	if cc --target=x86_64-apple-macosx14.0 -x objective-c -fobjc-runtime=macosx-14.0 -fobjc-arc -nostdinc -isystem "$RES" -isystem "$I" -isystem "$R" -isystem "$W/sdk/stubs" -I"$S" -I"$P/WindowServer/include" -I"$P/SkyLight/include" -fsyntax-only -Wno-everything -ferror-limit=2 "$f" 2>>"$W/sdk/appkit-errors.txt"; then ok=$((ok+1)); fi
done
echo "AppKit sources, syntax only: $ok of $n pass"
grep -E "error:" "$W/sdk/appkit-errors.txt" | sed -E "s/^[^ ]+ //; s/'[^']*'/'X'/g" | sort | uniq -c | sort -rn | head -6
