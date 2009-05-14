package com.stamen.ui.tooltip
{
	import flash.display.DisplayObject;
	import flash.events.Event;

	public class TooltipEvent extends Event
	{
		public static const SHOW:String = 'show';
		public static const HIDE:String = 'hide';
		
		public var obj:DisplayObject;
		
		public function TooltipEvent(type:String, obj:DisplayObject)
		{
			// TODO: make cancellable?
			super(type, false, false);
			this.obj = obj;
		}
	}
}