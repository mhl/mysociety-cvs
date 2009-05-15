package com.stamen.ui.tooltip
{
	import flash.display.DisplayObject;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.filters.DropShadowFilter;
	import flash.geom.Point;
	import flash.text.AntiAliasType;
	import flash.text.Font;
	import flash.text.FontStyle;
	import flash.text.FontType;
	import flash.text.TextField;
	import flash.text.TextFormat;
	import flash.utils.clearTimeout;
	import flash.utils.setTimeout;
	
	public class Tooltip extends Sprite
	{
	    public var checkEveryFrame:Boolean = false;
	    
		private var tipTimer:uint;
		private var _active:Boolean = true;

		public var tipField:TextField;		
		
		public var defaultOffset:Point = new Point(0, -5);
		public var centered:Boolean = true;

		public var timeoutMillis:Number = 250;
		public var showSeconds:Number = .25;
		public var hideSeconds:Number = .25;
		
        protected var _bgColor:uint = 0xfffffee;
		protected var padding:Number = 2;
		
		protected var providerClass:Class;
		protected var blockerClass:Class;
		
		public function Tooltip(font:Font=null)
		{
			mouseChildren = mouseEnabled = false;
			visible = false;
			filters = [ new DropShadowFilter(1,45,0,1,3,3,.7,2) ];
			
			providerClass = TooltipProvider;
			blockerClass = TooltipBlocker;
			
			tipField = new TextField();
			tipField.mouseEnabled = false;
			tipField.selectable = false;
			tipField.embedFonts = font ? font.fontType == FontType.EMBEDDED : false;
			tipField.antiAliasType = AntiAliasType.ADVANCED;
            if (font)
            {
                tipField.defaultTextFormat = new TextFormat(font.fontName, 10, 0x000000, font.fontStyle == FontStyle.BOLD, null, null, null, null, null, null, null, null, null);
            }
            else
            {
                tipField.defaultTextFormat = new TextFormat("Helvetica", 10, 0x000000, false);
            }
			addChild(tipField);			
			
			addEventListener(Event.ADDED_TO_STAGE, onAddedToStage);	
		}
		
		public function setTextFormat(format:TextFormat, embedFonts:Boolean=true):void
		{
		    tipField.defaultTextFormat = format;
		    tipField.embedFonts = embedFonts;
		    if (active)
		    {
                tipField.text = tipField.text;
                redraw();
            }
		}
		
		public function get bgColor():uint
		{
		    return _bgColor;
		}
		
		public function set bgColor(value:uint):void
		{
		    if (value != bgColor)
		    {
                _bgColor = value;
                if (active) redraw();
            }
		}
		
		private function onAddedToStage(event:Event):void
		{
			removeEventListener(Event.ADDED_TO_STAGE, onAddedToStage);
            stage.addEventListener(MouseEvent.MOUSE_MOVE, checkUnderMouse);
			stage.addEventListener(MouseEvent.MOUSE_DOWN, disactivate);
			stage.addEventListener(MouseEvent.MOUSE_UP, activate);
			stage.addEventListener(Event.MOUSE_LEAVE, disactivate);
			stage.addEventListener(MouseEvent.MOUSE_OVER, activate);
			addEventListener(Event.REMOVED_FROM_STAGE, onRemovedFromStage);
		}
					
		private function onRemovedFromStage(event:Event):void
		{
			removeEventListener(Event.REMOVED_FROM_STAGE, onRemovedFromStage);
			stage.removeEventListener(MouseEvent.MOUSE_MOVE, checkUnderMouse);
			stage.removeEventListener(MouseEvent.MOUSE_DOWN, disactivate);
			stage.removeEventListener(MouseEvent.MOUSE_UP, activate);
			stage.removeEventListener(Event.MOUSE_LEAVE, disactivate);
			stage.removeEventListener(MouseEvent.MOUSE_OVER, activate);
			addEventListener(Event.ADDED_TO_STAGE, onAddedToStage);
		}			
		
		private function checkUnderMouse(event:Event=null):void
		{
			if (!active || !stage) return;
			if (alpha == 1) {
				hideSprite(this, hideSeconds);
				dispatchEvent(new TooltipEvent(TooltipEvent.HIDE, null));				
			}
			if (tipTimer) {
				clearTimeout(tipTimer);
			}
			
			if (timeoutMillis > 0)
			{
                tipTimer = setTimeout(reallyCheckUnderMouse, timeoutMillis);
            }
            else
            {
                reallyCheckUnderMouse();			
            }
		}
		
		private function visibleObjects(object:DisplayObject, ...rest):Boolean
		{
			return object.visible && object.alpha > 0;
		}
				
		private function reallyCheckUnderMouse():void
		{	
			if (active && stage) {
				
				var mousePoint:Point = new Point(stage.mouseX, stage.mouseY);

				var objs:Array = stage.getObjectsUnderPoint(mousePoint);
				objs = objs.reverse();
				
				objs = objs.filter(visibleObjects);
				
				//trace('[Tooltip.reallyCheckUnderMouse]', objs);
				
				var obj:DisplayObject;
				
				var gotOne:Boolean = false;
				for each (obj in objs) {
					if (obj is blockerClass) {
						break;
					}
					else if (obj is providerClass) {

						gotOne = true;

						dispatchEvent(new TooltipEvent(TooltipEvent.SHOW, obj));

						var tipText:String = TooltipProvider(obj).getTooltipText();

						if (tipField.htmlText != tipText) {

							tipField.htmlText = tipText;
							tipField.x = padding;
							tipField.y = padding;
							tipField.width = tipField.textWidth + 4;
							tipField.height = tipField.textHeight + 4;
							
							redraw();							
						}
						
						var p:Point;
						
						if (obj is TooltipPositioner) {
							p = TooltipPositioner(obj).getTooltipPosition();
						}
						else {
							p = new Point(stage.mouseX, stage.mouseY);
						}
						
						reposition(p);
						
						break;
					}
					else {
						obj = null;
					}
				}

				if (gotOne && parent) {
					parent.setChildIndex(this, parent.numChildren-1);
					showSprite(this, showSeconds);
				}				
			}			
		}
		
		protected function redraw():void
		{
			var w:Number = tipField.width + 2*tipField.x;
			var h:Number = tipField.height + 2*tipField.y - 1;
			with (this.graphics) {
				clear();
				beginFill(bgColor, 1.0);
				moveTo(0,0);
				lineTo(w, 0);
				lineTo(w, h);
				lineTo(0, h);
				lineTo(0, 0);
				endFill();
			}
		}
		
		protected function reposition(p:Point):void
		{
			if (stage) {
				if (centered) {				
					this.x = p.x - this.width/2 + defaultOffset.x;
					this.y = p.y - this.height + defaultOffset.y;
				}
				else {
					this.x = p.x + defaultOffset.x;
					this.y = p.y - this.height + defaultOffset.y;					
				}
				this.y = Math.max(1, Math.min(stage.stageHeight - this.height - 1, this.y));
				this.x = Math.max(1, Math.min(stage.stageWidth - this.width - 1, this.x));
				// TODO: avoid mouse?
			}
		}

		protected function activate(event:Event):void
		{
			active = true;
		}
		
		protected function disactivate(event:Event):void
		{
			active = false;
		}

		protected function set active(a:Boolean):void
		{
			_active = a;
			if (a) {
				checkUnderMouse();
			}
			else {
				hideSprite(this, hideSeconds);
				dispatchEvent(new TooltipEvent(TooltipEvent.HIDE, null));				
			}
		}
		
		protected function get active():Boolean
		{
			return _active;
		}
				
	}
}
