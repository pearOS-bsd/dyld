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
if 'NS_NOESCAPE' not in open(fh).read():
    t = open(fh).read()
    t = t.replace('#define NS_OPTIONS', '#ifndef NS_NOESCAPE\n#define NS_NOESCAPE __attribute__((noescape))\n#endif\n#define NS_EXTENSIBLE_STRING_ENUM\n#define NS_STRING_ENUM\n#define NS_TYPED_ENUM\n#define NS_TYPED_EXTENSIBLE_ENUM\n#define NS_OPTIONS', 1)
    open(fh, 'w').write(t)
open(extra, 'a').write('''
typedef NSString *NSRunLoopMode;
@protocol NSSecureCoding <NSCoding>
+ (BOOL)supportsSecureCoding;
@end
static const NSEdgeInsets NSEdgeInsetsZero = { 0, 0, 0, 0 };
typedef NSUInteger NSComparisonPredicateModifier;
extern NSString *const NSURLTypeIdentifierKey;
''' + ('' if any('NSComparator' in open(os.path.join(os.path.dirname(fh), f), errors='ignore').read() for f in os.listdir(os.path.dirname(fh)) if f.endswith('.h') and f != 'NSSubscripting_pear.h') else 'typedef NSComparisonResult (^NSComparator)(id obj1, id obj2);\n') + '''@interface NSMutableArray<ObjectType> (PearMore)
- (void)sortUsingComparator:(NSComparator)cmptr;
@end
@interface NSArray<ObjectType> (PearMore2)
- (NSUInteger)indexOfObjectPassingTest:(BOOL (^)(ObjectType obj, NSUInteger idx, BOOL *stop))predicate;
@end
@interface NSURL (PearMore)
- (BOOL)getResourceValue:(id *)value forKey:(NSString *)key error:(NSError **)error;
@end
@interface NSPointerArray : NSObject
@property(readonly) NSUInteger count;
- (void *)pointerAtIndex:(NSUInteger)index;
- (void)addPointer:(void *)pointer;
@end
typedef NS_ENUM(NSUInteger, NSCompoundPredicateType) { NSNotPredicateType = 0, NSAndPredicateType, NSOrPredicateType };
@interface NSJSONSerialization : NSObject
+ (id)JSONObjectWithData:(NSData *)data options:(NSUInteger)opt error:(NSError **)error;
+ (NSData *)dataWithJSONObject:(id)obj options:(NSUInteger)opt error:(NSError **)error;
@end
typedef NS_ENUM(NSUInteger, NSFileWrapperWritingOptions) { NSFileWrapperWritingAtomic = 1 << 0, NSFileWrapperWritingWithNameUpdating = 1 << 1 };
@interface NSFileWrapper : NSObject
- (BOOL)writeToURL:(NSURL *)url options:(NSFileWrapperWritingOptions)options originalContentsURL:(NSURL *)originalContentsURL error:(NSError **)outError;
- (NSData *)regularFileContents;
@end
typedef NSUInteger NSPredicateOperatorType;
@interface NSExpression : NSObject
+ (NSExpression *)expressionForConstantValue:(id)obj;
+ (NSExpression *)expressionForKeyPath:(NSString *)keyPath;
@end
typedef NS_ENUM(NSUInteger, PearPredOps) { NSLessThanPredicateOperatorType = 0, NSLessThanOrEqualToPredicateOperatorType, NSGreaterThanPredicateOperatorType, NSGreaterThanOrEqualToPredicateOperatorType, NSEqualToPredicateOperatorType, NSNotEqualToPredicateOperatorType, NSMatchesPredicateOperatorType, NSLikePredicateOperatorType, NSBeginsWithPredicateOperatorType, NSEndsWithPredicateOperatorType, NSInPredicateOperatorType, NSCustomSelectorPredicateOperatorType, NSContainsPredicateOperatorType = 99, NSBetweenPredicateOperatorType = 100 };
@interface NSComparisonPredicate : NSPredicate
+ (NSComparisonPredicate *)predicateWithLeftExpression:(NSExpression *)lhs rightExpression:(NSExpression *)rhs modifier:(NSComparisonPredicateModifier)modifier type:(NSPredicateOperatorType)type options:(NSUInteger)options;
- (NSComparisonPredicateModifier)comparisonPredicateModifier;
- (NSPredicateOperatorType)predicateOperatorType;
- (NSExpression *)leftExpression;
- (NSExpression *)rightExpression;
@end
@interface NSCompoundPredicate : NSPredicate
- (instancetype)initWithType:(NSCompoundPredicateType)type subpredicates:(NSArray *)subpredicates;
+ (NSPredicate *)andPredicateWithSubpredicates:(NSArray *)subpredicates;
- (NSCompoundPredicateType)compoundPredicateType;
- (NSArray *)subpredicates;
@end
@interface NSPropertyListSerialization (PearMore)
+ (id)propertyListWithData:(NSData *)data options:(NSUInteger)opt format:(NSUInteger *)format error:(NSError **)error;
+ (NSData *)dataWithPropertyList:(id)plist format:(NSUInteger)format options:(NSUInteger)opt error:(NSError **)error;
@end
@interface NSPointerArray (PearMore)
+ (NSPointerArray *)weakObjectsPointerArray;
- (void)removePointerAtIndex:(NSUInteger)index;
@end
@interface NSArray<ObjectType> (PearMore3)
- (NSArray<ObjectType> *)sortedArrayUsingComparator:(NSComparator)cmptr;
@end
@interface NSMutableIndexSet (PearMore)
- (void)enumerateIndexesUsingBlock:(void (^)(NSUInteger idx, BOOL *stop))block;
@end
@interface NSBundle (PearMore)
@property(readonly, copy) NSURL *bundleURL;
@property(readonly, copy) NSURL *executableURL;
@end
''')
cgdir = os.path.join(d, 'CoreGraphics')
if os.path.isdir(cgdir):
    open(os.path.join(cgdir, 'CGPear.h'), 'w').write('/* tools/sdk/patch-foundation-headers.py: declarations that the macOS SDK has and this CoreGraphics has not */\n' + '''typedef struct CGGradient *CGGradientRef;
extern const CFStringRef kCGColorSpaceSRGB, kCGColorSpaceGenericRGB, kCGColorSpaceLinearGray, kCGColorSpaceGenericGrayGamma2_2, kCGColorSpaceGenericCMYK, kCGColorSpaceDisplayP3;
CGRect CGRectApplyAffineTransform(CGRect rect, CGAffineTransform t);
CGAffineTransform CGAffineTransformInvert(CGAffineTransform t);
CGRect CGPathGetPathBoundingBox(CGPathRef path);
''')
    cgh = os.path.join(cgdir, 'CoreGraphics.h'); t = open(cgh).read()
    if 'CGPear.h' not in t: open(cgh, 'w').write(t.rstrip('\n') + '\n#import <CoreGraphics/CGPear.h>\n')

# NSMakeRange and the geometry helpers are static inline in the macOS SDK (the real Foundation does not export them)
for f, rep in (
    ('NSRange.h', [(r'FOUNDATION_EXPORT NSRange NSMakeRange\(NSUInteger location, NSUInteger length\);', 'static inline NSRange NSMakeRange(NSUInteger location, NSUInteger length) { NSRange r; r.location = location; r.length = length; return r; }'),
                   (r'FOUNDATION_EXPORT NSUInteger NSMaxRange\(NSRange range\);', 'static inline NSUInteger NSMaxRange(NSRange range) { return range.location + range.length; }')]),
    ('NSGeometry.h', [(r'FOUNDATION_EXPORT BOOL NSEqualRects\(NSRect rect0, NSRect rect1\);', 'static inline BOOL NSEqualRects(NSRect a, NSRect b) { return a.origin.x == b.origin.x && a.origin.y == b.origin.y && a.size.width == b.size.width && a.size.height == b.size.height; }'),
                      (r'FOUNDATION_EXPORT BOOL NSEqualSizes\(NSSize size0, NSSize size1\);', 'static inline BOOL NSEqualSizes(NSSize a, NSSize b) { return a.width == b.width && a.height == b.height; }'),
                      (r'FOUNDATION_EXPORT BOOL NSIntersectsRect\(NSRect rect0, NSRect rect1\);', 'static inline BOOL NSIntersectsRect(NSRect a, NSRect b) { return a.origin.x < b.origin.x + b.size.width && b.origin.x < a.origin.x + a.size.width && a.origin.y < b.origin.y + b.size.height && b.origin.y < a.origin.y + a.size.height; }')]),
):
    for pat, r in rep:
        sub(f, pat, r)

# MIN, MAX and ABS are macros of NSObjCRuntime.h in the macOS SDK
sub('NSObjCRuntime.h', r'(#define NS_INLINE static inline)', r'\1\n#ifndef MAX\n#define MAX(A,B) ({ __typeof__(A) __a = (A); __typeof__(B) __b = (B); __a < __b ? __b : __a; })\n#endif\n#ifndef MIN\n#define MIN(A,B) ({ __typeof__(A) __a = (A); __typeof__(B) __b = (B); __a < __b ? __a : __b; })\n#endif\n#ifndef ABS\n#define ABS(A) ({ __typeof__(A) __a = (A); __a < 0 ? -__a : __a; })\n#endif')
print('patched:', ', '.join(done), '+ NSSubscripting_pear.h')
