package org.mysociety.display
{
    import com.modestmaps.core.Tile;
    import com.stamen.graphics.color.IColor;
    import com.stamen.graphics.color.RGB;

    public class NullTile extends Tile
    {
        public static var fillColor:IColor = RGB.grey(0x99);
        public static var errorColor:IColor = new RGB(255, 0, 0);
        
        public function NullTile(column:int, row:int, zoom:int)
        {
            super(column, row, zoom);

            graphics.clear();
            if (fillColor)
            {
                graphics.beginFill(fillColor.hex, fillColor.alpha);
                graphics.drawRect(0, 0, 256, 256);
                graphics.endFill();
            }
        }

        override public function paintError(w:Number=256, h:Number=256):void
        {
            graphics.clear();
            if (errorColor)
            {
                graphics.beginFill(errorColor.hex, errorColor.alpha);
                graphics.drawRect(0, 0, w, h);
                graphics.endFill();
            }
        }
    }
}