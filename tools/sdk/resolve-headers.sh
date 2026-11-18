#!/bin/sh
# compiles a C file against the assembled tree and, for every header that is missing, looks for it in the fetched sources and copies it in (until it compiles or something is not to be found):
#   sh tools/sdk/resolve-headers.sh [WORK] [FILE.c]
W="${1:-/root/oss}"; I="$W/sdk/usr/include"; T="${2:-$W/sdk/t.c}"; RES=$(cc --print-resource-dir)/include; : > "$W/sdk/notfound.txt"
for i in $(seq 1 80); do
	out=$(cc --target=x86_64-apple-macosx14.0 -nostdinc -isystem "$RES" -isystem "$I" -fsyntax-only -ferror-limit=1 "$T" 2>&1)
	h=$(echo "$out" | grep -o "fatal error: '[^']*' file not found" | head -1 | sed "s/fatal error: '//; s/' file not found//")
	[ -z "$h" ] && { echo "$out" | head -12; echo "done after $((i-1)) headers copied"; break; }
	src=$(find "$W" -path "$W/sdk" -prune -o -path "*/$h" -type f -print 2>/dev/null | grep -v "/\.git/" | head -1)
	if [ -n "$src" ]; then mkdir -p "$I/$(dirname "$h")"; cp "$src" "$I/$h"; echo "copied $h  <- ${src#$W/}"
	else echo "NOT FOUND: $h" | tee -a "$W/sdk/notfound.txt"; break; fi
done
