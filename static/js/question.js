$(function () {

    $('div#answer_box').hide();
    $('span.write-answer').click(function(){
        $('div#answer_box').show();
    })


    $('div.submit_btn').click(function(){
        var userid = $("div.user_profile_menu").attr("data-userid");
        var username = $("div.user_profile_menu").attr("data-nickname");
        var question_title = $('textarea[name=question_title]').val();


        var question_description = $('textarea[name=question_description]').val();
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();

        if(question_title == ''){
            slideTips('请先输入问题标题');
        }else{
            $.ajax({
                url: '/question/',
                type: 'post',
                data: {
                    userid: userid,
                    username: username,
                    title: question_title,
                    description: question_description,
                    classfication:"[0,1]",
                    'csrfmiddlewaretoken': csrf
                },
                success: function(res){
                    console.log(res);
                    if(res.code == 0){
                        window.location.href="/question/"+res.data.question_id+"/"
                    }
                }
            })
        }
    })


     $('div.setting_submit_group').click(function(){
       // var content = $("div#my_editor").val();

       var content = $('div#my_editor').trumbowyg('html');
       var userid = $("div.user_profile_menu").attr("data-userid");
	   var question_id = $("div.title_box").attr("data-qid");
	   var question_title = $("h2.question_title").html();
       var username = $("div.user_profile_menu").attr("data-nickname");
       var csrf = $('input[name="csrfmiddlewaretoken"]').val();


       $.ajax({
                url: '/answer/',
                type: 'post',
                data: {
					question_id:question_id,
                    userid: userid,
                    username: username,
                    question_title:question_title,
                    content: content,
                    'csrfmiddlewaretoken': csrf
                },
                success: function(res){
                    if(res.code == 0){
                        window.location.href="/question/"+res.data.question_id+"/answer/"+res.data.answer_id;
                    }
                }
            })

    })
})