//点击隐藏或显示密码
window.onload = function(){
    var btn = document.getElementById('im-black-eye');
    var pwd = document.getElementById('password');
    btn.onmousedown = function () {
        pwd.type = "text";
        this.classList.remove('fa-eye-slash');
        this.classList.add('fa-eye');
    }
    btn.onmouseup = function () {
        pwd.type = "password";
        this.classList.remove('fa-eye');
        this.classList.add('fa-eye-slash');
    }
}

$(function () {
    var timestamp = (new Date()).getTime();

    function slideTips(txt){
        var tips_box_el = $('.show-tips-container');

        if (tips_box_el.hasClass('slide-down')){
             return;
        }else{
            tips_box_el.addClass('slide-down').find('p').text(txt);
        }
        if (tips_box_el.hasClass('slide-down')){
            setTimeout(function () {
                tips_box_el.removeClass('slide-down');
            }, 3000);
        }
    }

    //登录密码或者验证码切换
    $('.a-for-captcha-login').click(function(){
        var times = null;
        var cap = $('.captcha-input').css('display');
        if(cap == 'none'){
            $('.captcha-input').show();
            $('.password-input').hide();
            $(this).text('切换到密码登录');
            $('.operation-tips-text a').attr('href','javascript:;').text('获取不到验证码？').addClass('woaini');
            $('input[name="password"]').val('');
            $('span.pwd_tips').hide();
            $('#password').css({
                'border-bottom':'1px solid #ddd'
            });
            
        }else{
            $('.captcha-input').hide();
            $('.password-input').show();
            $(this).text('手机验证码登录');
            $('.operation-tips-text a').attr('href','forget.html').text('忘记密码').removeClass('woaini');
            $('input[name="captcha"]').val('');
        }
    })

    //红色警告
    function LgTips(val){
        $('span.' + val).fadeIn(400).css({
        'font-size': '14px',
        'color': '#f1403c',
        'width': '100%',
        'display': 'block',
        'text-align': 'left',
        'margin-top': '-10px'
        });
    }

    //手机号为空时警告
    $('input[name="phone"]').blur(function(){
        if($(this).val() == ''){
            LgTips('lg_tips');
            $('#phone').css({
                'border-bottom':'1px solid #f1403c',
                'transition': '0.7s'
            });
            $('span.lg_tips').text('还没有输入手机号呢 -_-');
        }else if($(this).val().length < 11){
             LgTips('lg_tips');
             $('#phone').css({
                'border-bottom':'1px solid #f1403c',
                'transition': '0.7s'
            });
            $('span.lg_tips').text('手机格式不正确 -_-');
        }else{
            $('span.lg_tips').css('display','none');
            $('#phone').css({
                'border-bottom':'1px solid #ddd'
            });
        }
    })

     //下滑框提示功能
    function slideTips(text){
        $('.slide_tips').text(text).css('top','5px');
        setTimeout(function(){ $('.slide_tips').css('top','-55px') },2000);
    }

    //密码为空时警告
    $('input[name="password"]').blur(function(){
        if($(this).val() == ''){
            LgTips('pwd_tips');
            $('#password').css({
                'border-bottom':'1px solid #f1403c',
                'transition': '0.7s'
            });
        }else{
            $('span.pwd_tips').css('display','none');
            $('#password').css({
                'border-bottom':'1px solid #ddd'
            });
        }
    })

    //ajax数据提交
    function LgAjax(data){
        console.log(data);

        $.ajax({
            url: '/login/',
            type: 'post',
            data: data,
            success: function(res){
                console.log(res);
                if(res.code == 1){
                    slideTips('请输入正确的邮箱地址或登录密码');
                }else if(res.code == 6){
                    slideTips('用户不存在');
                }
				else if(res.code == 0){
                  window.location.href = "/";
                     
                }
            }
        })
    }

    //验证码倒计时功能
    var vilidCode = true;
    $('span.captcha-control').click(function(){
        var countdown = 60;
        var $captcha = $(this);
        var phone = $('input[name=phone]').val();
        if(phone == '' || phone.length < 25){
            slideTips('请先输入正确的手机号码');
        }else{
            $.ajax({
                url: '/sms/',
                type: 'post',
                data: {
                    phone: phone,
                    timestamp: timestamp
                },
                success: function(res){
                    console.log(res);
                    if(res.code == 0){
                        if(vilidCode){
                            vilidCode = false;
                            var t =setInterval(function(){
                                countdown--;
                                $captcha.html(countdown+'秒重新获取');
                                if(countdown==0){
                                    clearInterval(t);
                                    $captcha.html('获取验证码');
                                    vilidCode = false;
                                }
                            },1000)
                        }
                    }
                }
            })
        }
    })

    //登录功能
    $('#login_btn').click(function(){
        var email = $('input[name="email"]').val();
        var pwd = $('input[name="password"]').val();
        var captcha = $('input[name="captcha"]').val();
        var condition = $('#captcha').is(':visible');
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
		var data = {
            veri_type:1,
			timestamp: timestamp,
            username: email,
            secret_key: pwd,
            
			'csrfmiddlewaretoken': csrf
        };

        if(condition === false){
            if(email == ''){
                slideTips('请输入邮箱地址');
                return false;
            }else if(pwd == ''){
                slideTips('请输入密码');
                return false;
                
            }else{
                LgAjax(data);
            }
        }else{
            if(email == ''){
                slideTips('请输入邮箱地址');
                return false;
            }else if(email.length < 10){
                slideTips('请输入正确的邮箱地址');
                return false;
            }
            else if(captcha == ''){
                slideTips('请先填写验证码');
                return false;
            }
            else if(email != '' && captcha != ''){
                LgAjax(data);
                console.log('验证码登录');
            }
        }
    })
})