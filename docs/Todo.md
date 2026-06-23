# OpenCV Python API 对齐 Todo

> 目标：记录当前 aardio `cv2` 封装中与 Python OpenCV API 未对齐、待补齐或建议修改的模块 / 函数 / 方法。
>
> 状态说明：
> - `TODO`：尚未处理
> - `DOING`：处理中
> - `DONE`：已完成
> - `HOLD`：暂缓，通常因为版本差异、OpenCvSharp 不支持或优先级较低

## 1. 模块结构 / 命名空间对齐

| 优先级 | 模块 / 名称 | 当前情况 | Python OpenCV 对齐目标 | 待办动作 | 状态 |
| --- | --- | --- | --- | --- | --- |
| P0 | `cv2.dnn` | DNN 函数主要挂在 `cv2` 根命名空间，`cv2.dnn` 下未完整暴露 | `cv2.dnn.blobFromImage`、`cv2.dnn.readNetFromONNX`、`cv2.dnn.NMSBoxes` 等 | 已将 DNN 相关函数同步挂载到 `cv2.dnn`，保留根命名空间兼容别名 | DONE |
| P1 | `cv2.utils` | 原存在 `utils.aardio`，但运行时 `cv2.utils` 内容与 Python 不一致 | Python 存在 `cv2.utils` 子模块 | 已将版本、计时、线程工具同步到 `cv2.utils` 并测试 | DONE |
| P1 | `cv2.core` / `cv2.imgproc` / `cv2.highgui` 等 | aardio 内部按模块拆分，Python 这些通常不是公开子模块 | Python 函数大多直接位于 `cv2` 根命名空间 | 已新增 `docs/PythonApiCompatibility.md`，明确内部拆分模块，文档主推根命名空间写法 | DONE |
| P1 | 内部 helper 暴露 | `_size2wh`、`_scalar4`、`_asNetMat` 等 helper 暴露在 `cv2` 根对象 | Python 不公开这些内部函数 | 已新增兼容文档说明这些为内部实现细节；后续可在 P2/P3 继续物理隐藏 | DONE |
| P2 | contrib 扩展模块 | `aruco`、`barcode`、`cuda`、`ml`、`fisheye` 等基本缺失 | 对齐 `opencv-contrib-python` 的常见模块 | 根据项目目标决定是否支持；默认暂缓 | HOLD |

## 2. `cv2.dnn` 待挂载 / 待对齐函数

| 优先级 | 函数 / 类名 | 当前情况 | Python OpenCV 对齐目标 | 待办动作 | 状态 |
| --- | --- | --- | --- | --- | --- |
| P0 | `cv2.dnn.blobFromImage` | 当前为 `cv2.blobFromImage` | `cv2.dnn.blobFromImage` | 已增加 dnn 子模块别名 | DONE |
| P0 | `cv2.dnn.blobFromImages` | 当前为 `cv2.blobFromImages` | `cv2.dnn.blobFromImages` | 已增加 dnn 子模块别名 | DONE |
| P0 | `cv2.dnn.readNet` | 当前为 `cv2.readNet` | `cv2.dnn.readNet` | 已增加 dnn 子模块别名 | DONE |
| P0 | `cv2.dnn.readNetFromONNX` | 当前为 `cv2.readNetFromONNX` / `readNetFromOnnx` | `cv2.dnn.readNetFromONNX` | 已增加 `readNetFromONNX` 与 `readNetFromOnnx` dnn 子模块别名，推荐大写 `ONNX` | DONE |
| P0 | `cv2.dnn.readNetFromCaffe` | 当前为 `cv2.readNetFromCaffe` | `cv2.dnn.readNetFromCaffe` | 已增加 dnn 子模块别名 | DONE |
| P0 | `cv2.dnn.readNetFromDarknet` | 当前为 `cv2.readNetFromDarknet` | `cv2.dnn.readNetFromDarknet` | 已增加 dnn 子模块别名 | DONE |
| P0 | `cv2.dnn.readNetFromTensorflow` | 当前为 `cv2.readNetFromTensorflow` | `cv2.dnn.readNetFromTensorflow` | 已增加 dnn 子模块别名 | DONE |
| P0 | `cv2.dnn.readNetFromTorch` | 当前为 `cv2.readNetFromTorch` | `cv2.dnn.readNetFromTorch` | 已增加 dnn 子模块别名 | DONE |
| P0 | `cv2.dnn.NMSBoxes` | 当前为 `cv2.NMSBoxes` | `cv2.dnn.NMSBoxes` | 已增加 dnn 子模块别名 | DONE |
| P0 | `cv2.dnn.Net` | 当前存在 `DnnNet` / `Net` 风格差异 | Python 通过 `cv2.dnn.Net` 表示网络对象类型 / 相关语义 | 已导出 `cv2.dnn.Net` / `cv2.dnn.DnnNet`，根命名空间 `cv2.Net` 保持兼容 | DONE |

## 3. 命名不符合 Python 风格，建议修改或增加别名

| 优先级 | 当前名称 | Python OpenCV 对齐名称 | 当前问题 | 待办动作 | 状态 |
| --- | --- | --- | --- | --- | --- |
| P1 | `BitwiseAnd` | `bitwise_and` | PascalCase / OpenCvSharp 风格 | 已保留兼容别名，并通过测试主推 `bitwise_and` | DONE |
| P1 | `BitwiseOr` | `bitwise_or` | PascalCase / OpenCvSharp 风格 | 已保留兼容别名，并通过测试主推 `bitwise_or` | DONE |
| P1 | `BitwiseXor` | `bitwise_xor` | PascalCase / OpenCvSharp 风格 | 已保留兼容别名，并通过测试主推 `bitwise_xor` | DONE |
| P1 | `BitwiseNot` | `bitwise_not` | PascalCase / OpenCvSharp 风格 | 已保留兼容别名，并通过测试主推 `bitwise_not` | DONE |
| P1 | `bitwiseAnd` | `bitwise_and` | camelCase 不符合 Python 命名 | 已保留兼容别名，并通过测试主推 snake_case | DONE |
| P1 | `bitwiseOr` | `bitwise_or` | camelCase 不符合 Python 命名 | 已保留兼容别名，并通过测试主推 snake_case | DONE |
| P1 | `bitwiseXor` | `bitwise_xor` | camelCase 不符合 Python 命名 | 已保留兼容别名，并通过测试主推 snake_case | DONE |
| P1 | `bitwiseNot` | `bitwise_not` | camelCase 不符合 Python 命名 | 已保留兼容别名，并通过测试主推 snake_case | DONE |
| P1 | `camShift` | `CamShift` | 大小写与 Python 不一致 | 已测试并主推 `CamShift`，保留 `camShift` 兼容 | DONE |
| P1 | `denoiseTVL1` | `denoise_TVL1` | 下划线位置与 Python 不一致 | 已增加 `denoise_TVL1` 别名并测试 | DONE |
| P2 | `convexHullIndices` | 可通过 `convexHull(..., returnPoints=false)` 实现 | Python 没有该独立函数名 | 文档标记为 aardio 便利函数，不作为 Python 对齐 API | TODO |
| P2 | `contourMoments` | `moments` | Python 使用 `cv2.moments` | 确认 `moments` 是否已存在；如已有则文档弱化 `contourMoments` | TODO |
| P2 | `applyCLAHE` | `CLAHE.apply` / `createCLAHE` | Python 通常通过 CLAHE 对象方法 | 补齐 / 强化 `createCLAHE` 与 `CLAHE.apply` 用法 | TODO |
| P2 | `Abs` | 无直接同名 Python API | OpenCvSharp / 辅助风格 | 标记为扩展函数或隐藏 | TODO |
| P2 | `CopyTo` | `Mat.copyTo` 或 numpy 赋值语义 | OpenCvSharp 风格 | 标记为扩展函数或隐藏 | TODO |
| P2 | `Format` | 无直接同名 Python API | OpenCvSharp 风格 | 标记为扩展函数或隐藏 | TODO |
| P2 | `Sum` | `sumElems` | Python 常见为 `cv2.sumElems` | 增加 / 主推 `sumElems` | TODO |
| P2 | `cvRound` / `cvFloor` / `cvCeil` | Python 通常不直接暴露这些 C 宏风格函数 | C API 风格 | 标记为扩展函数或隐藏 | HOLD |

## 4. 返回值 / 语义需要对齐的函数

| 优先级 | 函数名 | 当前返回 / 行为 | Python OpenCV 行为 | 待办动作 | 状态 |
| --- | --- | --- | --- | --- | --- |
| P0 | `findHomography` | 原返回 `ok, Mat` 风格 | Python 返回 `(H, mask)` | 已修改为返回单应矩阵 `H` 和 `mask` | DONE |
| P0 | `findFundamentalMat` | 原返回 `ok, Mat` 风格 | Python 返回 `(F, mask)` | 已修改为返回基础矩阵 `F` 和 `mask` | DONE |
| P1 | `imencode` | 原只返回编码后的 bytes | Python 返回 `(retval, buf)` | 已改为返回 `true, bytes`，并更新测试 | DONE |
| P1 | `imread` | 文件不存在返回 `null, "文件不存在..."` | Python 返回 `None`，通常不抛异常 | 评估是否保留 aardio 风格错误信息；文档说明差异或增加兼容模式 | TODO |
| P1 | `VideoCapture.read` | 当前返回 `ok, Mat` | Python 返回 `(ret, frame)` | 已有视频文件读帧测试覆盖 | DONE |
| P1 | `threshold` | 当前返回 `retVal, Mat` | Python 返回 `(retval, dst)` | 已有测试覆盖 `(retval, dst)` | DONE |
| P1 | `findContours` | 当前返回 `contours, hierarchy` | OpenCV 4 Python 返回 `(contours, hierarchy)` | 已有测试覆盖 `(contours, hierarchy)` | DONE |

## 5. features2d 待补齐函数 / 类

| 优先级 | 函数 / 类名 | 当前情况 | Python OpenCV 对齐目标 | 待办动作 | 状态 |
| --- | --- | --- | --- | --- | --- |
| P1 | `AKAZE_create` | 原缺失 | `cv2.AKAZE_create` | 已封装 OpenCvSharp AKAZE 并测试 `detectAndCompute` | DONE |
| P1 | `BRISK_create` | 原缺失 | `cv2.BRISK_create` | 已封装 OpenCvSharp BRISK 并测试 `detectAndCompute` | DONE |
| P1 | `KAZE_create` | 原缺失 | `cv2.KAZE_create` | 已封装 OpenCvSharp KAZE 并测试 `detectAndCompute` | DONE |
| P1 | `SIFT_create` | 底层 OpenCvSharp 4.5.3 当前构建未暴露 `OpenCvSharp.SIFT` | `cv2.SIFT_create` | 暂缓；需升级底层 OpenCV/OpenCvSharp 或确认 contrib/free 模块支持 | HOLD |
| P1 | `BFMatcher_create` | 原缺失或未主推 | `cv2.BFMatcher_create` | 已增加 Python 风格工厂函数，映射到 `BFMatcher` 并测试 | DONE |
| P1 | `FlannBasedMatcher_create` | 原缺失 | `cv2.FlannBasedMatcher_create` | 已封装 FlannBasedMatcher 基础工厂函数 | DONE |
| P2 | `DescriptorMatcher_create` | 缺失 | `cv2.DescriptorMatcher_create` | 增加工厂函数 | TODO |
| P2 | `FastFeatureDetector_create` | 缺失 | `cv2.FastFeatureDetector_create` | 增加工厂函数 | TODO |
| P2 | `AgastFeatureDetector_create` | 缺失 | `cv2.AgastFeatureDetector_create` | 增加工厂函数 | TODO |
| P2 | `GFTTDetector_create` | 缺失 | `cv2.GFTTDetector_create` | 增加工厂函数 | TODO |
| P2 | `MSER_create` | 缺失 | `cv2.MSER_create` | 增加工厂函数 | TODO |
| P2 | `SimpleBlobDetector_create` | 缺失 | `cv2.SimpleBlobDetector_create` | 增加工厂函数 | TODO |
| P2 | `drawMatchesKnn` | 缺失 | `cv2.drawMatchesKnn` | 增加 KNN 匹配绘制函数 | TODO |
| P2 | `KeyPoint_convert` | 缺失 | `cv2.KeyPoint_convert` | 增加 KeyPoint 转点工具 | TODO |
| P2 | `KeyPoint_overlap` | 缺失 | `cv2.KeyPoint_overlap` | 增加 KeyPoint 重叠度工具 | TODO |

## 6. calib3d 待补齐函数

| 优先级 | 函数名 | 当前情况 | Python OpenCV 对齐目标 | 待办动作 | 状态 |
| --- | --- | --- | --- | --- | --- |
| P1 | `calibrateCamera` | 缺失 | `cv2.calibrateCamera` | 封装相机标定主函数 | TODO |
| P1 | `solvePnPRansac` | 缺失 | `cv2.solvePnPRansac` | 封装 RANSAC PnP | TODO |
| P1 | `findEssentialMat` | 缺失 | `cv2.findEssentialMat` | 封装本质矩阵估计 | TODO |
| P1 | `recoverPose` | 缺失 | `cv2.recoverPose` | 封装相机姿态恢复 | TODO |
| P1 | `estimateAffine2D` | 缺失 | `cv2.estimateAffine2D` | 封装 2D 仿射估计 | TODO |
| P1 | `estimateAffinePartial2D` | 缺失 | `cv2.estimateAffinePartial2D` | 封装部分仿射估计 | TODO |
| P2 | `calibrateCameraExtended` | 缺失 | `cv2.calibrateCameraExtended` | 评估底层支持后封装 | TODO |
| P2 | `calibrateCameraRO` | 缺失 | `cv2.calibrateCameraRO` | 评估底层支持后封装 | TODO |
| P2 | `solvePnPGeneric` | 缺失 | `cv2.solvePnPGeneric` | 评估底层支持后封装 | TODO |
| P2 | `composeRT` | 缺失 | `cv2.composeRT` | 封装旋转平移组合 | TODO |
| P2 | `decomposeEssentialMat` | 缺失 | `cv2.decomposeEssentialMat` | 封装本质矩阵分解 | TODO |
| P2 | `decomposeHomographyMat` | 缺失 | `cv2.decomposeHomographyMat` | 封装单应矩阵分解 | TODO |
| P2 | `decomposeProjectionMatrix` | 缺失 | `cv2.decomposeProjectionMatrix` | 封装投影矩阵分解 | TODO |
| P2 | `drawChessboardCorners` | 缺失 | `cv2.drawChessboardCorners` | 增加棋盘角点绘制 | TODO |
| P2 | `findChessboardCorners` | 缺失 | `cv2.findChessboardCorners` | 增加棋盘角点检测 | TODO |
| P2 | `findCirclesGrid` | 缺失 | `cv2.findCirclesGrid` | 增加圆点阵检测 | TODO |
| P2 | `stereoCalibrate` | 缺失 | `cv2.stereoCalibrate` | 增加双目标定 | TODO |
| P2 | `stereoRectify` | 缺失 | `cv2.stereoRectify` | 增加双目校正 | TODO |

## 7. highgui 待补齐函数

| 优先级 | 函数名 | 当前情况 | Python OpenCV 对齐目标 | 待办动作 | 状态 |
| --- | --- | --- | --- | --- | --- |
| P1 | `createTrackbar` | 缺失 | `cv2.createTrackbar` | 增加滑块控件封装 | TODO |
| P1 | `getTrackbarPos` | 缺失 | `cv2.getTrackbarPos` | 增加读取滑块位置 | TODO |
| P1 | `setTrackbarPos` | 缺失 | `cv2.setTrackbarPos` | 增加设置滑块位置 | TODO |
| P1 | `setMouseCallback` | 缺失 | `cv2.setMouseCallback` | 增加窗口鼠标回调 | TODO |
| P2 | `selectROI` | 缺失 | `cv2.selectROI` | 增加 ROI 选择 | TODO |
| P2 | `selectROIs` | 缺失 | `cv2.selectROIs` | 增加多 ROI 选择 | TODO |
| P2 | `getWindowProperty` | 缺失 | `cv2.getWindowProperty` | 增加窗口属性读取 | TODO |
| P2 | `setWindowProperty` | 缺失 | `cv2.setWindowProperty` | 增加窗口属性设置 | TODO |
| P2 | `pollKey` | 缺失 | `cv2.pollKey` | 增加非阻塞按键轮询 | TODO |
| P3 | `displayOverlay` | 缺失 | `cv2.displayOverlay` | 评估是否需要支持 | HOLD |
| P3 | `displayStatusBar` | 缺失 | `cv2.displayStatusBar` | 评估是否需要支持 | HOLD |
| P3 | `createButton` | 缺失 | `cv2.createButton` | 评估是否需要支持 | HOLD |

## 8. video / tracking 待补齐函数 / 类

| 优先级 | 函数 / 类名 | 当前情况 | Python OpenCV 对齐目标 | 待办动作 | 状态 |
| --- | --- | --- | --- | --- | --- |
| P1 | `createBackgroundSubtractorMOG2` | 原缺失 | `cv2.createBackgroundSubtractorMOG2` | 已封装 MOG2 背景建模并测试 `apply` | DONE |
| P1 | `createBackgroundSubtractorKNN` | 原缺失 | `cv2.createBackgroundSubtractorKNN` | 已封装 KNN 背景建模并测试 `apply` | DONE |
| P2 | `KalmanFilter` | 缺失 | `cv2.KalmanFilter` | 封装 KalmanFilter 类 | TODO |
| P2 | `DISOpticalFlow_create` | 缺失 | `cv2.DISOpticalFlow_create` | 评估底层支持后封装 | TODO |
| P2 | `FarnebackOpticalFlow_create` | 缺失 | `cv2.FarnebackOpticalFlow_create` | 评估底层支持后封装 | TODO |
| P2 | `SparsePyrLKOpticalFlow_create` | 缺失 | `cv2.SparsePyrLKOpticalFlow_create` | 评估底层支持后封装 | TODO |
| P3 | `TrackerMIL_create` | 缺失 | `cv2.TrackerMIL_create` | contrib / tracking 相关，按需支持 | HOLD |
| P3 | `TrackerGOTURN_create` | 缺失 | `cv2.TrackerGOTURN_create` | contrib / tracking 相关，按需支持 | HOLD |
| P3 | `TrackerDaSiamRPN_create` | 缺失 | `cv2.TrackerDaSiamRPN_create` | contrib / tracking 相关，按需支持 | HOLD |
| P3 | `TrackerNano_create` | 缺失 | `cv2.TrackerNano_create` | contrib / tracking 相关，按需支持 | HOLD |

## 9. photo / HDR / tonemap 待补齐函数

| 优先级 | 函数名 | 当前情况 | Python OpenCV 对齐目标 | 待办动作 | 状态 |
| --- | --- | --- | --- | --- | --- |
| P2 | `createAlignMTB` | 缺失 | `cv2.createAlignMTB` | 封装 HDR 图像对齐 | TODO |
| P2 | `createCalibrateDebevec` | 缺失 | `cv2.createCalibrateDebevec` | 封装 Debevec 标定 | TODO |
| P2 | `createCalibrateRobertson` | 缺失 | `cv2.createCalibrateRobertson` | 封装 Robertson 标定 | TODO |
| P2 | `createMergeDebevec` | 缺失 | `cv2.createMergeDebevec` | 封装 Debevec HDR 合并 | TODO |
| P2 | `createMergeMertens` | 缺失 | `cv2.createMergeMertens` | 封装 Mertens 曝光融合 | TODO |
| P2 | `createMergeRobertson` | 缺失 | `cv2.createMergeRobertson` | 封装 Robertson HDR 合并 | TODO |
| P2 | `createTonemap` | 缺失 | `cv2.createTonemap` | 封装基础 Tonemap | TODO |
| P2 | `createTonemapDrago` | 缺失 | `cv2.createTonemapDrago` | 封装 Drago Tonemap | TODO |
| P2 | `createTonemapMantiuk` | 缺失 | `cv2.createTonemapMantiuk` | 封装 Mantiuk Tonemap | TODO |
| P2 | `createTonemapReinhard` | 缺失 | `cv2.createTonemapReinhard` | 封装 Reinhard Tonemap | TODO |

## 10. `Mat` / 对象方法差异说明

| 优先级 | 对象 / 方法 | 当前情况 | Python OpenCV 对齐目标 | 待办动作 | 状态 |
| --- | --- | --- | --- | --- | --- |
| P1 | `cv2.Mat` | aardio 使用自定义 `Mat` 包装 OpenCvSharp Mat | Python 主要使用 `numpy.ndarray` | 已在 `docs/PythonApiCompatibility.md` 说明语言差异，不承诺完全等价 numpy API | DONE |
| P1 | `Mat.get` / `Mat.set` | aardio 自定义像素读写接口 | Python 使用 numpy 下标 | 已在兼容文档中增加 numpy 下标到 `Mat.get` / `Mat.set` 的迁移示例 | DONE |
| P2 | `Mat.toBytes` / `toFloatArray` / `toDoubleArray` | aardio 便利方法 | Python 无同名 Mat 方法 | 文档标记为 aardio 扩展方法 | TODO |
| P2 | `Mat.clone` / `row` / `col` / `roi` | 更接近 C++ / OpenCvSharp Mat 方法 | Python numpy 有不同切片语义 | 文档说明与 Python 示例迁移方式 | TODO |
