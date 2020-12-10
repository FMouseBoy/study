/**
 * use: <count-down leftTime="{{leftTime}}"><count-down>
 */
Component({
  properties:{
    startTime: {
        type: Number,
        value: 0
    },
    endTime: {
        type: Number,
        value: 0
    },
    leftTime: {
        type: Number,
        value: 0
    },
    showType: {
      type: String,
      value: ''
    }
  },
  data:{
    d: '00',
    h: '00',
    m: '00',
    s: '00',
    ms: '00',
    timer: ''
  },
  lifetimes: {
    attached: function() {
      // 在组件实例进入页面节点树时执行
      console.log(this.data.leftTime)
      this.getRtime(this.data.leftTime)
    },
    detached: function() {
      // 在组件实例被从页面节点树移除时执行
      clearTimeout(this.data.timer)
    },
  },
  onShow(){

  },
  methods:{
    /**
     * 剩余时间:毫秒
     */
    getRtime(leftTime) {
        let d = '00',
            h = '00',
            m = '00',
            s = '00',
            ms = '00';
        if (leftTime > 0) {
            d = Math.floor(leftTime / 1000 / 60 / 60 / 24);
            // h = Math.floor((leftTime / 1000 / 60 / 60) % 24);  // 正常dd:hh:mm:ss:ms
            h = Math.floor(leftTime / 1000 / 60 / 60);  // 大于24小时显示, hh:mm:ss:ms
            m = Math.floor((leftTime / 1000 / 60) % 60);
            s = Math.floor((leftTime / 1000) % 60);
            ms = Math.floor(leftTime % 1000);
            if (s < 10) {
                s = '0' + s;
              }
            if (m < 10) {
                m = '0' + m;
            }
            if (h < 10) {
                h = '0' + h;
            }
            if (d < 10) {
                d = '0' + d;
            }
            if (ms < 100) {
                ms = '0' + ms
            }
            clearTimeout(this.data.timer)
            let timer = setTimeout(() => {
                this.getRtime(leftTime - 100)
            },100)  // 若只需要秒,不需要毫秒,50 改为1000,提高性能
            this.setData({
                timer: timer
            })
        } else {
            console.log('活动已结束~')
        }
        this.setData({
            d: String(d),
            h: String(h),
            m: String(m),
            s: String(s),
            ms: String(ms).substr(0, 1)
        })
        // console.log('倒计时====>', this.data.d , this.data.h ,this.data.m,this.data.s,this.data.ms);
    }
  }
})