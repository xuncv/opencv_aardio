# opencv_aardio

`opencv_aardio` 是面向 [aardio](https://www.aardio.com/) 的 OpenCV 封装库，接口风格尽量贴近 `opencv-python`，便于把常见的 Python/OpenCV 示例迁移到 aardio 桌面程序中使用。

本项目当前基于 OpenCV/OpenCvSharp 插件桥接实现，适合在 Windows 下快速完成图像处理、机器视觉、DNN 推理、桌面调参工具和上位机软件开发。

## 当前状态

- 主要库入口：`/lib/cv2/_.aardio`
- 自动化测试目录：`/test/cv2/`
- DNN 使用文档：[`docs/dnn.md`](./docs/dnn.md)
- 示例目录：`/samples/`
- 当前测试集已整理为非阻塞自动化回归测试，不再保留旧的交互式测试脚本。

## 依赖

1. aardio
2. OpenCV native runtime
3. [opencv-plugin](https://github.com/xuncv/opencv-plugin/)（基于 OpenCvSharp 修改）

注意：本仓库的 `.gitignore` 会忽略 `*.dll`，因此全新克隆后需要自行下载并放置运行时 DLL。

推荐目录结构：

```text
lib/cv2/.res/
├── net461/
│   ├── OpenCvSharp.dll
│   ├── OpenCvSharp.Extensions.dll
│   ├── System.Drawing.Common.dll
│   ├── System.Memory.dll
│   ├── System.Runtime.CompilerServices.Unsafe.dll
│   └── System.ValueTuple.dll
└── native/
    └── x86/
        ├── OpenCvSharpExtern.dll
        └── opencv_videoio_ffmpeg453.dll
```

如果缺少这些 DLL，`import cv2` 或首次调用 OpenCV 接口时会失败。

## 快速开始

```aardio
import cv2;

var img = cv2.imread("/dist/images/Lena.jpg",1);
var dst = cv2.medianBlur(img,5);

cv2.imshow("dst",dst);
cv2.waitKey(0); // 按任意键关闭窗口
cv2.destroyAllWindows();
```

保存图像：

```aardio
cv2.imwrite("/result.jpg",dst);
```

`imshow / waitKey / destroyAllWindows` 属于 HighGUI 接口。`waitKey(0)` 会阻塞等待按键，适合手工调试，不应放入自动化测试。

## 已封装模块概览

当前 `lib/cv2` 已按功能拆分为多个模块：

```text
core / core_extra / core_utils
imgproc / imgproc_basic / draw
io / video / photo
features2d / calib3d
highgui
dnn
```

常用能力包括：

- Mat 创建、读写、类型/维度/通道信息、ROI、clone、reshape、convertTo
- 基础矩阵运算、统计、归一化、变换、通道拆分与合并
- 图像读取与保存：`imread / imwrite / imdecode / imencode`
- 图像处理：滤波、阈值、形态学、边缘、轮廓、几何变换、透视变换、Hough 等
- 绘图：`line / rectangle / circle / putText / polylines / drawContours`
- 视频与相机：`VideoCapture / VideoWriter` 相关封装
- 特征：ORB、BFMatcher 等基础特征匹配能力
- HighGUI：`imshow / waitKey / namedWindow / destroyWindow / destroyAllWindows`
- DNN：模型加载、forward、分类/检测/分割后处理与可视化辅助函数

## DNN / AI 推理

当前 `cv2.dnn` 已支持 OpenCV DNN 的基础推理流程：

```aardio
import cv2;

var net = cv2.readNetFromONNX("/models/model.onnx");
var img = cv2.imread("/dist/images/Lena.jpg");
var blob = cv2.blobFromImage(img,1/255,[224,224],[0,0,0],true,false);

net.setInput(blob);
var out = net.forward();

var top5 = cv2.dnnDecodeClassification(out,["cat","dog","bird"],5,true);
```

已支持：

- `blobFromImage / blobFromImages`
- `readNet / readNetFromONNX / readNetFromCaffe / readNetFromDarknet / readNetFromTensorflow / readNetFromTorch / readNetFromYolo`
- `Net.setInput / Net.forward / Net.forwardLayers / Net.getPerfProfile`
- `Mat.dims / Mat.sizeAt / Mat.toFloatArray / Mat.toDoubleArray`
- 分类后处理：`dnnSoftmax / dnnSigmoid / dnnArgMax / dnnTopK / dnnDecodeClassification`
- 检测后处理：`NMSBoxes / dnnDecodeYolo / dnnDecodeYoloLatest / dnnDecodeYoloV8/V9/V10/V11/V12 / dnnYoloDetect / dnnDecodeSSD / dnnDecodeFasterRCNN / dnnDrawDetections`
- 分割后处理：`dnnDecodeBinaryMask / dnnDecodeSegmentation`

详细说明见：[`docs/dnn.md`](./docs/dnn.md)

## 示例

当前仓库内的示例包括：

```text
samples/highgui_imshow.aardio              HighGUI 显示窗口示例（交互式）
samples/cornCounter.aardio                 自生成图像的轮廓计数示例
samples/matchTemplate.aardio               基于内置 Lena 图像的模板匹配示例
samples/dnn_minimal_caffe_relu.aardio      动态生成最小 Caffe ReLU 网络并 forward
samples/dnn_minimal_onnx_relu.aardio       动态生成最小 ONNX ReLU 网络并 forward
samples/dnn_postprocess_demo.aardio        DNN 分类/检测/分割后处理综合示例
samples/yolo_latest_onnx.aardio            Ultralytics YOLO 最新 ONNX 模型调用示例
```

除 `highgui_imshow.aardio` 是专门用于演示窗口显示外，其余示例默认不阻塞；需要预览图像时可给支持的示例传入 `show=true`。

## 测试

自动化测试入口：

```aardio
return loadcodex("/test/cv2/run_all.aardio");
```

当前测试目录只保留 `/test/cv2/*.aardio`，均为 `util.testRunner` 风格的非阻塞测试。当前回归覆盖：

- core / Mat / 数学与矩阵操作
- imgproc 基础处理、边缘、轮廓、几何变换、形态学、分割辅助
- features2d / ORB / matcher
- video/photo 基础封装
- HighGUI 非阻塞接口
- DNN 基础接口、Caffe/ONNX 最小真实 forward、分类/检测/分割后处理

截至本次整理，完整回归结果：

```text
total: 750
passed: 750
failed: 0
success: true
```

## 项目目标

1. 充分利用 aardio 的胶水语言特性，增强 aardio 图像处理与机器视觉能力。
2. 结合 aardio 桌面开发优势，提升上位机、调参工具、工业视觉小工具的开发效率。
3. 提供比 Python/conda 环境更轻量的 OpenCV 使用方式。
4. 提高 OpenCV 示例迁移、算法验证和桌面集成效率。
5. 支持实时窗口显示与交互调参。

## 参考

- [aardio 官网](https://www.aardio.com/)
- [OpenCV 官网](https://opencv.org/)
- [opencv-plugin](https://github.com/xuncv/opencv-plugin/)
- [旧版中文文档](https://xuncv.github.io/#/)（可能未覆盖当前新增 DNN/HighGUI/测试整理内容）
