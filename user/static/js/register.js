//倒计时
var count = 60

function get_time() {
    if (count === 1) {
        count = 60
        $('#get-code').text('重新发送验证码!')
        $('#get-code').attr('onmousedown', 'get_code()') //添加点击元素
        return;
    } else {
        count--;
        $('#get-code').text('倒计时(' + count + ')')
        $('#get-code').removeAttr('onmousedown') //移除点击元素
    }
    setTimeout(function () {
        get_time()
    }, 1000)
}


//判断用户名是否存在已经是否符合条件
function username_val() {
    //用户名正则，4到16位（字母，数字，下划线，减号）
    var uPattern = /^[a-zA-Z0-9_-]{4,16}$/;
    var username = $('#username').val()
    $('#usernameState').removeAttr('class')
    if (!uPattern.test(username)) {
        $('#usernameHelp').text('请输入4到16位（字母，数字，下划线，减号）')
    } else {
        $.ajax({
            url: user_val,
            method: 'post',
            cache: false,
            data: {username: username},
            success: function (msg) {
                if (msg.result == 0) {
                    $('#usernameHelp').text('用户名以注册，请重新输入!')
                    $('#usernameState').attr('class', 'glyphicon glyphicon-remove form-control-feedback')
                    $("#btn").attr('disabled', true);
                } else {
                    $('#usernameHelp').text('')
                    $('#usernameState').attr('class', 'glyphicon glyphicon-ok form-control-feedback')
                }
            },
            error: function (xhr) {
            }
        })
    }
}

//判断两次密码是否一致
function password_val() {
    var password1 = $('#password1').val();
    var password2 = $('#password2').val();
    if (password1 != password2) {
        $('#passwordHelp').text('两次密码不一致，请重新输入！')
         $("#btn").attr('disabled', true);
    } else {
        $('#btn').removeAttr('disabled')
        $('#passwordHelp').text('')
    }

}

//发送验证码
function get_code() {
    var tel = $('#tel').val()
    var myreg = /^[1][3,4,5,7,8,9][0-9]{9}$/
    if (!myreg.test(tel)) {
        $('#telHelp').text('手机号输入错误，请重新输入!')
        $('#telState').attr('class', 'glyphicon glyphicon-remove form-control-feedback')
    } else {
        $('#telHelp').text('')
        //手机号发送，获取验证码
        $.ajax({
            url: code_send,
            method: 'post',
            cache: false,
            data: {tel: tel},
            success: function (msg) {
                if (msg.result == 0) {
                    $('#telHelp').text('验证码发送成功')
                    $('#telState').attr('class', 'glyphicon glyphicon-ok form-control-feedback')
                    get_time()
                } else if (msg.result == 1) {
                    $('#telHelp').text('验证码发送频繁，请一分钟之后在次尝试！')
                    $('#telState').attr('class', 'glyphicon glyphicon-remove form-control-feedback')
                    $("#btn").attr('disabled', true);
                } else {
                    $('#telHelp').text('手机号已注册')
                    $('#telState').attr('class', 'glyphicon glyphicon-remove form-control-feedback')
                    $("#btn").attr('disabled', true);
                }
            },
            error: function (xhr) {
                console.log(xhr)
            }
        })
    }
}

//验证 验证码
function put_code() {
    var tel = $('#tel').val()
    var code = $('#code').val();
    $('#code').text('')
    //发送请求，进行验证
    $.ajax({
        url: code_val,
        method: 'post',
        cache: false,
        data: {code: code, tel: tel},
        success: function (msg) {
            if (msg.result == 0) {
                $('#codeState').attr('class', 'glyphicon glyphicon-ok form-control-feedback')
            } else {
                $('#codeState').attr('class', 'glyphicon glyphicon-remove form-control-feedback')
                $("#btn").attr('disabled', true);
            }
        },
        error: function (xhr) {
            console.log(xhr)
        }
    })
}

$('form').click(function () {
    console.log('11')
    var patt1 = new RegExp("glyphicon-ok");
    usernameState = $('#usernameState').attr('class')
    telState = $('#telState').attr('class')
    codeState = $('#codeState').attr('class')
    if (patt1.test(usernameState) && patt1.test(telState) && patt1.test(codeState)) {
        $('#btn').removeAttr('disabled')
    }
})