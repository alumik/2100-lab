/**
 * 对图片进行剪裁函数
 * @param url
 * @param width
 * @param height
 * @param callback
 * 根据传入URL读取图片信息
 * 根据width和height进行canvas上的图片剪裁
 * 回调函数将剪裁后的数据发回
 */

export default function resize_image (url, width, height, callback) {
  var sourceImage = new Image()

  sourceImage.onload = function (evt) {
    var canvas = document.createElement('canvas')
    canvas.width = width
    canvas.height = height

    if (sourceImage.width === sourceImage.height) {
      canvas.getContext('2d').drawImage(sourceImage, 0, 0, width, height)
    } else {
      let minVal = Math.min(sourceImage.width, sourceImage.height)
      if (sourceImage.width > sourceImage.height) {
        canvas.getContext('2d').drawImage(sourceImage, (sourceImage.width - minVal) / 2, 0, minVal, minVal, 0, 0, width, height)
      } else {
        canvas.getContext('2d').drawImage(sourceImage, 0, (sourceImage.height - minVal) / 2, minVal, minVal, 0, 0, width, height)
      }
    }
    callback(canvas.toDataURL())
  }

  sourceImage.src = url
}
