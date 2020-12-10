const app = getApp()

Page({
  data: {
    defaultActive: 0,
    skuProducts: [1,2,3,4]
  },
  onLoad: function () {
    
  },

  changeTab (e) {
    let index = e.currentTarget.dataset.index
    this.setData({
      defaultActive: index
    })
  }
})
