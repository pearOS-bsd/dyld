#!/usr/bin/env python3
"""python3 tools/fwskel.py ROOT [LIST] | --tree ROOT: the symlink skeleton of the frameworks under ROOT.

dyld looks a dlopen() path up in the file system first (realpath) and only then in the shared cache, so the alias paths
(Foo.framework/Foo, .../Versions/Current/..., CoreServices.framework/Frameworks/...) need their symlinks although the dylibs
need not exist.  LIST: install names, one per line (default tools/framework-paths.txt: what a Mac process with AppKit loaded).
Found with cfprefsd, which dlopen()s FSEvents by the alias path and calls a null function pointer when that fails."""
import os, sys

def link(target, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.lexists(path):
        return
    os.symlink(target, path)

if len(sys.argv) > 2 and sys.argv[1] == '--tree':
    # python3 tools/fwskel.py --tree ROOT: the aliases of every framework that exists under ROOT/System/Library as a Versions/<V> directory
    # (an image laid out from a manifest: the binaries are in the dyld cache, Foo.framework/Foo and Versions/Current are what dlopen() needs;
    # found with AppKit on pearOS: NSSoftLinking of ViewBridge failed and -[NSApplication _currentAppIsViewService] asserted)
    root = sys.argv[2]
    n = 0
    for top in ('System/Library/Frameworks', 'System/Library/PrivateFrameworks', 'System/iOSSupport/System/Library/Frameworks', 'System/iOSSupport/System/Library/PrivateFrameworks'):
        for dirpath, dirnames, _ in os.walk(os.path.join(root, top)):
            for d in list(dirnames):
                if not d.endswith('.framework'):
                    continue
                fw = os.path.join(dirpath, d); name = d[:-len('.framework')]; vers = os.path.join(fw, 'Versions')
                if os.path.islink(fw) or not os.path.isdir(vers):
                    continue
                real = [v for v in sorted(os.listdir(vers)) if v != 'Current' and os.path.isdir(os.path.join(vers, v)) and not os.path.islink(os.path.join(vers, v))]
                if not real:
                    continue
                if not os.path.lexists(os.path.join(vers, 'Current')):
                    link(real[-1], os.path.join(vers, 'Current')); n += 1
                if not os.path.lexists(os.path.join(fw, name)):
                    link('Versions/Current/' + name, os.path.join(fw, name)); n += 1
                if os.path.isdir(os.path.join(vers, 'Current', 'Frameworks')) and not os.path.lexists(os.path.join(fw, 'Frameworks')):
                    link('Versions/Current/Frameworks', os.path.join(fw, 'Frameworks')); n += 1
    print('fwskel: %d links' % n)
    sys.exit(0)

root = sys.argv[1] if len(sys.argv) > 1 else '/'
lst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'framework-paths.txt')

for line in open(lst):
    p = line.strip()
    parts = p.split('/')
    for i, c in enumerate(parts):
        if not c.endswith('.framework') or i + 2 >= len(parts) or parts[i + 1] != 'Versions':
            continue
        fw = '/'.join(parts[:i + 1]); ver = parts[i + 2]; name = c[:-len('.framework')]
        os.makedirs(root + fw + '/Versions/' + ver, exist_ok=True)
        link(ver, root + fw + '/Versions/Current')
        link('Versions/Current/' + name, root + fw + '/' + name)
        if i > 0 and parts[i - 1] == 'Frameworks' and parts[i - 3:i - 2] == ['Versions']:      # Outer.framework/Versions/A/Frameworks/Inner.framework
            outer = '/'.join(parts[:i - 3])
            link('Versions/Current/Frameworks', root + outer + '/Frameworks')
