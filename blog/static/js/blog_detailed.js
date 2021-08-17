//对文本内容进行判断


function btn_reply(comment_id, reply_id, replyuser, nickname) {
    console.log('22')
    $('html').animate({scrollTop: $('#div1').offset().top - 150}, 300, function () {
        $('.placeholder').text('欢迎回复' + nickname + ':')
        $('.btn').attr('value', '回复')
        $('.btn').attr('comment_id', comment_id)
        $('.btn').attr('reply_id', reply_id)
        $('.btn').attr('replyuser', replyuser)
    }) //滚动条滚动到指定位置
}

function btn_comments() {
    if (editor.txt.text() == '') {
        $('#span_text').text('内容不能为空')
    } else if ($('.btn').val() == '评论') {
        $.ajax({
            url: comments_url,
            method: 'post',
            cache: false,
            data: {'text': editor.txt.text(), 'blog_id': blog_id},
            success: function (data) {
                console.log(111)
                if (data['msg'] == 'SUCCESS') {
                    var str= '\''+data['comment_id']+'\'' + ',' + '\''+data['comment']+'\'' + ',' + '\''+data['user_id']+'\''+ ',' + '\''+data['user']+'\''
                    console.log(str)
                    //插入评论
                    var comment_html = '<div class="comment" id="comment_' + data['comment_id'] + '">' +
                        '<span>' + data['user'] + '</span> ' +
                        '<span>(' + data['comment_time'] + '):</span> ' +
                        '<span id="">' + data['text'] + '</span>' +
                        '<a onclick="btn_reply(' +str+')"> 回复</a>' +
                        '</div>'
                    $("#comment-list").prepend(comment_html);
                    editor.txt.clear()
                    $("#text-p").empty();
                    $('#span_text').text('评论成功')
                } else {
                    $('#span_text').text('评论失败')
                }
            },
            error: function (xhr) {
                console.log(xhr)
            }
        })
        return false;
    } else {
        $.ajax({
            url: reply,
            method: 'post',
            cache: false,
            data: {
                text: editor.txt.text(),
                blog_id: blog_id,
                comment_id: $('.btn').attr('comment_id'),
                reply_id: $('.btn').attr('reply_id'),
                replyuser: $('.btn').attr('replyuser')
            },
            success: function (data) {
                console.log('11')
                if (data['msg'] == 'SUCCESS') {
                    //插入回复
                    var str= '\''+data['topcomment']+'\'' + ',' + '\''+data['comment_reoly_id']+'\'' + ',' + '\''+data['replyuser_id']+'\''+ ',' + '\''+data['replyuser']+'\''
                    var comment_html = '<div class="reply" id="' + data['comment_reoly_id'] + '">' +
                        data['user'] + ' @ ' + data['replyuser'] + ' (' + data['comment_time'] + ')：' + data['text'] +
                        '<a onclick="btn_reply(' + str + ')"> 回复</a>' +
                        '</div>'
                    if ($("#comment_" + $('.btn').attr('comment_id')).find("div").length == 0) {
                        $("#comment_" + data['topcomment']).append(comment_html);
                    } else {
                        data = data['comment_reoly_id'] - 1
                        $('#' + data).before(comment_html)
                    }
                    editor.txt.clear()
                    $("#text-p").empty();
                    $('#span_text').text('回复成功')
                    $('.placeholder').text('欢迎评论:')
                    $('.btn').attr('value', '评论')
                } else {
                    $('#span_text').text('回复失败')
                }
            },
            error: function (xhr) {
                console.log(xhr)
            }
        })

    }
}

$(function () {
    $("[data-toggle='tooltip']").tooltip();
    if (user_nickname == '') {
        $(".like").attr('data-original-title', '请登录')
    } else {
        if (document.getElementsByClassName('active').length == 0) {
            $(".like").attr('data-original-title', '请点赞')
        } else {
            $(".like").attr('data-original-title', '取消点赞')
        }
    }
});

function like(obj, content_type, object_id) {
    var is_like = obj.getElementsByClassName('active').length == 0
    $.ajax({
        url: blog_like,
        type: 'GET',
        data: {
            content_type: content_type,
            object_id: object_id,
            is_like: is_like,
        },
        cache: false,
        success: function (data) {
            if (data['status'] == 'SUCCESS') {
                //更新点赞状态
                var element = $(obj.getElementsByClassName('glyphicon'))
                if (is_like) {
                    element.addClass('active');
                    $(".like").attr('data-original-title', '取消点赞')
                } else {
                    element.removeClass('active')
                    $(".like").attr('data-original-title', '请点赞')
                }
                //更新点赞数量
                var liked_num = $(obj.getElementsByClassName('liked-num'))
                liked_num.text(data['liked_num'])
            } else {
                console.log(data)
            }
        },
        error: function (xhr) {
            console.log(xhr)
        }
    })
}