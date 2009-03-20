package org.mysociety.display
{
    import com.modestmaps.core.Tile;

    public class NullTile extends Tile
    {
        public function NullTile(column:int, row:int, zoom:int)
        {
            super(column, row, zoom);

            graphics.clear();
            graphics.beginFill(0x000000);
            graphics.drawRect(0, 0, 256, 256);
            graphics.endFill();
        }

        override public function paintError(w:Number=256, h:Number=256):void
        {
        }
    }
}