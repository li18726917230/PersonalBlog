//初始化 wangEditor
const E = window.wangEditor
const editor = new E('#div1')

// 配置 server 接口地址
editor.config.uploadImgServer = '../upload_image/'
//配置上传的 filename
editor.config.uploadFileName = 'fileName'
//配置上传的文件类型
editor.config.uploadImgAccept = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']
//限制一次最多上传几张
editor.config.uploadImgMaxLength = 5

editor.create()

//对文本内容进行判断
$('#form_btn').submit(function (event) {
    if (editor.txt.text()==''){
        $('#span_text').text('内容不能为空')
        event.preventDefault(); //阻止页面提交
    }
    else {
         $('#content').val(editor.txt.html())
    }
})
