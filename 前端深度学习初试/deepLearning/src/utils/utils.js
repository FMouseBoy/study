import * as tf from '@tensorflow/tfjs'
/**
 * 两种方式创建模型，创建卷积神经网络模型, keras方式、Functiony方式
 * @export
 * @returns model
 */
export function KerasCreateModel() {
  const model = tf.sequential()
  model.add(tf.layers.conv2d({
    inputShape: [224 ,224, 3],
    kernelSize: 3,
    filters: 32,
    activation: 'relu'
  }))
  model.add(tf.layers.maxPooling2d({
    poolSize: 2
  }))
  model.add(tf.layers.conv2d({
    kernelSize: 3,
    filters: 64,
    activation: 'relu'
  }))
  model.add(tf.layers.maxPooling2d({
    poolSize: 2
  }))
  model.add(tf.layers.flatten())
  model.add(tf.layers.dense({
    units: 5, activation: 'softmax'
  }))
  model.compile({ loss : 'categoricalCrossentropy', optimizer: 'Adam', metrics: ['accuracy']})
  console.log('Keras方式创建模型结构如下:')
  model.summary()
  return model
}

export function FunctionCreateModel () {
  const input = tf.input({shape: [224, 224, 3]})
  const conv_1 = tf.layers.conv2d({
    filters: 32,
    kernelSize: 3,
    activation: 'relu'
  }).apply(input)
  const maxpol_1 = tf.layers.maxPooling2d({
    poolSize:2
  }).apply(conv_1)
  const conv_2 = tf.layers.conv2d({
    filters: 64,
    kernelSize: 3,
    activation: 'relu'
  }).apply(maxpol_1)
  const maxpol_2 = tf.layers.maxPooling2d({
    poolSize: 2
  }).apply(conv_2)
  const flatten = tf.layers.flatten().apply(maxpol_2)
  const output = tf.layers.dense({
    units: 5,
    activation: 'softmax'
  }).apply(flatten)
  const model = tf.model({inputs: input, outputs: output})
  model.compile({ loss : 'categoricalCrossentropy', optimizer: 'Adam', metrics: ['accuracy']})
  console.log('Fuction方式创建模型结构如下:')
  model.summary()
  return model
}