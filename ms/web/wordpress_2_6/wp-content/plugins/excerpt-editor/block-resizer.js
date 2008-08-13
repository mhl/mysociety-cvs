// this script is part of Excerpt Editor plugin for Wordress. For stand-alone version visit http://www.laptoptips.ca/javascripts/block-resizer/

Resizer = {

  ttl : 'Drag to resize', // title for the resize handle if auto-created

  Start : function(e) {
    var y = e ? e.clientY : event.clientY;
    this.s = this.elem.style.height ? parseInt(this.elem.style.height) - y : this.elem.clientHeight - y;
    this.res = true;
    document.onselectstart = function(){return false;};
    document.onmousemove = function(e){Resizer.Move(e)};
    if (e) document.onmouseout = function(e){Resizer._s(e)};
    else document.body.onmouseleave = function(){Resizer.Stop()};
  },
  
  _s : function(e) {
    if ( e.target.nodeName != 'HTML' ) return;
    this.Stop();
  },
  
  Stop : function() {
	this.res = false;
    document.onselectstart = null;
    document.onmousemove = null;
    document.onmouseout = null;
    document.body.onmouseleave = null;
  },

  Move : function(e) {
    if ( this.res ) {
      var mvto = e ? e.clientY : event.clientY;
      var h = this.s + mvto;
      if( h < 60 ) return false;
      this.elem.style.height = h + 'px';
   }
  },

  Init : function() {
    var h;
    this.res = false;
    if ( this.elem && this.elem.id == id ) return;
    if ( ! ( this.elem = document.getElementById('pgee_edit_excrpt') ) ) return;
    if ( ! ( h = document.getElementById('auto-handle') ) ) return;
    h.onmousedown = function(e){Resizer.Start(e)};
    document.onmouseup = function(e){Resizer.Stop(e)};
    window.onunload = function(){Resizer.Exit()};
  },
  
  Exit : function() {
    document.onmouseup = null;
    window.onunload = null;
  }
}
Resizer.Init();