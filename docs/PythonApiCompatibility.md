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

`Mat.toBytes`、`toFloatArray`、`toDoubleArray` 是 aardio 便利方法，不是 Python `cv2.Mat` API。

## 5. 内部 helper

当前运行时仍可能看到 `_size2wh`、`_scalar4`、`_asNetMat` 等下划线前缀 helper。这些是内部实现细节，不属于 Python OpenCV 对齐 API，文档和示例不应主推这些名称。
