//index.js
//获取应用实例
import  { load }  from '../../models/mobilenet'

const app = getApp()
const tfl = require('@tensorflow/tfjs-layers')


Page({
  data: {
    avatar: '',
    classIndex: 0,
    imageGroups: []
  },
  onShow() {
    const { avatar, classIndex } = app.globalData
    if (avatar) {
      this.setData({ avatar, classIndex })
    }
  },

  onShareAppMessage() {
    url: 'pages/index/index'
  },

  onLoad: function () {
    
  },
  onUnload() {
    
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {
    this.init()
  },

  getData () {
    return new Promise((resolve, reject) => {
      wx.request({
        url: 'https://m.jr.jd.com/mjractivity/data_source_100002605.json?t=1',
        success: res => {
          resolve(res.data)
        }
      })
    })
    
  },


  /**
   * 小程序init
   */
  async init () {
    
    const imagesData = await this.getData()
  
    this.setData({
      imageGroups: imagesData.imageGroups
    })
    this.initClassifier()
    
  },
  
  /**
   * 初始化加载模型
   */
  async initClassifier () {
    this.modeLoading()

    await load()

    this.hideLoading()
  },


  /**
   * 模型加载中Toast提示
   */
  modeLoading (message = '模型加载中...') {
    wx.showLoading({
      title: message,
    })
  },

  /**
   * 模型加载中Toast提示
   */
  hideLoading() {
    wx.hideLoading()
  },

  /**
   * 选择要识别的图片
   */
  chooseImage() {
    wx.chooseImage({
      count: 1,
      success: (res) => {
        const { tempFilePaths } = res
        const filePath = tempFilePaths[0]
        wx.navigateTo({
          url: `/pages/classifity/index?url=${filePath}`,
        })
      },
    })
  }
})
