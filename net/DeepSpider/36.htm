var AJAX={
	http_request:false,
	DivObj:null,
	waitstate:null,
	success:null,
	get:function (divid,url) {
		AJAX.http_request = false;
		AJAX.DivObj = document.getElementById(divid);
		if(window.XMLHttpRequest) { //Mozilla 浏览器
			AJAX.http_request = new XMLHttpRequest();
			if (AJAX.http_request.overrideMimeType) {//设置MiME类别
				AJAX.http_request.overrideMimeType('text/xml');
			}
		}else if (window.ActiveXObject) { // IE浏览器
			try {
				AJAX.http_request = new ActiveXObject("Msxml2.XMLHTTP");
			} catch (e) {
				try {
					AJAX.http_request = new ActiveXObject("Microsoft.XMLHTTP");
				} catch (e) {}
			}
		}
		if (!AJAX.http_request) {
			window.alert("不能创建XMLHttpRequest对象实例.");
			return false;
		}
		AJAX.http_request.onreadystatechange = AJAX.processRequest;
		AJAX.http_request.open("GET", url+"&"+Math.random(), true);
		AJAX.http_request.send(null);
	},
	post:function (divid,url,postvalue) {
		AJAX.http_request = false;
		AJAX.DivObj = document.getElementById(divid);
		if(window.XMLHttpRequest) { //Mozilla 浏览器
			AJAX.http_request = new XMLHttpRequest();
			if (AJAX.http_request.overrideMimeType) {//设置MiME类别
				AJAX.http_request.overrideMimeType('text/xml');
			}
		}else if (window.ActiveXObject) { // IE浏览器
			try {
				AJAX.http_request = new ActiveXObject("Msxml2.XMLHTTP");
			} catch (e) {
				try {
					AJAX.http_request = new ActiveXObject("Microsoft.XMLHTTP");
				} catch (e) {}
			}
		}
		if (!AJAX.http_request) {
			window.alert("不能创建XMLHttpRequest对象实例.");
			return false;
		}
		AJAX.http_request.onreadystatechange = AJAX.processRequest;
		AJAX.http_request.open("POST", url , true);
		AJAX.http_request.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
		AJAX.http_request.send(poststr);
	},
    processRequest:function () {
        if (AJAX.http_request.readyState == 4) {
            if (AJAX.http_request.status == 200) {
				if(AJAX.DivObj!=null){
					AJAX.DivObj.innerHTML=AJAX.http_request.responseText;
				}
            } else {
                alert("您所请求的页面有异常。");
            }
        }else{
			if(AJAX.DivObj!=null){
				AJAX.DivObj.innerHTML='<hr>请等待...<hr>';
			}
		}
    }
}
function makesmallpic(obj,w,h){
	var srcImage = new Image();
	srcImage.src=obj.src;
	var srcW=srcImage.width;		
	var srcH=srcImage.height;

	if (srcW==0)
	{
		obj.src=srcImage.src;
		srcImage.src=obj.src;
		var srcW=srcImage.width;		
		var srcH=srcImage.height;
	}
	if (srcH==0)
	{
		obj.src=srcImage.src;
		srcImage.src=obj.src;
		var srcW=srcImage.width;		
		var srcH=srcImage.height;
	}

	if(srcW>srcH){
		if(srcW>w){
			obj.width=newW=w;
			obj.height=newH=(w/srcW)*srcH;
		}else{
			obj.width=newW=srcW;
			obj.height=newH=srcH;
		}
	}else{
		if(srcH>h){
			obj.height=newH=h;
			obj.width=newW=(h/srcH)*srcW;
		}else{
			obj.width=newW=srcW;
			obj.height=newH=srcH;
		}
	}
	if(newW>w){
		obj.width=w;
		obj.height=newH*(w/newW);
	}else if(newH>h){
		obj.height=h;
		obj.width=newW*(h/newH);
	}
}