#!/usr/bin/env python3
"""
OCR a PDF using macOS Vision framework.

Usage: python3 parser/vision_ocr.py <input.pdf> <output.txt>

Renders each PDF page to a CGImage, runs VNRecognizeTextRequest with the
"accurate" recognition level, and writes the concatenated text. Page
boundaries are marked with a form-feed and `=== Page N ===` header.
"""

import sys
from pathlib import Path

from Quartz import (
    CGDataProviderCreateWithCFData,
    CGPDFDocumentCreateWithProvider,
    CGPDFDocumentGetNumberOfPages,
    CGPDFDocumentGetPage,
    CGPDFPageGetBoxRect,
    kCGPDFCropBox,
    CGBitmapContextCreate,
    CGBitmapContextCreateImage,
    CGContextDrawPDFPage,
    CGContextScaleCTM,
    CGContextSetRGBFillColor,
    CGContextFillRect,
    CGRectMake,
    CGColorSpaceCreateDeviceRGB,
    kCGImageAlphaPremultipliedLast,
)
from Vision import VNRecognizeTextRequest, VNImageRequestHandler
from CoreFoundation import CFDataCreate


def render_page_to_image(pdf_page, scale=4.0):
    """Render a single PDF page to a CGImage at the given scale."""
    rect = CGPDFPageGetBoxRect(pdf_page, kCGPDFCropBox)
    width = int(rect.size.width * scale)
    height = int(rect.size.height * scale)
    color_space = CGColorSpaceCreateDeviceRGB()
    ctx = CGBitmapContextCreate(
        None, width, height, 8, 0, color_space,
        kCGImageAlphaPremultipliedLast,
    )
    # White background
    CGContextSetRGBFillColor(ctx, 1, 1, 1, 1)
    CGContextFillRect(ctx, CGRectMake(0, 0, width, height))
    CGContextScaleCTM(ctx, scale, scale)
    CGContextDrawPDFPage(ctx, pdf_page)
    return CGBitmapContextCreateImage(ctx)


def ocr_image(cg_image):
    """Run Vision OCR on a CGImage. Returns the recognized text as a string."""
    handler = VNImageRequestHandler.alloc().initWithCGImage_options_(cg_image, None)
    request = VNRecognizeTextRequest.alloc().init()
    request.setRecognitionLevel_(1)  # 1 = accurate, 0 = fast
    request.setUsesLanguageCorrection_(True)
    success, error = handler.performRequests_error_([request], None)
    if not success:
        raise RuntimeError(f"Vision request failed: {error}")
    observations = request.results() or []
    lines = []
    for obs in observations:
        candidates = obs.topCandidates_(1)
        if candidates:
            lines.append(str(candidates[0].string()))
    return "\n".join(lines)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 vision_ocr.py <input.pdf> <output.txt>", file=sys.stderr)
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    data = pdf_path.read_bytes()
    cf_data = CFDataCreate(None, data, len(data))
    provider = CGDataProviderCreateWithCFData(cf_data)
    pdf_doc = CGPDFDocumentCreateWithProvider(provider)
    n_pages = CGPDFDocumentGetNumberOfPages(pdf_doc)

    pieces = []
    for i in range(1, n_pages + 1):
        page = CGPDFDocumentGetPage(pdf_doc, i)
        img = render_page_to_image(page)
        text = ocr_image(img)
        pieces.append(f"=== Page {i} ===\n{text}")
        print(f"  page {i}/{n_pages}: {len(text)} chars", file=sys.stderr)

    out_path.write_text("\n\f\n".join(pieces))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
