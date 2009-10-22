/*
 * js.js
 * FixMyStreet JavaScript
 * 
 * TODO
 * Investigate jQuery
 * Tidy it all up
 * Selection of pin doesn't really need a server request, but I don't really care
 * 
 */


YAHOO.util.Event.onContentReady('pc', function() {
    if (this.id && this.value == this.defaultValue) {
        this.focus();
    }
});

function compass_pan(e, a) {
    YAHOO.util.Event.preventDefault(e);
    if (a.home) {
        a.x = a.orig_x-drag_x;
        a.y = a.orig_y-drag_y;
    }
    pan(a.x, a.y);
}

YAHOO.util.Event.onContentReady('compass', function() {
    var ua=navigator.userAgent.toLowerCase();
    // if (document.getElementById('mapForm') && (/safari/.test(ua) || /Konqueror/.test(ua))) return;
    if (document.getElementById('map').offsetWidth > 510) return;

    var points = this.getElementsByTagName('a');
    YAHOO.util.Event.addListener(points[1], 'click', compass_pan, { x:0, y:tileheight });
    YAHOO.util.Event.addListener(points[3], 'click', compass_pan, { x:tilewidth, y:0 });
    YAHOO.util.Event.addListener(points[5], 'click', compass_pan, { x:-tilewidth, y:0 });
    YAHOO.util.Event.addListener(points[7], 'click', compass_pan, { x:0, y:-tileheight });
    YAHOO.util.Event.addListener(points[0], 'click', compass_pan, { x:tilewidth, y:tileheight });
    YAHOO.util.Event.addListener(points[2], 'click', compass_pan, { x:-tilewidth, y:tileheight });
    YAHOO.util.Event.addListener(points[6], 'click', compass_pan, { x:tilewidth, y:-tileheight });
    YAHOO.util.Event.addListener(points[8], 'click', compass_pan, { x:-tilewidth, y:-tileheight });
    YAHOO.util.Event.addListener(points[4], 'click', compass_pan, { home:1, orig_x:drag_x, orig_y:drag_y });
});

YAHOO.util.Event.onContentReady('map', function() {
    var ua=navigator.userAgent.toLowerCase();
    // if (document.getElementById('mapForm') && (/safari/.test(ua) || /Konqueror/.test(ua))) return;
    if (document.getElementById('map').offsetWidth > 510) return;
    new YAHOO.util.DDMap('map');
    update_tiles(start_x, start_y, true);
});


YAHOO.util.Event.onContentReady('mapForm', function() {
    this.onsubmit = function() {
       if (this.submit_problem) {
            this.onsubmit = function() { return false; };
        }

        this.x.value = fms_x + 2;
        this.y.value = fms_y + 2;
        /*
        if (swfu && swfu.getStats().files_queued > 0) {
            swfu.startUpload();
            return false;
        }
        */
        return true;
    }
});

YAHOO.util.Event.onContentReady('another_qn', function() {
    if (!document.getElementById('been_fixed_no').checked && !document.getElementById('been_fixed_unknown').checked) {
        YAHOO.util.Dom.setStyle(this, 'display', 'none');
    }
    YAHOO.util.Event.addListener('been_fixed_no', 'click', function(e) {
        YAHOO.util.Dom.setStyle('another_qn', 'display', 'block');
    });
    YAHOO.util.Event.addListener('been_fixed_unknown', 'click', function(e) {
        YAHOO.util.Dom.setStyle('another_qn', 'display', 'block');
    });
    YAHOO.util.Event.addListener('been_fixed_yes', 'click', function(e) {
        YAHOO.util.Dom.setStyle('another_qn', 'display', 'none');
    });
});

var timer;
function email_alert_close() {
    YAHOO.util.Dom.setStyle('email_alert_box', 'display', 'none');
}
YAHOO.util.Event.onContentReady('email_alert', function() {
    YAHOO.util.Event.addListener(this, 'click', function(e) {
        if (!document.getElementById('email_alert_box'))
            return true;
        YAHOO.util.Event.preventDefault(e);
        if (YAHOO.util.Dom.getStyle('email_alert_box', 'display') == 'block') {
            email_alert_close();
        } else {
            var pos = YAHOO.util.Dom.getXY(this);
            pos[0] -= 20; pos[1] += 20;
            YAHOO.util.Dom.setStyle('email_alert_box', 'display', 'block');
            YAHOO.util.Dom.setXY('email_alert_box', pos);
            document.getElementById('alert_rznvy').focus();
        }
    });
    YAHOO.util.Event.addListener(this, 'mouseout', function(e) {
        timer = window.setTimeout(email_alert_close, 2000);        
    });
    YAHOO.util.Event.addListener(this, 'mouseover', function(e) {
        window.clearTimeout(timer);
    });
});
YAHOO.util.Event.onContentReady('email_alert_box', function() {
    YAHOO.util.Event.addListener(this, 'mouseout', function(e) {
        timer = window.setTimeout(email_alert_close, 2000);        
    });
    YAHOO.util.Event.addListener(this, 'mouseover', function(e) {
        window.clearTimeout(timer);
    });
});

YAHOO.util.Event.addListener('hide_pins_link', 'click', function(e) {
    YAHOO.util.Event.preventDefault(e);
    if (this.innerHTML == 'Show pins') {
        YAHOO.util.Dom.setStyle('pins', 'display', 'block');
        this.innerHTML = 'Hide pins';
    } else if (this.innerHTML == 'Dangos pinnau') {
        YAHOO.util.Dom.setStyle('pins', 'display', 'block');
        this.innerHTML = 'Cuddio pinnau';
    } else if (this.innerHTML == 'Cuddio pinnau') {
        YAHOO.util.Dom.setStyle('pins', 'display', 'none');
        this.innerHTML = 'Dangos pinnau';
    } else if (this.innerHTML == 'Hide pins') {
        YAHOO.util.Dom.setStyle('pins', 'display', 'none');
        this.innerHTML = 'Show pins';
    }
});
YAHOO.util.Event.addListener('all_pins_link', 'click', function(e) {
    YAHOO.util.Event.preventDefault(e);
    YAHOO.util.Dom.setStyle('pins', 'display', 'block');
    var welsh = 0;
    if (this.innerHTML == 'Include stale reports') {
        this.innerHTML = 'Hide stale reports';
        document.getElementById('all_pins').value = '1';
        load_pins(fms_x, fms_y);
    } else if (this.innerHTML == 'Cynnwys hen adroddiadau') {
        this.innerHTML = 'Cuddio hen adroddiadau';
        document.getElementById('all_pins').value = '1';
        welsh = 1;
        load_pins(fms_x, fms_y);
    } else if (this.innerHTML == 'Cuddio hen adroddiadau') {
        this.innerHTML = 'Cynnwys hen adroddiadau';
        welsh = 1;
        document.getElementById('all_pins').value = '';
        load_pins(fms_x, fms_y);
    } else if (this.innerHTML == 'Hide stale reports') {
        this.innerHTML = 'Include stale reports';
        document.getElementById('all_pins').value = '';
        load_pins(fms_x, fms_y);
    }
    if (welsh) {
        document.getElementById('hide_pins_link').innerHTML = 'Cuddio pinnau';
    } else {
        document.getElementById('hide_pins_link').innerHTML = 'Hide pins';
    }
});

/* File upload */
/*
function doSubmit(e) {
    e = e || window.event;
    if (e.stopPropagation) e.stopPropagation();
    e.cancelBubble = true;
    try {
        if (swfu.getStats().files_queued > 0)
            swfu.startUpload();
        else
            return true;
    } catch (e) {}
    return false;
}

function uploadDone() {
    var m = document.getElementById('mapForm');
    if (m) {
        m.submit();
    } else {
        document.getElementById('fieldset').submit();
    }
}

var swfu;
var swfu_settings = {
    upload_url : "http://matthew.bci.mysociety.org/upload.cgi",
    flash_url : "http://matthew.bci.mysociety.org/jslib/swfupload/swfupload_f9.swf",
    file_size_limit : "10240",
    file_types : "*.jpg;*.jpeg;*.pjpeg",
    file_types_description : "JPEG files",
    file_upload_limit : "0",

    swfupload_loaded_handler : function() {
        var d = document.getElementById("fieldset");
        if (d) d.onsubmit = doSubmit;
    },
    file_queued_handler : function(obj) {
        document.getElementById('txtfilename').value = obj.name;
    },
    file_queue_error_handler : fileQueueError,
//upload_start_handler : uploadStartEventHandler,
    upload_progress_handler : function(obj, bytesLoaded, bytesTotal) {
        var percent = Math.ceil((bytesLoaded / bytesTotal) * 100);
        obj.id = "singlefile";
        var progress = new FileProgress(obj, this.customSettings.progress_target);
        progress.setProgress(percent);
        progress.setStatus("Uploading...");
    },
    upload_success_handler : function(obj, server_data) {
        obj.id = "singlefile";
        var progress = new FileProgress(obj, this.customSettings.progress_target);
        progress.setComplete();
        progress.setStatus("Complete!");
        if (server_data == ' ') {
            this.customSettings.upload_successful = false;
        } else {
            this.customSettings.upload_successful = true;
            document.getElementById('upload_fileid').value = server_data;
        }
    },
    upload_complete_handler : function(obj) {
        if (this.customSettings.upload_successful) {
            var d = document.getElementById('update_post');
            if (d) d.disabled = 'true';
            uploadDone();
        } else {
            obj.id = 'singlefile';
            var progress = new FileProgress(obj, this.customSettings.progress_target);
            progress.setError();
            progress.setStatus("File rejected");
            document.getElementById('txtfilename').value = '';
        }
        
    },
    upload_error_handler : uploadError,

    swfupload_element_id : "fileupload_flashUI",
    degraded_element_id : "fileupload_normalUI",
    custom_settings : {
        upload_successful : false,
        progress_target : 'fileupload_flashUI'
    }
};
*/

// I love the global
var tile_x = 0;
var tile_y = 0;
var tilewidth = 254;
var tileheight = 254;

var myAnim;
function pan(x, y) {
    if (!myAnim || !myAnim.isAnimated()) {
        myAnim = new YAHOO.util.Motion('drag', { points:{by:[x,y]} }, 10, YAHOO.util.Easing.easeOut);
        myAnim.useSeconds = false;
        //myAnim.onTween.subscribe(function(){ update_tiles(x/10, y/10, false); });
        myAnim.onComplete.subscribe(function(){
            update_tiles(x, y, false);
            cleanCache();
        });
        myAnim.animate();
    }
}

var drag_x = 0;
var drag_y = 0;
function update_tiles(dx, dy, force) {
    dx = getInt(dx); dy = getInt(dy);
    if (!dx && !dy && !force) return;
    var old_drag_x = drag_x;
    var old_drag_y = drag_y;
    drag_x += dx;
    drag_y += dy;

    var drag = document.getElementById('drag');
    drag.style.left = drag_x + 'px';
    drag.style.top = drag_y + 'px';

    var horizontal = Math.floor(old_drag_x/tilewidth) - Math.floor(drag_x/tilewidth);
    var vertical = Math.floor(old_drag_y/tileheight) - Math.floor(drag_y/tileheight);
    if (!horizontal && !vertical && !force) return;
    fms_x += horizontal;
    
    tile_x += horizontal;
    fms_y -= vertical;
    tile_y += vertical;
    var url = [ root_path + '/tilma/tileserver/10k-full/', fms_x, '-', (fms_x+5), ',', fms_y, '-', (fms_y+5), '/JSON' ].join('');
    YAHOO.util.Connect.asyncRequest('GET', url, {
        success: urls_loaded, failure: urls_not_loaded,
        argument: [tile_x, tile_y]
    });

    if (force) return;
    load_pins(fms_x, fms_y);
}

function load_pins(x, y) {
    if (document.getElementById('formX')) {
        var ajax_params = [ 'sx=' + document.getElementById('formX').value, 
                            'sy=' + document.getElementById('formY').value, 
                            'x='  + (x+2),
                            'y='  + (y+2), 
                            'all_pins=' +  document.getElementById('all_pins').value ];

	if (document.getElementById('extra_param')) {
            ajax_params.push(document.getElementById('extra_param').name + '=' + document.getElementById('extra_param').value);
        }            

        var separator;
        if (window.Cobrand){
             separator = window.Cobrand.param_separator();
        }else{
             separator = ';';
        }
        var url = [ root_path , '/ajax?', ajax_params.join(separator)].join('');
        YAHOO.util.Connect.asyncRequest('GET', url, {
           success: pins_loaded
        });
    }
}

function pins_loaded(o) {
    var data = eval(o.responseText);
    document.getElementById('pins').innerHTML = data.pins;
    if (typeof(data.current) != 'undefined')
        document.getElementById('current').innerHTML = data.current;
    if (typeof(data.current_near) != 'undefined')
        document.getElementById('current_near').innerHTML = data.current_near;
    if (typeof(data.fixed_near) != 'undefined')
        document.getElementById('fixed_near').innerHTML = data.fixed_near;
}

function urls_not_loaded(o) { /* Nothing yet */ }

// Load 6x6 grid of tiles around current 2x2
function urls_loaded(o) {
    var tiles = eval(o.responseText);
    var drag = document.getElementById('drag');
    for (var i=0; i<6; i++) {
        var ii = (i + o.argument[1]);
        for (var j=0; j<6; j++) {
            if (tiles[i][j] == null) continue;
            var jj = (j + o.argument[0]);
            var id = [ 't', ii, '.', jj ].join('');
            var xx = fms_x+j;
            var yy = fms_y+5-i;
            var img = document.getElementById(id);
            if (img) {
                if (!img.galleryimg) { img.galleryimg = false; }
                img.onclick = drag_check;
                tileCache[id] = { x: xx, y: yy, t: img };
                continue;
            }
            img = cloneNode();
            img.style.top = ((ii-2)*tileheight) + 'px';
            img.style.left = ((jj-2)*tilewidth) + 'px';
            img.name = [ 'tile_', xx, '.', yy ].join('')
            img.id = id;
            if (browser) {
                img.style.visibility = 'hidden';
                img.onload=function() { this.style.visibility = 'visible'; }
            }
            img.src = 'http://tilma.mysociety.org/tileserver/10k-full/' + tiles[i][j];
            tileCache[id] = { x: xx, y: yy, t: img };
            drag.appendChild(img);
        }
    }
}

var imgElCache;
function cloneNode() {
    var img = null;
    if (!imgElCache) {
        var form = document.getElementById('mapForm');
        if (form) {
            img = imgElCache = document.createElement('input');
            img.type = 'image';
        } else {
            img = imgElCache = document.createElement('img');
        }
        img.onclick = drag_check;
        img.style.position = 'absolute';
        img.style.width = tilewidth + 'px';
        img.style.height = tileheight + 'px';
        img.galleryimg = false;
        img.alt = 'Loading...';
    } else {
        img = imgElCache.cloneNode(true);
    }
    return img;
}

var tileCache=[];
function cleanCache() {
    for (var i in tileCache) {
        if (tileCache[i].x < fms_x || tileCache[i].x > fms_x+5 || tileCache[i].y < fms_y || tileCache[i].y > fms_y+5) {
            var t = tileCache[i].t;
            t.parentNode.removeChild(t); // de-leak?
            delete tileCache[i];
        }
    }
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

var in_drag = false;
function drag_check(e) {
    if (in_drag) {
        in_drag = false;
        return false;
    }
    return true;
}

/* Simpler version of DDProxy */
var mouse_pos = {};
YAHOO.util.DDMap = function(id, sGroup, config) {
    this.init(id, sGroup, config);
};
YAHOO.extend(YAHOO.util.DDMap, YAHOO.util.DD, {
    scroll: false,
    b4MouseDown: function(e) { },
    startDrag: function(x, y) {
        mouse_pos = { x: x, y: y };
        setCursor('move');
        in_drag = true;
    },
    b4Drag: function(e) { },
    onDrag: function(e) {
        var point = get_posn(e);
        if (point == mouse_pos) return false;
        var dx = point.x-mouse_pos.x;
        var dy = point.y-mouse_pos.y;
        mouse_pos = point;
        update_tiles(dx, dy, false);
    },
    endDrag: function(e) {
        setCursor('crosshair');
        cleanCache();
    },
    toString: function() {
        return ("DDMap " + this.id);
    }
});

var browser = 1;
var ua=navigator.userAgent.toLowerCase();
if (!/opera|safari|gecko/.test(ua) && typeof document.all!='undefined')
    browser=0;

function getInt(n) {
    n = parseInt(n); return (isNaN(n) ? 0 : n);
}

