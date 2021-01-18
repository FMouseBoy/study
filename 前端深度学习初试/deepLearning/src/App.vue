<template>
  <div id="app">
    <div>
      <canvas id="mycanvas"></canvas>
    </div>
    <div v-if="resultIndex!=5">
      {{project[resultIndex]}}
    </div>
    <!-- <div v-if="imageUrl!=''">
      <img style="width:224px;height:224px" :src="imageUrl">
    </div> -->
    <div class="btn">
      <button @click="kerasCreateModel">Keras方式创建模型</button>
    </div>
    <div class="btn">
      <button @click="functionCreateModel">Function方式创建模型</button>
    </div>
    <div class="btn">
      <button @click="loadModel">加载模型</button>
    </div>
    <div class="btn">
      <button @click="doDraw">预测</button>
    </div>
    
  </div>
</template>

<script>
import * as tf from '@tensorflow/tfjs'
import { KerasCreateModel, FunctionCreateModel } from './utils/utils.js'
import { mod, model } from '@tensorflow/tfjs'

export default {
  name: 'App',
  components: {
    
  },
  data() {
    return {
      imageUrl: 'https://m.360buyimg.com/jrqb/jfs/t1/154534/25/14131/60531/5ffd5d3bEf86b0753/3676741307c18d50.png',
      project: {
        0: '金贴裂变',
        1: '云养猪',
        2: '金贴码H5',
        3: '一份拼抽',
        4: '黄金猜涨跌',
        5: ''
      },
      resultIndex: 5
    }
  },
  created() {
    
  },
  mounted(){
    
  },
  methods: {
    kerasCreateModel() {
      const model = KerasCreateModel()
      console.log(model)
    },
    functionCreateModel() {
      const model = FunctionCreateModel()
      // model.fit(batch_size)
      console.log(model)
    },
    async loadModel() {
      const model = await tf.loadLayersModel('https://storage.360buyimg.com/rama/common/model_classify5/model.json');
      console.log('模型结构如下:')
      model.summary()
      console.log(model)
    },
    doDraw(){
      const _this = this
      // 获取canvas
      var canvas = document.getElementById("mycanvas")
      if(!canvas){
        return false
      } else {
        var context = canvas.getContext('2d')
        var img = new Image()
        img.crossOrigin = '';
        img.src = this.imageUrl
        // 加载图片
        img.onload = function(){
          if(img.complete){
            // 根据图像重新设定了canvas的长宽
            canvas.setAttribute("width",img.width)
            canvas.setAttribute("height",img.height)
            // 绘制图片
            context.drawImage(img,0,0,img.width,img.height)
            var imgData = context.getImageData(0,0,img.width,img.height)
            console.log(imgData)
            var x = tf.browser.fromPixels(imgData);
            // console.log(imgData)
            // console.log('x:',x.shape)
            const result = x.reshape([1,224,224,3])
            // console.log(result.shape)
            // result.print()
            _this.predict(result)
          }
        }
      }
    },
    async predict (imageData) {
      console.log('加载模型。。。')
      const model = await tf.loadLayersModel('https://storage.360buyimg.com/rama/common/model_classify5/model.json');
      console.log('加载完毕。。。')
      const result = model.predict(imageData)   //  返回的是一个tensor， tensor.shape: [1,5]
      const axis = 1;   //  1：看列， 0：看行
      const resultIndex = result.argMax(axis);  // 返回的还是张量， 获取的是张量某一方向最大值的索引
      // console.log('索引:',resultIndex.dataSync()[0])   //  返回的数值
      this.resultIndex = resultIndex.dataSync()[0]
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.btn {
  margin-top: 10px;
}
</style>
