package org.mysociety.style.fonts.c4
{
    import flash.text.Font;

    [Embed(mimeType="application/x-font",
        fontName="C4 Text", fontWeight="bold",
        source="C4TexBol.ttf",
        unicodeRange='U+00A0,U+0020-U+007E,U+00A1-U+00BF,U+02BB-U+02BC,U+2010-U+2015,U+2018-U+201D,U+2024-U+2026'
    )]
    public class C4TextBold extends Font
    {
        public function C4TextBold()
        {
            super();
        }
        
    }
}