var mySwiper=new Swiper(".swiper-container",{direction:"vertical",loop:false,speed:1200,on:{init:function(){move(".page0-text-div").set("opacity","1").duration("5s").end()},touchStart:function(a){if(this.activeIndex<11){document.getElementById("person").hidden=true;document.getElementById("person-jump").hidden=false}else{document.getElementById("person").hidden=true;document.getElementById("person-jump").hidden=true}},transitionEnd:function(){if(this.activeIndex<11){document.getElementById("person").hidden=false;document.getElementById("person-jump").hidden=true}else{document.getElementById("person").hidden=true;document.getElementById("person-jump").hidden=true}},slideChange:function(){move(".page"+this.activeIndex+"-text-div").set("opacity","1").duration("5s").end();if(this.activeIndex==6){chart.restart()}else{if(this.activeIndex==9){$(".bar").each(function(a,b){drawBar(b)})}}},}});var $audio=$("#media")[0];wx.config({debug:false,appId:"",timestamp:(new Date()).getTime(),nonceStr:"",signature:"",jsApiList:["checkJsApi"]});wx.ready(function(){$audio.play()});var x=document.getElementById("media");$(function(){$("#audio_btn").click(function(){$(this).toggleClass("rotate");if($(this).hasClass("rotate")){x.play()}else{x.pause()}})});var input=document.getElementById("input_msg");var btn_submit=document.getElementById("btn_submit");btn_submit.onclick=function(){fly.get("/schoollifemsg",{msg:input.value,userid:userid}).then(function(){alert("留言成功");input.disabled=true;btn_submit.hidden=true})};var btn_biwan=document.getElementById("btn-biwan");btn_biwan.onclick=function(){move("#btn-biwan").set("margin-left","100px").duration("0.5s").end();setTimeout(function(){fly.get("/wenyi");window.open(wenyi_url)},500)};function makePic(b,c){var a=new Image();a.src=b;a.onload=function(){var g=document.createElement("canvas");g.width=a.width;g.height=a.height;var d=g.getContext("2d");d.drawImage(a,0,0);d.font="38px Arial";d.fillText("我是第"+count+"个打开这份记录的人",135,185);d.font="35px Arial";var h=350;for(var f=0;f<c.length;f++){d.fillText(c[f],60,h);h+=80}var e=g.toDataURL("image/png",1);document.getElementById("share-img").src=e}}var btn_share=document.getElementById("btn_change");var shareListLength=shareList.length;makePic(shareList[index%shareListLength].img,shareList[index%shareListLength].text);index+=1;btn_share.onclick=function(){makePic(shareList[index%shareListLength].img,shareList[index%shareListLength].text);index+=1};