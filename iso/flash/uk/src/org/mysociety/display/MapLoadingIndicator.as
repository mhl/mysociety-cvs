package org.mysociety.display
{
    import com.stamen.graphics.color.RGB;
    import com.stamen.ui.BlockSprite;
    import com.stamen.ui.LoadingBar;
    
    import flash.display.Graphics;
    import flash.geom.Rectangle;
    import flash.text.TextField;
    import flash.text.TextFieldAutoSize;
    
    import org.mysociety.style.StyleGuide;

    public class MapLoadingIndicator extends BlockSprite
    {
        public static const DEFAULT_WIDTH:Number = 256;
        public static const DEFAULT_HEIGHT:Number = 50;
        
        protected var title:TextField;
        protected var bar:LoadingBar;
        protected var padding:Number = 6;
        protected var round:Number = 0;
        
        public function MapLoadingIndicator(w:Number=DEFAULT_WIDTH, h:Number=DEFAULT_HEIGHT)
        {
            title = StyleGuide.createTextField(12, RGB.white(), true);
            title.autoSize = TextFieldAutoSize.LEFT;
            title.text = 'Loading...';
            addChild(title);
            
            bar = new LoadingBar();
            bar.indeterminate = true;
            addChild(bar);
            
            super(w, h, RGB.black());
        }
        
        override protected function resize():void
        {
            var rect:Rectangle = new Rectangle(0, 0, width, height);
            rect.inflate(-padding, -padding);
            
            title.y = rect.y - 3;
            title.x = rect.x - 2;
            title.width = rect.width + 2;
            
            bar.width = rect.width;
            bar.x = rect.x;
            bar.y = Math.ceil(title.y + title.height) + 4;
            
            _height = bar.y + bar.height + padding;
            
            super.resize();
        }
        
        override protected function drawShape(g:Graphics=null):void
        {
            if (round > 0)
            {
                (g || graphics).drawRoundRect(0, 0, width, height, round, round);
            }
            else
            {
                super.drawShape(g);
            }
        }
    }
}