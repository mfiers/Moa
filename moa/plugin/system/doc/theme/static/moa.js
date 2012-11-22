function UrlExists(url) {
	var http = new XMLHttpRequest();
	http.open('HEAD', url, false);
	http.send();
	return http.status != 404;
}

window.onload = function () {
	var winloc = window.location
	var all = document.getElementsByTagName("a");
	for (var i=0; i < all.length; i++) {
		var a = all[i];
		if (a.hostname == winloc.hostname &&
			a.port == winloc.port &&
			a.protocol == winloc.protocol) {
			var url = a.getAttribute("href");
			if (url.indexOf('category/') !== -1) {
				newurl = url.replace('category/', 'category_')
				a.href=newurl
				url = newurl
			}
			if (a.protocol != 'file:') {
				if (! UrlExists(url)) {
					a.className = a.className + " moaDoesNotExist";
				}
			}
		}
	}
}