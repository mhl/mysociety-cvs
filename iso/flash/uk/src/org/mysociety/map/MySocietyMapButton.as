package org.mysociety.map
{
    import com.modestmaps.extras.ui.Button;
    
    import flash.geom.ColorTransform;
    
    import org.mysociety.style.StyleGuide;

    public class MySocietyMapButton extends Button
    {
        public function MySocietyMapButton(type:String, radius:Number=4)
        {
            overTransform = new ColorTransform();
            outTransform = new ColorTransform();
            super(type, radius, StyleGuide.liteGreen.hex, 0x000000, false);
            
            scaleX = scaleY = 2;
        }
    }
}