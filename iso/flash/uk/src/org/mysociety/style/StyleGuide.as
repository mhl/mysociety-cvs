package org.mysociety.style
{
    import com.stamen.graphics.color.IColor;
    import com.stamen.graphics.color.RGB;
    
    public class StyleGuide
    {
        public static var liteGreen:RGB = RGB.fromHex(0xCCEA66);
        public static var darkGreen:RGB = RGB.fromHex(0x339933);
        
        public static var highlight:IColor = darkGreen.clone();
         
        public function StyleGuide()
        {
        }

    }
}