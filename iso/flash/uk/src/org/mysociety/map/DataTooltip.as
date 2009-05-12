package org.mysociety.map
{
    import com.stamen.graphics.color.RGB;
    
    import flash.display.Shape;
    import flash.display.Sprite;
    import flash.text.StyleSheet;
    import flash.text.TextField;
    import flash.text.TextFieldAutoSize;
    
    import org.mysociety.style.StyleGuide;

    public class DataTooltip extends Sprite
    {
        public var field:TextField;
        
        protected var bgColor:uint;
        protected var box:Shape;
        protected var arrow:Shape;
        
        public function DataTooltip(width:Number=235, height:Number=80, bgColor:uint=0x000000)
        {
            super();
            
            this.bgColor = bgColor;
            
            var size:int = 12;
            arrow = new Shape();
            arrow.graphics.beginFill(this.bgColor);
            arrow.graphics.moveTo(0, 0);
            arrow.graphics.lineTo(size, -size);
            arrow.graphics.lineTo(-size, -size);
            arrow.graphics.lineTo(0, 0);
            addChild(arrow);
            
            box = new Shape();
            box.graphics.beginFill(this.bgColor);
            box.graphics.drawRect(0, 0, width, height);
            box.graphics.endFill();
            box.x = -box.width / 2;
            box.y = -(box.height + arrow.height);
            addChild(box);
            
            var padding:Number = 8;
            field = StyleGuide.createTextField(15, RGB.white());
            field.selectable = false;
            field.autoSize = TextFieldAutoSize.LEFT;
            field.multiline = field.wordWrap = true;
            field.x = box.x + padding;
            field.y = box.y + padding - 3;
            field.width = box.width - padding * 2;
            field.height = box.height - padding * 2;
            var style:StyleSheet = new StyleSheet();
            style.setStyle('a', {color: '#' + StyleGuide.orange.toString(), fontWeight: 'bold'});
            field.styleSheet = style;
            addChild(field);
            
            mouseEnabled = mouseChildren = false;
        }
    }
}