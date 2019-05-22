var mySwiper = new Swiper('.swiper-container', {
        direction: 'vertical', // 垂直切换选项
        loop: false, // 循环模式选项
        speed: 1200,
        on: {
            // 处理小人跳跃逻辑
            touchStart: function (e) {
                document.getElementById("person").hidden=true
                document.getElementById("person-jump").hidden=false
            },
            transitionEnd: function () {
                document.getElementById("person").hidden=false
                document.getElementById("person-jump").hidden=true
            },
            slideChange: function () {
                if(this.activeIndex==0){
                    move("page0-text")
                        .set('opacity', '1')
                        .duration("2s")
                        .end()
                }
                else if (this.activeIndex == 2) {
                    move('.text')
                    .set('opacity', '1')
                    .end();
                    $('.text')
                    .fitText(3.2, { minFontSize: '45px', maxFontSize: '50px' })
                    .textillate({
                        loop: false,
                        in: { effect: 'flipInX' }
                    });
                } else if (this.activeIndex == 3) {
                    var myImage = document.getElementById("canvas");
                    var cxt = myImage.getContext("2d");
                    var img = new Image();
                    img.src = "static/2019SchoolLife/img/123.jpg";
                    img.onload = function () {
                        cxt.drawImage(img, 0,0);
                        cxt.strokeText("要写的文字", 50, 50);
                    };
                    cxt.font = "30px bold 黑体";
                        // 设置颜色
                        cxt.fillStyle = "#111111";
                        // 设置水平对齐方式
                        cxt.textAlign = "center";
                        // 设置垂直对齐方式
                        cxt.textBaseline = "middle";
                        // 绘制文字（参数：要写的字，x坐标，y坐标）
                        // Converts canvas to an image
                        var img = document.getElementById("saveimg");
                        var tempSrc = canvas.toDataURL("image/png");
                        img.src=tempSrc;
                        person.hidden=true
                    }
                    else if (this.activeIndex == 4) {
                        jQuery('.skillbar').each(function(){
                            jQuery(this).find('.skillbar-bar').animate({
                                width:jQuery(this).attr('data-percent')
                            },6000);
                        });
                    }
                },
            }
        })

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
        window.onload = function() {
            draw();
            var saveButton = document.getElementById("saveImageBtn");
            bindButtonEvent(saveButton, "click", saveImageInfo);
            var dlButton = document.getElementById("downloadImageBtn");
            bindButtonEvent(dlButton, "click", saveAsLocalImage);
        };
        function draw(){
            var myImage = document.getElementById("thecanvas");
            var cxt = myImage.getContext("2d");
            var img = new Image();
            img.src = "static/2019SchoolLife/img/123.jpg";
            img.onload = function () {
                cxt.drawImage(img, 0,0);
                cxt.strokeText("要写的文字", 50, 50);
            };
            cxt.font = "15px bold 黑体";
                        // 设置颜色
                        cxt.fillStyle = "#111111";
                        // 设置水平对齐方式
                        cxt.textAlign = "center";
                        // 设置垂直对齐方式
                        cxt.textBaseline = "middle";
                        // 绘制文字（参数：要写的字，x坐标，y坐标）
                        // Converts canvas to an image
                    };

                    function bindButtonEvent(element, type, handler)
                    {
                        if(element.addEventListener) {
                            element.addEventListener(type, handler, false);
                        } else {
                            element.attachEvent('on'+type, handler);
                        }
                    }

                    function saveImageInfo ()
                    {
                        var img = document.getElementById("save_img");
                        var mycanvas = document.getElementById("thecanvas");
                        var image    = mycanvas.toDataURL("image/png");
                        img.src = 'image';
                        var w=window.open('about:blank','image from canvas');
                        w.document.write("<center><img src='"+image+"' alt='from canvas'/></center>");
                    }

                    function saveAsLocalImage () {
                        var myCanvas = document.getElementById("thecanvas");
        // here is the most important part because if you dont replace you will get a DOM 18 exception.
        // var image = myCanvas.toDataURL("image/png").replace("image/png", "image/octet-stream;Content-Disposition: attachment;filename=foobar.png");
        var image = myCanvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
        window.location.href=image; // it will save locally
    }