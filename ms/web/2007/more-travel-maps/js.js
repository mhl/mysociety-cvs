function queryToHash(q) {
    var newh = new Array();
    var vars = q.replace(/#/, "").split("&");
    for (var i=0;i<vars.length;i++) {
        var pair = vars[i].split("=");
        newh[pair[0]] = pair[1];
    }
    return newh
}

function hashToQuery(h) {
    q = "";
    for (var i in h) {
        if (i != "") {
            q = q + i + "=" + h[i] + "&";
        }
    }
    return "#" + q
}

function setHash(h) {
    curh = queryToHash(location.hash);
    newh = queryToHash(h);
    for (var i in newh) {
        curh[i] = newh[i];
    }
    location.hash = hashToQuery(curh);
}

function getHash() {
    return location.hash;
}

