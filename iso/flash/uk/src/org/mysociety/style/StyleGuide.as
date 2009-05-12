package org.mysociety.style
{
    import com.stamen.graphics.color.IColor;
    import com.stamen.graphics.color.RGB;
    
    import flash.text.Font;
    import flash.text.FontType;
    import flash.text.TextField;
    import flash.text.TextFormat;
    
    import org.mysociety.style.fonts.c4.C4TextBold;
    import org.mysociety.style.fonts.c4.C4TextRegular;
    
    public class StyleGuide
    {
        public static var baseFont:Font = new C4TextRegular();
        public static var boldFont:Font = new C4TextBold();
        
        public static var turquoise:RGB = RGB.fromHex(0x339999);
        public static var darkBlue:RGB = RGB.fromHex(0x003366);
        public static var orange:RGB = RGB.fromHex(0xFFCC33);
        
        public static var baseFormat:TextFormat = new TextFormat(baseFont.fontName, 12, 0x000000);
         
        public static function getTextFormat(size:Number=0, color:IColor=null, bold:Boolean=false):TextFormat
        {
            var font:Font = bold ? boldFont : baseFont;
            return new TextFormat(font ? font.fontName : '_sans',
                                  size || baseFormat.size,
                                  color ? color.hex : baseFormat.color,
                                  bold);
        }
        
        public static function createTextField(size:Number=0, color:IColor=null, bold:Boolean=false):TextField
        {
            var font:Font = bold ? boldFont : baseFont;
            var field:TextField = new TextField();
            field.defaultTextFormat = getTextFormat(size, color, bold);
            field.embedFonts = font && (font.fontType == FontType.EMBEDDED);
            return field;
        }
    }
}