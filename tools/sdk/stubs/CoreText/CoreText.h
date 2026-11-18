/* tools/sdk/stubs/CoreText/CoreText.h: the types and prototypes of CoreText that the AppKit sources use, written here (declarations only: at run time CoreText of the system answers) */
#ifndef PEAR_CORETEXT_STUB_H
#define PEAR_CORETEXT_STUB_H
#include <CoreFoundation/CoreFoundation.h>
#include <CoreGraphics/CoreGraphics.h>
typedef const struct __CFAttributedString *CFAttributedStringRef;
typedef const struct __CTFont *CTFontRef;
typedef const struct __CTFontDescriptor *CTFontDescriptorRef;
typedef const struct __CTLine *CTLineRef;
typedef const struct __CTFrame *CTFrameRef;
typedef const struct __CTFramesetter *CTFramesetterRef;
typedef uint32_t CTFontSymbolicTraits;
typedef uint32_t CTFontUIFontType;
typedef uint32_t CTFontOptions;
enum { kCTFontTraitItalic = 1 << 0, kCTFontTraitBold = 1 << 1, kCTFontTraitMonoSpace = 1 << 10, kCTFontTraitCondensed = 1 << 6, kCTFontTraitExpanded = 1 << 5 };
enum { kCTFontUIFontUser = 0, kCTFontUIFontUserFixedPitch = 1, kCTFontUIFontSystem = 2, kCTFontUIFontEmphasizedSystem = 3, kCTFontUIFontSmallSystem = 4, kCTFontUIFontMessage = 8, kCTFontUIFontMenuItem = 12 };
extern const CFStringRef kCTFontNameAttribute, kCTFontFamilyNameAttribute, kCTFontStyleNameAttribute, kCTFontSizeAttribute, kCTFontTraitsAttribute, kCTFontSymbolicTrait, kCTFontWeightTrait, kCTFontAttributeName, kCTForegroundColorAttributeName;
CTFontRef CTFontCreateWithName(CFStringRef name, CGFloat size, const CGAffineTransform *matrix);
CTFontRef CTFontCreateUIFontForLanguage(CTFontUIFontType uiType, CGFloat size, CFStringRef language);
CFStringRef CTFontCopyPostScriptName(CTFontRef font);
CGFloat CTFontGetSize(CTFontRef font);
CGFloat CTFontGetAscent(CTFontRef font);
CGFloat CTFontGetDescent(CTFontRef font);
CGFloat CTFontGetLeading(CTFontRef font);
CGFloat CTFontGetCapHeight(CTFontRef font);
CGFloat CTFontGetXHeight(CTFontRef font);
CGFloat CTFontGetSlantAngle(CTFontRef font);
CGFloat CTFontGetUnderlinePosition(CTFontRef font);
CGFloat CTFontGetUnderlineThickness(CTFontRef font);
CGRect CTFontGetBoundingBox(CTFontRef font);
CFIndex CTFontGetGlyphCount(CTFontRef font);
CTFontSymbolicTraits CTFontGetSymbolicTraits(CTFontRef font);
CTLineRef CTLineCreateWithAttributedString(CFAttributedStringRef string);
double CTLineGetTypographicBounds(CTLineRef line, CGFloat *ascent, CGFloat *descent, CGFloat *leading);
CFIndex CTLineGetStringIndexForPosition(CTLineRef line, CGPoint position);
CGFloat CTLineGetOffsetForStringIndex(CTLineRef line, CFIndex charIndex, CGFloat *secondaryOffset);
void CTLineDraw(CTLineRef line, CGContextRef context);
#endif
