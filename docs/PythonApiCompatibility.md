# Python OpenCV API 兼容说明

本文记录 aardio `cv2` 封装与 Python OpenCV 的主要对齐策略与已知差异。

## 1. 模块与命名空间

Python OpenCV 的常见调用方式是把大多数函数直接挂在 `cv2` 根命名空间，例如：

```python
cv2.imread(...)
cv2.cvtColor(...)
cv2.threshold(...)
```

本项目内部源码按功能拆分为 `cv2.core`、`cv2.imgproc`、`cv2.highgui`、`cv2.video` 等文件 / 命名空间，但这些主要是 aardio 侧的组织方式。文档和示例应优先使用 Python 风格的根命名空间调用：

```aardio
cv2.imread(...)
cv2.cvtColor(...)
cv2.threshold(...)
```

`cv2.dnn` 已补齐常用 Python 风格子模块入口，例如 `cv2.dnn.blobFromImage`、`cv2.dnn.readNetFromONNX`、`cv2.dnn.NMSBoxes`。

`cv2.utils` 当前提供基础版本、计时与线程工具别名：

```aardio
cv2.utils.getVersionString()
cv2.utils.getBuildInformation()
cv2.utils.getTickCount()
cv2.utils.getTickFrequency()
cv2.utils.setNumThreads(n)
cv2.utils.getNumThreads()
```

## 2. 命名风格

优先使用 Python 风格 snake_case 或 Python 原始大小写：

```aardio
cv2.bitwise_and(a,b)
cv2.bitwise_or(a,b)
cv2.bitwise_xor(a,b)
cv2.bitwise_not(a)
cv2.CamShift(probImage,window)
cv2.denoise_TVL1([img1,img2,img3])
```

为了兼容旧代码，仍保留部分 aardio / OpenCvSharp 风格别名，例如 `BitwiseAnd`、`bitwiseAnd`、`camShift`、`denoiseTVL1`。

## 3. 返回值对齐

以下函数已按 Python OpenCV 风格返回多值：

| 函数 | Python 风格返回 |
| --- | --- |
| `threshold` | `retval, dst` |
| `findContours` | `contours, hierarchy` |
| `findHomography` | `H, mask` |
| `findFundamentalMat` | `F, mask` |
| `imencode` | `retval, bytes` |
| `VideoCapture.read` | `ret, frame` |

注意：`imencode` 的第二返回值在 aardio 中是字节数组，便于直接传给 `cv2.imdecode`。

`imread` 保留 aardio 常见的 `null, err` 错误信息返回风格：文件不存在时第一个返回值为 `null`，第二返回值为错误说明。Python OpenCV 通常只返回 `None`。迁移 Python 示例时只判断第一个返回值是否为 `null` 即可。

## 4. Mat 与 numpy 差异

Python OpenCV 通常以 `numpy.ndarray` 表示图像和矩阵；aardio 使用 `cv2.Mat` 包装 OpenCvSharp `Mat`。

常见迁移方式：

| Python / numpy | aardio cv2 |
| --- | --- |
| `img.shape` | `img.shape`，返回 `[rows, cols, channels]` |
| `img[y, x]` | `img.get(y,x)` |
| `img[y, x] = v` | `img.set(y,x,v)` |
| `img.copy()` | `img.clone()` |
| `img[y:y+h, x:x+w]` | `img.roi(x,y,w,h)` |
| `img.astype(...)` | `img.convertTo(type)` |

`Mat.toBytes`、`toFloatArray`、`toDoubleArray` 是 aardio 便利方法，不是 Python `cv2.Mat` API。`Mat.clone`、`row`、`col`、`roi` 则更接近 C++ / OpenCvSharp 的 `Mat` 方法，Python 示例中的 numpy 切片通常应迁移为 `roi` 或 `rowRange` / `colRange`。

## 5. 已知 HOLD 项

以下能力已在 Todo 中标记为 `HOLD`，不是未登记的遗漏：

- contrib / 扩展模块：`aruco`、`barcode`、`cuda`、`ml`、`fisheye` 等依赖 opencv-contrib 或额外后端。
- `SIFT_create`：当前 OpenCvSharp 4.5.3 构建未暴露 `OpenCvSharp.SIFT` 类型。
- `drawMatchesKnn`：当前 wrapper 尚未提供 KNN match 嵌套结果对象。
- HighGUI 鼠标回调：`setMouseCallback` 已导出占位函数并返回明确错误；安全地把 aardio 函数反调为 HighGUI 原生回调需要单独设计桥接层。
- video/tracking 对象工厂、HDR/tonemap 对象 API、calib3d 的 extended/RO/stereo 系列：底层部分支持但对象生命周期、复杂输出数组或测试样例较多，当前先暂缓。

## 6. 内部 helper

当前运行时仍可能看到 `_size2wh`、`_scalar4`、`_asNetMat` 等下划线前缀 helper。这些是内部实现细节，不属于 Python OpenCV 对齐 API，文档和示例不应主推这些名称。
