// 控制声音播放部分
var $audio = $('#media')[0];
wx.config({
    debug: false, // 这里为false
    appId: '', // 以下随意填写即可
    timestamp: (new Date()).getTime(),
    nonceStr: '',
    signature: '',
    jsApiList: ['checkJsApi']
});
wx.ready(function () {
    $audio.play();
});
var x = document.getElementById("media");
$(function () {

    $("#audio_btn").click(function () {
        $(this).toggleClass("rotate"); //控制音乐图标 自转或暂停

        //控制背景音乐 播放或暂停
        if ($(this).hasClass("rotate")) {
            x.play();
        } else {
            x.pause();
        }
    })
});

// 控制提交评论
var input=document.getElementById("input")
var btn_submit=document.getElementById("btn_submit")
btn_submit.onclick = function () {
    fly.get("/schoollifemsg", {
        msg: input.value
    })
        .then(function () {
            alert("留言成功")
            input.hidden = true
            btn_submit.hidden=true
        })
}

// 毕晚按钮
var btn_biwan=document.getElementById("btn-biwan")
btn_biwan.onclick=function () {
    move("#btn-biwan")
        .set("margin-left","100px")
        .duration("0.5s")
        .end()
    setTimeout(function () {
        window.open("/schoollife")
    },500)
}

// 控制渲染分享海报
function makePic(img_url,text) {
    var img = new Image()
    img.src = img_url;
    img.onload = function () {
        var myCanvas = document.createElement("canvas")
        myCanvas.width = 643
        myCanvas.height = 1094
        var ctx = myCanvas.getContext("2d")
        ctx.drawImage(img, 0, 0);
        ctx.font = "30px Arial";
        ctx.fillText(text, 200, 150);
        var url = myCanvas.toDataURL("image/png", 1)
        document.getElementById("share-img").src = url
    }
}

var btn_share=document.getElementById("btn_change")
btn_share.onclick=function(){
    index+=1
    makePic(shareList[index%2].img,shareList[index%2].text)
}

// 翻页控制逻辑
var mySwiper = new Swiper('.swiper-container', {
    direction: 'vertical', // 垂直切换选项
    loop: false, // 循环模式选项
    speed: 1200,
    on: {
        // 首页文字动画
        init: function () {
            move(".page0-text-div")
                .set('opacity', '1')
                .duration("5s")
                .end()
        },
        // 处理小人跳跃逻辑
        touchStart: function (e) {
            document.getElementById("person").hidden = true
            document.getElementById("person-jump").hidden = false
        },
        transitionEnd: function () {
            document.getElementById("person").hidden = false
            document.getElementById("person-jump").hidden = true
        },
        slideChange: function () {
            move(".page" + this.activeIndex + "-text-div")
                .set('opacity', '1')
                .duration("5s")
                .end()
            if (this.activeIndex == 6) {
                chart.restart();
            } else if (this.activeIndex == 9) {
                $('.bar').each(function (i, elem) {
                    drawBar(elem);
                });
            }
        },
    }
})