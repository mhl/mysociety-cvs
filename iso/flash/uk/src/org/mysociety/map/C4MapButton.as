package org.mysociety.map
{
    import com.modestmaps.extras.ui.Button;
    import com.stamen.graphics.color.RGB;
    
    import flash.geom.ColorTransform;
    
    import org.mysociety.style.StyleGuide;

    public class C4MapButton extends Button
    {
        public function C4MapButton(type:String=null)
        {
            overTransform = new ColorTransform();
            outTransform = new ColorTransform();
            
            super(type, 4, StyleGuide.turquoise.hex, 0xFFFFFF, false);
        }
    }
}