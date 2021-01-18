import * as tfc from '@tensorflow/tfjs-converter'
import * as tf from '@tensorflow/tfjs-core'
const tfl = require('@tensorflow/tfjs-layers')

const app = getApp()
// https://storage.360buyimg.com/rama/common/model_classify5_2/model.json
// const MODEL_STORAGE_DIR = 'https://storage.360buyimg.com/rama/common/'
// const MODEL_FILE_URL = 'model_classify5_2/model.json'
const MODEL_STORAGE_DIR = 'https://storage.360buyimg.com/rama/common/'
const MODEL_FILE_URL = 'model_classify5/model.json'

  export function load() {
    return new Promise((resolve, reject) => {
      tfl.loadLayersModel((MODEL_STORAGE_DIR + MODEL_FILE_URL)).then(model => {
        model.summary()
        app.globalData.model = model
        resolve()
      }).catch(err => {
        wx.showLoading({
          title: '加载失败,重新加载',
        })
        load()
        reject(err)
      })
    })
  }
  export function predict(imageData) {
    tf.tidy(() => {
      
    })
    const model = app.globalData.model
    const tensorResult = tf.tidy(() => {
      const x = tf.browser.fromPixels(imageData);
      // console.log(x)
      // console.log(x.shape)
      const X = x.reshape([1,224,224,3])    //  模型的输入 [null, 224,224,3],此时输入为一张图片
      const X_Normalization = tf.div(X,255)   // 归一化
      return model.predict(X_Normalization)
    })
    const axis = 1;   //  1：看列， 0：看行
    const tensorIndex = tensorResult.argMax(axis);  // 返回的还是张量， 获取的是张量某一方向最大值的索引
    // console.log('索引:',tensorIndex.dataSync()[0])   //  返回的数值
    const resultIndex = tensorIndex.dataSync()[0]
    console.log('resultIndex',resultIndex)
    return resultIndex
  }