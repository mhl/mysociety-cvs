package com.stamen.display
{
    import com.stamen.graphics.color.Color;
    import com.stamen.graphics.color.IColor;
    
    import flash.display.Sprite;

    public class ColorSprite extends Sprite
    {
        protected var _color:IColor;

        public function ColorSprite(color:IColor=null)
        {
            super();
            this.color = color; 
        }

        public function get color():IColor
        {
            return _color;
        }
        
        public function set color(value:IColor):void
        {
            if (!Color.compare(_color, value))
            {
                _color = value;
                updateColor();
            }
        }
        
        protected function updateColor():void
        {
        }
    }
}