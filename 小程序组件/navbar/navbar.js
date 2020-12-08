
Component({
  properties: {
    header: {
      type: Object,
      value: {
        homeCapsule: true, // 是否展示首页
        backCapsule: true, // 是否展示返回
        headerbg: "#fff", // 背景颜色
        title: "", // 标题
        fontColor: "#000", // 字体颜色
        fontSize: '16', // 标题字体大小
        capsulebg: 'rgba(0,0,0,0.2)', // 胶囊样式
        capsuleborder: '1px solid rgba(0, 0, 0, 0.1)',
        capsulesep: '1px solid rgba(255,255,255,0.2)'
      }
    }
  },

  options: {
    styleIsolation: 'apply-shared',
  },

  methods: {
    backClick() {
      if (getCurrentPages().length == 1) {
        this.homeClick()
      } else {
        wx.navigateBack({
          delta: 1
        })
      }
    },
    homeClick() {
      wx.switchTab({
        url: '/pages/homepage/homepage',
      })
    }
  },
  attached() {
    var self = this;
    wx.getSystemInfo({
      success(res) {
        var isIos = res.system.indexOf('iOS') > -1;
        self.setData({
          statusHeight: res.statusBarHeight,
          navHeight: isIos ? 44 : 48
        })
      }
    })
  }
})
