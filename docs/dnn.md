# cv2 DNN 使用指南

本项目的 `cv2.dnn` 封装提供了 OpenCV DNN 的基础推理接口，以及分类、检测、分割常用后处理工具。接口尽量接近 opencv-python 的使用习惯，同时保留 aardio 表对象易组合的特点。

## 1. 最小推理流程

```aardio
import cv2;

var net = cv2.readNetFromONNX("/models/classifier.onnx");
net.setPreferableBackend(cv2.DNN_BACKEND_OPENCV);
net.setPreferableTarget(cv2.DNN_TARGET_CPU);

var img = cv2.imread("/images/test.jpg");
var blob = cv2.blobFromImage(img,1/255,[224,224],[0,0,0],true,false);

net.setInput(blob);
var out = net.forward();
```

常用模型加载函数：

```aardio
cv2.readNet(model,config,framework);
cv2.readNetFromONNX(path);
cv2.readNetFromCaffe(prototxt,caffeModel);
cv2.readNetFromDarknet(cfgFile,darknetModel);
cv2.readNetFromTensorflow(model,config);
cv2.readNetFromTorch(model);
```

## 2. blob 与输出 Mat

DNN blob 通常是 4D Mat，形状为：

```text
[N, C, H, W]
```

可用以下属性和方法查看：

```aardio
blob.dims;
blob.sizeAt(0); // N
blob.sizeAt(1); // C
blob.sizeAt(2); // H
blob.sizeAt(3); // W
```

读取 forward 输出：

```aardio
var values = out.toFloatArray();
var values64 = out.toDoubleArray();
```

## 3. 分类后处理

```aardio
var labels = ["cat","dog","bird"];
var top5 = cv2.dnnDecodeClassification(out,labels,5,true);

for(i,item in top5){
    // item.index, item.label, item.probability
}
```

也可以单独使用：

```aardio
var probs = cv2.dnnSoftmax(scores);
var index,score = cv2.dnnArgMax(probs);
var top = cv2.dnnTopK(probs,5);
```

## 4. YOLO 风格检测后处理

`dnnDecodeYolo` 支持常见行格式：

```text
[cx, cy, w, h, objectness, class1, class2, ...]
```

示例：

```aardio
var labels = ["person","car"];
var rows = [
    [0.5,0.5,0.4,0.2,0.90,0.10,0.80],
    [0.2,0.2,0.2,0.2,0.80,0.70,0.10]
];

var detections = cv2.dnnDecodeYolo(
    rows,
    [640,480],
    0.25,
    0.45,
    labels,
    true,
    true
);
```

返回 detection 对象格式：

```aardio
{
    classId = 2;
    label = "car";
    score = 0.72;
    objectness = 0.90;
    classScore = 0.80;
    box = {x=192;y=192;width=256;height=96;left=192;top=192;right=448;bottom=288};
    x = 192;
    y = 192;
    width = 256;
    height = 96;
}
```

绘制检测结果：

```aardio
cv2.dnnDrawDetections(img,detections,labels,cv2.dnnColorPalette(#labels),2,true);
cv2.imwrite("/result.jpg",img);
```

## 5. SSD / Faster-RCNN DetectionOutput 解码

支持常见输出行格式：

```text
[imageId, classId, confidence, left, top, right, bottom]
```

示例：

```aardio
var rows = [
    [0,2,0.90,0.10,0.20,0.50,0.70],
    [0,1,0.70,0.60,0.10,0.90,0.40]
];

var labels = ["background","cat","dog"];
var detections = cv2.dnnDecodeSSD(rows,[200,100],0.5,labels,true,0.4,true);
```

`dnnDecodeFasterRCNN` 是同一解码器的别名。

## 6. 分割 / mask 后处理

### 二值 mask

```aardio
var mask = cv2.dnnDecodeBinaryMask(logits,width,height,0.5,true);
// mask.data 为 0/1 数组
// mask.mask 为 CV_8UC1 Mat，像素值 0/255
```

### 多类语义分割

输入为 channel-first 的 `[C,H,W]` 或 `[N,C,H,W]` 数据：

```aardio
var seg = cv2.dnnDecodeSegmentation(output,width,height,numClasses,labels);
// seg.classIds: 每个像素的 1-based 类别 id
// seg.scores: 每个像素最大类别分数
// seg.labels: 可选标签图
```

## 7. 可运行示例

仓库已提供不依赖外部大模型文件的示例：

```text
/samples/dnn_minimal_caffe_relu.aardio
/samples/dnn_minimal_onnx_relu.aardio
/samples/dnn_postprocess_demo.aardio
```

也可参考测试文件了解更多边界用法：

```text
/test/cv2/dnn_basic.aardio
/test/cv2/dnn_caffe_relu.aardio
/test/cv2/dnn_onnx_relu.aardio
/test/cv2/dnn_postprocess.aardio
/test/cv2/dnn_detection_postprocess.aardio
/test/cv2/dnn_ssd_detection.aardio
/test/cv2/dnn_segmentation_postprocess.aardio
/test/cv2/dnn_visualization.aardio
```
