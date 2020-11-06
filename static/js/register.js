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

    //验证码倒计时功能
    var vilidCode = true;
    $('span.captcha-control').click(function(){
        var countdown = 60;
        var $captcha = $(this);
        var phone = $('input[name=phone]').val();
        var tips_box_el = $('.show-tips-container');
        if(phone == '' || phone.length < 11){
            slideTips('请输入正确的手机号码');
            // tips_box_el.addClass('slide-down').find('p').text('请输入正确的手机号码');
        }else{
            var csrf = $('input[name="csrfmiddlewaretoken"]').val();
            $.ajax({
                url:'/api/sms/',
                type: 'post',
                data: {
                    phone_number: phone,
                    'csrfmiddlewaretoken': csrf
                },
                success: function(res){
                    console.log(res);
                    if(res.code == 9){
                        slideTips('请60秒后再重新获取');
                        // tips_box_el.addClass('slide-down').find('p').text('请60秒后再重新获取');
                    }else if(res.code == 0){
                         $('input[name=captcha]').val(res.data.captcha);
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

    //注册表单提交功能
    $('#im-register-btn').click(function () {
        var email = $('input[name="email"]').val();
        var captcha = $('input[name="captcha"]').val();
        var pwd = $('input[name="password"]').val();
        var tips_box_el = $('.show-tips-container');
		var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        var agreed = $('.i-agree').attr('agreed');
        var data = {
            timestamp: timestamp,
            username: email,
            secret_key: pwd,
			nickname:"小梁",
			register_type:1,
           'csrfmiddlewaretoken': csrf
        };
		
	
        if (email == '') {
            slideTips('请输入邮箱地址');
            // tips_box_el.addClass('slide-down').find('p').text('请输入手机号码');
        } else if (pwd == '') {
            slideTips('请输入注册密码');
            // tips_box_el.addClass('slide-down').find('p').text('请输入验证码');
        
        }else if(typeof(agreed) === 'undefined'){
            slideTips('请先同意用户协议');
            // tips_box_el.addClass('slide-down').find('p').text('请先同意用户协议');
        }else{
            $.ajax({
                url: '/register/',
                type: 'post',
                data: data,
                success: function(res){
                    console.log(res);
                    if(res.code == 1){
                        tips_box_el.addClass('slide-down').find('p').text('手机号或验证码无效');
                    }else if(res.code == 5){
                        tips_box_el.addClass('slide-down').find('p').text('手机号已注册');
                    }else if(res.code == 10){
                        tips_box_el.addClass('slide-down').find('p').text('请求非法');
                    }else if(res.code == 0){
                        tips_box_el.addClass('slide-down').css('background','rgba(255,182,61,.8)').find('p').text('欢迎加入虾问大家庭:)');
                        setTimeout(function(){
                            window.location.href = "/login/";
                        },3500);
                    }
                }
            })

            
        }

        // if (tips_box_el.hasClass('slide-down')) {
        //     setTimeout(function () {
        //         tips_box_el.removeClass('slide-down');
        //     }, 3000);
        // }

        console.log(agreed);
    })

    $('.i-agree').click(function () {
        $(this).attr('agreed','agreed').children('span').show();
    });
})