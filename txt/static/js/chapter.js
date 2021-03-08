$(function(){

    //滚动速度
    var speed;
    var waitnextchapter = $('.waitnextchapter');
    var isLoading = false;
    var room = window.location.pathname.split('/')[2];

    if (/Android|webOS|iPhone|iPod|BlackBerry/i.test(navigator.userAgent)) {
        //移动端
        speed = 20;
    } else {
        //pc端
        speed = 40;
    }

    //禁止右键菜单
    document.oncontextmenu = function () {
        event.returnValue = false;
    };

    // 唤出工具栏
    isAutoScroll = false;

    // 滚动自动隐藏工具栏
    $(window).scroll(function(event){
        if(!isAutoScroll){
            $('.mainoper').hide();
        }
    });
    show_or_hide_tool_bar();

    //定义自动滚动函数，调用时根据滚动状态去调用，防止每次开始先滚动几秒

    //监听滚动事件，判断是否加载下一章
    $(window).scroll(function () {
        getNextChapter();
    })

    //滚动加载下一章
    function getNextChapter(){
        var scrollTop = $(window).scrollTop();
        var scrollHeight = $(document).height();
        var windowHeight = $(window).height();
        var restHeight = scrollHeight - scrollTop - windowHeight;
        if (restHeight <= 100 && isLoading == false) {
            isLoading = true;
            waitnextchapter.show();
            var currid = $('#currid');
            var currchapterid = parseInt(currid.val());
            var isNext = addNextChapter(room, currchapterid + 1);
            if(isNext){
                currid.val(currchapterid + 1);
                isLoading = false;
                waitnextchapter.hide();
            }
        }else if(restHeight > 100 && isLoading == true){
            isLoading = false;
        }
    }
    //加载某一章，操作div，包括增加新的和删除老的
    function addNextChapter(room, chapterid){
        var chapter = getchapterbyid(room, chapterid);
        if(chapter){
            title = chapter.title;
            content = chapter.content;
            //添加新章节div
            var nextContent = $('<div class="content notranslate"></div>');
            var jumbotron = $($('.jumbotron')[0]);
            var cssfontSize = $('.content:last p').css('font-size');
            isDay = $('#turnday').attr('day');
            jumbotron.append($('<h3>'+chapter.title+'</h3>'));
            jumbotron.append(nextContent);
            for(var i = 0; i < content.length; i++){
                var newp = $('<p>'+content[i]+'</p>');
                newp.css('font-size', cssfontSize);
                nextContent.append(newp);
            }
            setDayStyle(isDay);

            // 删除上上上上章前面的div
            while($('.content').length > 10){
                $($('.content')[0]).remove();
                $($('h3')[0]).remove();
            }

            //修改全局变量
            document.title = chapter.title;
            var nexta = $('#next');
            $('#preC').attr('href', '/content/' +room +'/' + str(chapterid-1));
            nexta.attr('href', '/content/'+room +'/' + str(chapterid + 1));
            //修改地址栏
            var stateObject = {};
            $('#title').text(title);
            var newUrl = "/content/" + room + "/" + (chapterid + 1);
            //修改从项目名后开始
            history.pushState(stateObject,title,newUrl);
            return true;
        }
        return null;
    }
    //加载某一章，纯请求
    function getchapterbyid(room, chapterid){
        var chapter;
        $.ajax({
            url: '/content/' + room + '/' + chapterid,
            type: 'POST',
            async: false,
            success: function(data){
                if(data.code==0){
                    chapter = data.data;
                }else{
                    toastr.error('未正确返回数据')
                }
            },
            error: function(data){
                toastr.error('请求失败')
                waitnextchapter.val('网络可能断了');
            }
        });
        return chapter;
    }



    $('#turnday').click(function () {
        isDay = $('#turnday').attr('day');
        if(isDay == 'day'){
            isDay = 'night';
        }else{
            isDay = 'day';
        }
        setDayStyle(isDay);
    });

    $('#fontup').click(function () {
        var cssfontSize = $('.content:last p').css('font-size');
        var unit = cssfontSize.slice(-2);
        var fontSize = parseFloat(cssfontSize);
        $('.content:last p').css('font-size', (fontSize + 1) + unit);
        setFontsize2Base(fontSize + 1);
    })

    $('#fontdown').click(function () {
        var cssfontSize = $('.content:last p').css('font-size');
        var unit = cssfontSize.slice(-2);
        var fontSize = parseFloat(cssfontSize);
        $('.content:last p').css('font-size', (fontSize - 1) + unit);
        setFontsize2Base(fontSize - 1);
    })

    function setFontsize2Base(size) {
        $.ajax({
            url: '/setfont/' + size,
            method: 'GET',
        })
    }

    //将颜色模式汇报至base
    function setDay2Base(isDay) {
        $.ajax({
            url: '/setDay/' + isDay,
            type: 'GET'
        });
    }

    //设置颜色模式
    function setDayStyle(isDay) {
        if (isDay == 'night') {
            //切换成黑夜模式
            $("html, body").css("backgroundColor", "#17181a");
            $(".jumbotron").css("backgroundColor", "#17181a");
            $(".mainoper").css("backgroundColor", "#0d0d0d");
            $(".content").css("backgroundColor", "#1f2022");
            $(".content").css("color", "#cbced3");
            if (/Android|webOS|iPhone|iPod|BlackBerry/i.test(navigator.userAgent)) {
                $(".content").css("backgroundColor", "#030303");
                $(".content").css("color", "#a6a6a6");
            }
            $('.fontsize').css('color', '#939392');
            $('#turnday').css('background-color', '#e7e7e7');
            $('#turnday').css('color', 'black');
            $('#turnday').attr('day', 'night');
            $('#dayimg').attr('src', '/static/imgs/day.png');
            setDay2Base('night');
        } else if (isDay == 'day') {
            //切换成白天模式
            $("html, body").css("backgroundColor", "#bfbfbf");
            $(".jumbotron").css("backgroundColor", "#f2f2f2");
            $(".mainoper").css("backgroundColor", "#f2f2f2");
            $(".content").css("backgroundColor", "#d9d9d9");
            $(".content").css("color", "black");
            $('.fontsize').css('color', 'black');
            $('#turnday').attr('day', 'day');
            $('#turnday').css('background-color', '#555555');
            $('#turnday').css('color', '#939392');
            $('#dayimg').attr('src', '/static/imgs/dark.png');
            setDay2Base('day');
        }
    }

    $('#toTop').click(function () {
        $('html,body').animate({ scrollTop: 0 }, 500);
    });


    $('.content').click(function(event) {
        $(".catalog").hide();
    });
    $('.catalog').click(function(e){
        //取消点击关闭事件冒泡
        e.stopPropagation();
    });

    //加载目录
    $('.context').click(function(e){
        //取消点击关闭事件冒泡
        e.stopPropagation();
        let that = $('.catalog');
        if(that.css("display")=="none"){
            if($('.catalog>ul li').length ==0){
                $.ajax({
                    url: '/catalog/' + room,
                    type: 'POST',
                    success: function(data){
                        var ul = $($('.catalog>ul')[0]);
                        ul.find("li").remove();
                        for(var i=0; i<data.catalogs.length;i++){
                            var li = '<a href="/content/'+room+'/' + data.catalogs[i][0] + '"><li class="list-group-item" style="background-color:black">' + data.catalogs[i][1] + '</li></a>';
                            if(data.his == data.catalogs[i][0]){
                                li = '<a id="curr" ><li class="list-group-item  active">' + data.catalogs[i][1] + '</li></a>';
                            }
                            ul.append($(li));
                        }
                        that.show();
                        $(".catalog").animate({scrollTop:$("#curr").offset().top - $(".catalog").offset().top + $(".catalog").scrollTop()},100)
                    }
                });
            }else{
                that.show();
            }

        }else{
            that.hide();
        }
    });

    //移动端禁止双指缩放
    document.addEventListener('gesturestart', function (event) {
        event.preventDefault();
    });
});

//禁止调试
function checkDebugger(){
    const d=new Date();
    debugger;
    const dur=Date.now()-d;
    if(dur<5){
        //5ms内打断点
        return false;
    }else{
        return true;
    }
}
function breakDebugger(){
    if(checkDebugger()){
        breakDebugger();
    }
}
function show_or_hide_tool_bar(){
    $('.content').click(function(){
        if($('.mainoper').is(':hidden')){
            $('.mainoper').show();
        }else{//否则
            $('.mainoper').hide();
        }
    })
}
