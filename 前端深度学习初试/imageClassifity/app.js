//app.js

const fetchWechat = require('fetch-wechat')
const tf = require('@tensorflow/tfjs-core')
const webgl = require('@tensorflow/tfjs-backend-webgl')
const plugin = requirePlugin('tfjsPlugin')

App({
  onLaunch: function () {

    // 获取系统信息
    wx.getSystemInfo({
      success: (result) => {
        this.globalData.systemInfo = wx.getSystemInfoSync()
        this.globalData.width = wx.getSystemInfoSync().windowWidth
        this.globalData.screenWidth = wx.getSystemInfoSync().screenWidth
        this.globalData.screenHeight = wx.getSystemInfoSync().screenHeight
      },
    })

    // 检测WEBGL版本
    tf.ENV.flagRegistry.WEBGL_VERSION.evaluationFn = () => {return 1}

    plugin.configPlugin({
      // polyfill fetch function
      fetchFunc: fetchWechat.fetchFunc(),
      // inject tfjs runtime
      tf,
      // inject webgl backend
      webgl,
      // provide webgl canvas
      canvas: wx.createOffscreenCanvas()
    })
  },
  globalData: {
    localStorageIO: plugin.localStorageIO,
    fileStorageIO: plugin.fileStorageIO,
    avatar: '',
    model: null,
    classIndex: 0
  }
})