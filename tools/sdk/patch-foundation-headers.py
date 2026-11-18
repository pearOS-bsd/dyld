#!/usr/bin/env python3
"""Brings a COPY of the headers of ravynOS' Foundation (MIT, Cocotron lineage: older than Apple's) closer to the Foundation of the macOS SDK, for compiling Mach-O programs against Apple's runtime:
lightweight generics on the collections, the subscripting methods, the modern geometry type.   usage: patch-foundation-headers.py DIR_WITH_Foundation/   (the files are changed in place)
Only declarations: at run time the real Foundation (from the dyld cache) answers every call."""
import re, sys, os
d = sys.argv[1]
def sub(fn, pat, rep, flags=0):
    p = os.path.join(d, 'Foundation', fn) if os.path.isdir(os.path.join(d, 'Foundation')) else os.path.join(d, fn)
    s = open(p).read(); n = re.sub(pat, rep, s, count=1, flags=flags); open(p, 'w').write(n); return n != s
done = []
for fn, pat, rep in [
 ('NSArray.h',        r'@interface NSArray\s*<HIDEvent>\s*:\s*NSObject',      '@interface NSArray<__covariant ObjectType> : NSObject'),
 ('NSMutableArray.h', r'@interface NSMutableArray\s*:\s*NSArray',             '@interface NSMutableArray<ObjectType> : NSArray<ObjectType>'),
 ('NSSet.h',          r'@interface NSSet\s*:\s*NSObject',                     '@interface NSSet<__covariant ObjectType> : NSObject'),
 ('NSMutableSet.h',   r'@interface NSMutableSet\s*:\s*NSSet',                 '@interface NSMutableSet<ObjectType> : NSSet<ObjectType>'),
 ('NSDictionary.h',   r'@interface NSDictionary\s*:\s*NSObject',              '@interface NSDictionary<__covariant KeyType, __covariant ObjectType> : NSObject'),
 ('NSMutableDictionary.h', r'@interface NSMutableDictionary\s*:\s*NSDictionary', '@interface NSMutableDictionary<KeyType, ObjectType> : NSDictionary<KeyType, ObjectType>'),
 ('NSEnumerator.h',   r'@interface NSEnumerator\s*:\s*NSObject',              '@interface NSEnumerator<__covariant ObjectType> : NSObject'),
]:
    if sub(fn, pat, rep): done.append(fn)
# the subscripting methods (declarations only), imported at the end of Foundation.h
open(os.path.join(d, 'Foundation', 'NSSubscripting_pear.h') if os.path.isdir(os.path.join(d, 'Foundation')) else os.path.join(d, 'NSSubscripting_pear.h'), 'w').write('''/* tools/sdk/patch-foundation-headers.py: declarations of the subscripting methods that the macOS SDK has */
#import <Foundation/NSArray.h>
#import <Foundation/NSMutableArray.h>
#import <Foundation/NSDictionary.h>
#import <Foundation/NSMutableDictionary.h>
@interface NSArray<ObjectType> (PearSubscripting)
- (ObjectType)objectAtIndexedSubscript:(NSUInteger)idx;
@end
@interface NSMutableArray<ObjectType> (PearSubscripting)
- (void)setObject:(ObjectType)obj atIndexedSubscript:(NSUInteger)idx;
@end
@interface NSDictionary<KeyType, ObjectType> (PearSubscripting)
- (ObjectType)objectForKeyedSubscript:(KeyType)key;
@end
@interface NSMutableDictionary<KeyType, ObjectType> (PearSubscripting)
- (void)setObject:(ObjectType)obj forKeyedSubscript:(KeyType <NSCopying>)key;
@end
''')
fh = os.path.join(d, 'Foundation', 'Foundation.h') if os.path.isdir(os.path.join(d, 'Foundation')) else os.path.join(d, 'Foundation.h')
s = open(fh).read()
if 'NSSubscripting_pear.h' not in s: open(fh, 'w').write(s.rstrip('\n') + '\n#import <Foundation/NSSubscripting_pear.h>\n')
# the macros and types that the SDK of macOS has and this Foundation has not
if 'NS_OPTIONS' not in open(fh).read():
    t = open(fh).read()
    t = t.replace('#define NS_ENUM(_type, _name) enum _name:_type _name; enum _name : _type', '#define NS_ENUM(_type, _name) enum _name : _type _name; enum _name : _type\n#define NS_OPTIONS(_type, _name) enum _name : _type _name; enum _name : _type\n#define NS_CLOSED_ENUM(_type, _name) NS_ENUM(_type, _name)', 1)
    open(fh, 'w').write(t)
extra = os.path.join(os.path.dirname(fh), 'NSSubscripting_pear.h')
open(extra, 'a').write('''
@class NSExpression;
typedef struct NSEdgeInsets { CGFloat top, left, bottom, right; } NSEdgeInsets;
static inline NSEdgeInsets NSEdgeInsetsMake(CGFloat top, CGFloat left, CGFloat bottom, CGFloat right) { NSEdgeInsets e = { top, left, bottom, right }; return e; }
''')
print('patched:', ', '.join(done), '+ NSSubscripting_pear.h')
