<html>
<body>
<script>
function imitateClick(oElement,iClientX,iClientY){
	var oEvent;
	if (document.createEventObject) {
		oEvent=document.createEventObject();
		oEvent.clientX=iClientX;
		oEvent.clientY=iClientY;
		oElement.fireEvent("onclick",oEvent);
	}else{
		oEvent=document.createEvent("MouseEvents");
		oEvent.initMouseEvent("click",true,true,document.defaultView,0,0,0,iClientX,iClientY);
		oElement.dispatchEvent(oEvent);
	}
}
var body=document.body;
body.οnclick=function(event){
	alert("clicked at("+event.clientX+","+event.clientY+")");
};
imitateClick(body,100,100);
</script>
</body>
</html>

