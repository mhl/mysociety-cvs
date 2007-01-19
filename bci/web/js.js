/*
 * js.js
 * Neighbourhood Fix-It JavaScript
 * 
 * TODO
 * Investigate jQuery
 * Tidy it all up
 * Don't wrap around tiles as it's quite confusing if the tile server is slow to respond
 * Selection of pin doesn't really need a server request, but I don't really care
 * 
 */

YAHOO.util.Event.onContentReady('compass', function() {
    var points = this.getElementsByTagName('a');
    points[1].onclick = function() { pan(0, tileheight); return false; };
    points[3].onclick = function() { pan(tilewidth, 0); return false; };
    points[4].onclick = function() { pan(-tilewidth, 0); return false; };
    points[6].onclick = function() { pan(0, -tileheight); return false; };
    points[0].onclick = function() { pan(tilewidth, tileheight); return false; };
    points[2].onclick = function() { pan(-tilewidth, tileheight); return false; };
    points[5].onclick = function() { pan(tilewidth, -tileheight); return false; };
    points[7].onclick = function() { pan(-tilewidth, -tileheight); return false; };
});

YAHOO.util.Event.onContentReady('mapForm', function() {
    this.onsubmit = function() {
        this.x.value = x + 2;
        this.y.value = y + 2;
        return true;
    }
});

var in_drag;
YAHOO.util.Event.onContentReady('drag', function() {
    var dragO = new YAHOO.util.DDMap('map');
    update_tiles(0, 0, false, true);
});

// I love the global
var tile_x = 0;
var tile_y = 0;
var tilewidth = 254;
var tileheight = 254;

function drag_check(e) {
    if (in_drag) {
        in_drag=false;
        return false;
    }
    return true;
}

function image_rotate(i, j, x, y) {
    var id = 't' + i + '.' + j;
    var img = document.getElementById(id);
    if (x)
        img.style.left = (img.offsetLeft + x*tilewidth) + 'px';
    if (y)
        img.style.top = (img.offsetTop + y*tileheight) + 'px';
}

var myAnim;
function pan(x, y) {
    if (!myAnim || !myAnim.isAnimated()) {
        update_tiles(x, y, true, false);
        myAnim = new YAHOO.util.Motion('drag', { points:{by:[x,y]} }, 10, YAHOO.util.Easing.easeOut);
        myAnim.useSeconds = false;
        myAnim.animate();
    }
}

function update_tiles(dx, dy, noMove, force) {
    if (!dx && !dy && !force) return;

    var old_drag_x = drag_x;
    var old_drag_y = drag_y;
    drag_x += dx;
    drag_y += dy;

    if (!noMove) {
        var drag = document.getElementById('drag');
        drag.style.left = drag_x + 'px';
        drag.style.top = drag_y + 'px';
    }

    var horizontal = Math.floor(old_drag_x/tilewidth) - Math.floor(drag_x/tilewidth);
    var vertical = Math.floor(old_drag_y/tileheight) - Math.floor(drag_y/tileheight);
    if (!horizontal && !vertical && !force) return;

    for (var j=0; j<horizontal; j++) {
        for (var i=0; i<6; i++) { image_rotate(i, mod(j + tile_x, 6),  6, 0); }
    }
    for (var j=horizontal; j<0; j++) {
        for (var i=0; i<6; i++) { image_rotate(i, mod(j + tile_x, 6), -6, 0); }
    }
    for (var i=0; i<vertical; i++) {
        for (var j=0; j<6; j++) { image_rotate(mod(i + tile_y, 6), j, 0,  6); }
    }
    for (var i=vertical; i<0; i++) {
        for (var j=0; j<6; j++) { image_rotate(mod(i + tile_y, 6), j, 0, -6); }
    }

    x += horizontal;
    tile_x = mod((tile_x + horizontal), 6);
    y -= vertical;
    tile_y = mod((tile_y + vertical), 6);

    var url = '/tilma/tileserver/10k-full-london/' + x + '-' + (x+5) + ',' + y + '-' + (y+5) + '/JSON';
    var req = YAHOO.util.Connect.asyncRequest('GET', url, async_response);
}

var async_response = {
    success: urls_loaded,
    failure: urls_not_loaded
};

function urls_not_loaded(o) {
}

// Load 6x6 grid of tiles around current 2x2
function urls_loaded(o) {
    var tiles = eval(o.responseText);
    var drag = document.getElementById('drag');
    for (var i=0; i<6; i++) {
        var ii = (i + tile_y) % 6;
        for (var j=0; j<6; j++) {
            var jj = (j + tile_x) % 6;
            var id = 't'+ii+'.'+jj;
            var xx = x+j;
            var yy = y+5-i;
            var img = document.getElementById(id);
            if (img) {
                if (!img.galleryimg) { img.galleryimg = false; }
                img.onclick = drag_check;
                var new_src = 'http://tilma.mysociety.org/tileserver/10k-full-london/' + tiles[i][j];
                if (img.src != new_src) img.src = new_src;
                img.name = 'tile_' + xx + '.' + yy;
                continue;
            }
            img = document.createElement('input');
            img.type = 'image';
            img.src = 'http://tilma.mysociety.org/tileserver/10k-full-london/' + tiles[i][j];
            img.name = 'tile_' + xx + '.' + yy;
            img.id = id;
            img.onclick = drag_check;
            img.style.position = 'absolute';
            img.style.width = tilewidth + 'px';
            img.style.height = tileheight + 'px';
            img.style.top = ((ii-2)*tileheight) + 'px';
            img.style.left = ((jj-2)*tilewidth) + 'px';
            img.galleryimg = false;
            img.alt = 'Loading...';
            drag.appendChild(img);
        }
    }
}

// Mod always to positive result
function mod(m, n) {
    if (m>=0) return m % n;
    return (m % n) + n;
}

/* Called every mousemove, so on first call, overwrite itself with quicker version */
function get_posn(ev) {
    var posx, posy;
    if (ev.pageX || ev.pageY) {
        get_posn = function(e) {
            return { x: e.pageX, y: e.pageY };
        };
    } else if (ev.clientX || ev.clientY) {
        get_posn = function(e) {
            return {
                x: e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft,
                y: e.clientY + document.body.scrollTop + document.documentElement.scrollTop
            };
        };
    } else {
        get_posn = function(e) {
            return { x: undef, y: undef };
        };
    }
    return get_posn(ev);
}

function setCursor(s) {
    var drag = document.getElementById('drag');
    var inputs = drag.getElementsByTagName('input');
    for (var i=0; i<inputs.length; i++) {
        inputs[i].style.cursor = s;
    }
}

var mouse_pos = {};
YAHOO.util.DDMap = function(id, sGroup, config) {
    if (id) {
        this.init(id, sGroup, config);
    }
};
YAHOO.extend(YAHOO.util.DDMap, YAHOO.util.DD, {
    scroll: false,
    b4MouseDown: function(e) { },
    b4StartDrag: function(x, y) { },
    startDrag: function(x, y) {
        mouse_pos = { x: x, y: y };
        setCursor('move');
        in_drag = true;
    },
    onDrag: function(e) {
        var point = get_posn(e);
        if (point == mouse_pos) return false;
        var dx = point.x-mouse_pos.x;
        var dy = point.y-mouse_pos.y;
        mouse_pos = point;
        update_tiles(dx, dy, false, false);
    },
    b4EndDrag: function(e) { },
    endDrag: function(e) {
        setCursor('crosshair');
    },
    toString: function() {
        return ("DDMap " + this.id);
    }
});
