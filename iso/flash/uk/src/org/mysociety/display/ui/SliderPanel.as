package org.mysociety.display.ui
{
    import com.stamen.graphics.color.IColor;
    import com.stamen.graphics.color.RGB;
    import com.stamen.ui.BlockSprite;
    
    import flash.display.Shape;
    import flash.text.TextField;
    import flash.text.TextFieldAutoSize;
    
    import org.mysociety.style.StyleGuide;

    public class SliderPanel extends BlockSprite
    {
        public var slider:Slider;
        public var label:TextField;
        
        protected var titleField:TextField;
        protected var titleBg:Shape;
        
        public function SliderPanel(title:String, sliderMin:Number=0, sliderMax:Number=1, sliderValue:Number=0, w:Number=240, h:Number=60, color:IColor=null)
        {
            titleBg = new Shape();
            titleBg.graphics.beginFill(0x000000);
            titleBg.graphics.drawRect(0, 0, 20, 20);
            titleBg.graphics.endFill();
            addChild(titleBg);
            
            titleField = StyleGuide.createTextField(16, RGB.white(), true);
            titleField.autoSize = TextFieldAutoSize.LEFT;
            titleField.text = title;
            addChild(titleField);
            
            slider = new Slider(sliderMin, sliderMax, sliderValue);
            addChild(slider);
            
            label = StyleGuide.createTextField(12, RGB.black(), false);
            label.autoSize = TextFieldAutoSize.LEFT;
            addChild(label);
             
            super(w, h, color);
        }
        
        public function get titleWidth():Number
        {
            return titleBg.width;
        }
        
        override protected function resize():void
        {
            super.resize();
            
            titleField.x = 2;
            titleField.y = 0;
            
            titleBg.x = 0;
            titleBg.y = titleField.y;
            titleBg.width = Math.ceil(titleField.width + 4);
            titleBg.height = Math.ceil(titleField.height);
            
            slider.x = titleBg.x + 2;
            slider.y = titleBg.getRect(this).bottom + 13;
            slider.width = width;
            
            label.x = titleBg.x - 2;
            label.y = slider.y + 14;
        }
    }
}