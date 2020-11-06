$(function () {

     $('div.comments_footer_box').click(function(){
       var comment = $('input[name="comment"]').val();
       var answer_id = $("div.contentItem_answerItem").attr("data-answer-id");
       var url_token = $("li#urltoken").attr("data-urltoken");

       var username = $("div.user_profile_menu").attr("data-nickname");

       var csrf = $('input[name="csrfmiddlewaretoken"]').val();

       $.ajax({
                url: '/comment/',
                type: 'post',
                data: {
					url_token:url_token,
                    comment:comment,
                    username: username,
                    answer_id: answer_id,
                    'csrfmiddlewaretoken': csrf
                },
                success: function(res){
                    if(res.code == 0){
                        window.location.href="/";
                    }
                }
            })
    })

})