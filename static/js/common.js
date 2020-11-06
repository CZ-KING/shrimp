$(function(){


    $('#QESinput').focus(function(){
    	$('#makeQuestion').css({'display':'none'});
    	$('.search_detail_box').show();
		$(this).css('width','300px');
	})

	 $('#QESinput').blur(function(){
		$('#makeQuestion').css({'display':'block'});
		$('.search_detail_box').hide();
		$(this).css('width','250px');
	})

    $('#QESinput').keypress(function(event){
        if (event.which == 13) {
           var question = $(this).val();
		   window.location.href= "/search?query="+question;
        }
	})


	$('.profile_img_box').click(function(){
		$('span.menu_arrow').toggle();
		$('.user_profile_menu').toggle();
	})

	$('div span.comment').click(function(){
		$('.comment_wrapper').css('display','flex');
		$('.make_question_container').hide();
		$('.comments_container').show();

	})

	$('span.comment-close').click(function(){
		$('.comment_wrapper').hide();
		$('.comments_container').hide();
	});

	$('#makeQuestion').click(function(){
		$('.modal_wrapper').css('display','flex');
		$('.make_question_container').show();
	});

	$('span.close').click(function(){
		$('.modal_wrapper').hide();
		$('.make_question_container').hide();
	});

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

	$('.submit_btn button').click(function(){
		var data = {
            question_id: question_id,
            user_id: user_id,
            user_token: user_token,
            nickname: nickname,
            slogan: slogan,
            answer: answer
        };

		$.ajax({
	        url: '/question/',
	        type: 'post',
	        data: data,
	        success: function(res){
	            console.log(res);
	            if(res.code == 0){
	               $('.modal_wrapper').hide();
					$('.make_question_container').hide();
			  			setTimeout(function(){
			  				slideTips('提问成功');
			  			},800);
				}
	        }


	    })
	})
	$('.comment button').click(function(){
		var data = {
            answer_id: 1,
            page:1

        };

		$.ajax({
	        url: '/comment/',
	        type: 'get',
	        data: data,
	        success: function(res){
	            console.log(res);
	            if(res.code == 0){
	               $('.modal_wrapper').hide();
					$('.make_question_container').hide();
			  			setTimeout(function(){
			  				slideTips('提问成功');
			  			},800);
				}
	        }


	    })
	})
})