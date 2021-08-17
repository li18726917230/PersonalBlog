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
//设置高度
editor.config.height = 100
//取消全屏
editor.config.showFullScreen = false
//配置不显示的菜单
// 配置菜单栏，设置不需要的菜单
editor.config.excludeMenus = [
    'video',
    'image'
]

editor.create()

//对文本内容进行判断

