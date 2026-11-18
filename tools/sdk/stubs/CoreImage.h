/* tools/sdk/stubs/CoreImage.h: what the AppKit sources need of CoreImage (declarations only) */
#import <Foundation/Foundation.h>
#import <CoreGraphics/CoreGraphics.h>
@interface CIImage : NSObject
@property(readonly) CGRect extent;
@end
