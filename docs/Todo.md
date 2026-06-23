# OpenCV Python API 对齐 Todo

> 目标：记录 aardio `cv2` 封装与 Python OpenCV API 的对齐进度。当前文档中不再保留未解释的待处理项：能在当前 OpenCvSharp 4.5.3 后端稳定实现的项标为 `DONE`；受底层版本、contrib、回调桥接或复杂对象 API 限制的项标为 `HOLD` 并说明原因。
>
> 状态说明：
> - `DONE`：已实现、已测试或已在兼容文档中明确说明。
> - `HOLD`：暂缓；通常因为当前 OpenCvSharp 构建不支持、需要 opencv-contrib、需要额外回调桥接设计，或对象生命周期 / 多输出数组 API 复杂且暂未纳入当前封装范围。

## 1. 模块结构 / 命名空间对齐

| 优先级 | 模块 / 名称 | 当前结论 | 状态 |
| --- | --- | --- | --- |
| P0 | `cv2.dnn` | 已同步挂载 `blobFromImage`、`readNet*`、`NMSBoxes`、`Net` 等到 `cv2.dnn`，保留根命名空间兼容别名。 | DONE |
| P1 | `cv2.utils` | 已同步版本、计时与线程工具到 `cv2.utils`。 | DONE |
| P1 | `cv2.core` / `cv2.imgproc` / `cv2.highgui` 等 | 已在 `docs/PythonApiCompatibility.md` 说明：这些主要是 aardio 内部拆分，公开示例主推 `cv2` 根命名空间。 | DONE |
| P1 | 内部 helper 暴露 | 已在兼容文档中标明 `_size2wh`、`_scalar4`、`_asNetMat` 等为内部实现细节，文档和示例不主推。 | DONE |
| P2 | contrib 扩展模块 | `aruco`、`barcode`、`cuda`、`ml`、`fisheye` 等依赖 opencv-contrib 或额外后端，默认暂缓。 | HOLD |

## 2. `cv2.dnn` 对齐

| 优先级 | 函数 / 类名 | 当前结论 | 状态 |
| --- | --- | --- | --- |
| P0 | `cv2.dnn.blobFromImage` / `blobFromImages` | 已增加 dnn 子模块别名。 | DONE |
| P0 | `cv2.dnn.readNet` / `readNetFromONNX` / `readNetFromOnnx` / `readNetFromCaffe` / `readNetFromDarknet` / `readNetFromTensorflow` / `readNetFromTorch` | 已增加 dnn 子模块别名，推荐 `readNetFromONNX`。 | DONE |
| P0 | `cv2.dnn.NMSBoxes` / `nmsBoxes` | 已增加 dnn 子模块别名。 | DONE |
| P0 | `cv2.dnn.Net` / `DnnNet` | 已导出 `cv2.dnn.Net` / `cv2.dnn.DnnNet`，根命名空间 `cv2.Net` 保持兼容。 | DONE |

## 3. 命名风格对齐 / 扩展函数说明

| 优先级 | 当前名称 | Python 对齐目标 / 结论 | 状态 |
| --- | --- | --- | --- |
| P1 | `BitwiseAnd` / `bitwiseAnd` | 已保留兼容别名，并主推 / 测试 `bitwise_and`。 | DONE |
| P1 | `BitwiseOr` / `bitwiseOr` | 已保留兼容别名，并主推 / 测试 `bitwise_or`。 | DONE |
| P1 | `BitwiseXor` / `bitwiseXor` | 已保留兼容别名，并主推 / 测试 `bitwise_xor`。 | DONE |
| P1 | `BitwiseNot` / `bitwiseNot` | 已保留兼容别名，并主推 / 测试 `bitwise_not`。 | DONE |
| P1 | `camShift` | 已主推 / 测试 Python 风格 `CamShift`，保留 `camShift` 兼容。 | DONE |
| P1 | `denoiseTVL1` | 已增加 Python 风格 `denoise_TVL1` 别名并测试。 | DONE |
| P2 | `convexHullIndices` | 作为 aardio 便利函数保留；Python 风格可用 `convexHull(..., returnPoints=false)` 语义理解。 | DONE |
| P2 | `contourMoments` | 已存在 Python 风格 `moments`，`contourMoments` 作为兼容 / 便利别名弱化。 | DONE |
| P2 | `applyCLAHE` | 已有 `createCLAHE` / `CLAHE.apply` 用法，`applyCLAHE` 作为便利函数保留。 | DONE |
| P2 | `Abs` / `CopyTo` / `Format` | 作为 OpenCvSharp / aardio 扩展函数保留，不作为 Python 对齐 API 主推。 | DONE |
| P2 | `Sum` | 已有 Python 风格 `sumElems`，旧别名作为兼容保留。 | DONE |
| P2 | `cvRound` / `cvFloor` / `cvCeil` | C API / 宏风格函数，Python 通常不直接主推，保留为扩展项。 | HOLD |

## 4. 返回值 / 语义对齐

| 优先级 | 函数名 | Python OpenCV 行为 / 当前结论 | 状态 |
| --- | --- | --- | --- |
| P0 | `findHomography` | 已改为返回 `H, mask`。 | DONE |
| P0 | `findFundamentalMat` | 已改为返回 `F, mask`。 | DONE |
| P1 | `imencode` | 已改为返回 `true, bytes`，对齐 Python `(retval, buf)`，并更新测试。 | DONE |
| P1 | `imread` | 保留 aardio 风格 `null, err`；兼容文档已说明迁移时判断第一个返回值即可。 | DONE |
| P1 | `VideoCapture.read` | 已按 `(ret, frame)` 风格测试。 | DONE |
| P1 | `threshold` | 已按 `(retval, dst)` 风格测试。 | DONE |
| P1 | `findContours` | 已按 OpenCV 4 Python `(contours, hierarchy)` 风格测试。 | DONE |

## 5. features2d 对齐

| 优先级 | 函数 / 类名 | 当前结论 | 状态 |
| --- | --- | --- | --- |
| P1 | `AKAZE_create` | 已封装 OpenCvSharp AKAZE 并测试。 | DONE |
| P1 | `BRISK_create` | 已封装 OpenCvSharp BRISK 并测试。 | DONE |
| P1 | `KAZE_create` | 已封装 OpenCvSharp KAZE 并测试。 | DONE |
| P1 | `SIFT_create` | 当前 OpenCvSharp 4.5.3 构建未暴露 `OpenCvSharp.SIFT` 类型，需升级后端或确认 contrib/free 模块。 | HOLD |
| P1 | `BFMatcher_create` | 已增加 Python 风格工厂函数并测试。 | DONE |
| P1 | `FlannBasedMatcher_create` | 已封装基础工厂函数。 | DONE |
| P2 | `DescriptorMatcher_create` | 已增加 `BruteForce` / `BruteForce-L1` / `BruteForce-Hamming` / `FlannBased` 映射并测试。 | DONE |
| P2 | `FastFeatureDetector_create` | 已封装并测试 `detect`。 | DONE |
| P2 | `AgastFeatureDetector_create` | 已封装并测试 `detect`。 | DONE |
| P2 | `GFTTDetector_create` | 已封装并测试 `detect`。 | DONE |
| P2 | `MSER_create` | 已封装并测试 `detect`。 | DONE |
| P2 | `SimpleBlobDetector_create` | 已封装并测试 `detect`。 | DONE |
| P2 | `drawMatchesKnn` | 当前 wrapper 尚未提供 KNN match 嵌套结果对象，暂缓。 | HOLD |
| P2 | `KeyPoint_convert` | 已增加 KeyPoint 转点数组工具并测试。 | DONE |
| P2 | `KeyPoint_overlap` | 已增加 KeyPoint 圆形区域 IoU 工具并测试。 | DONE |

## 6. calib3d 对齐

| 优先级 | 函数名 | 当前结论 | 状态 |
| --- | --- | --- | --- |
| P1 | `calibrateCamera` | 已封装相机标定主函数并用合成棋盘点测试。 | DONE |
| P1 | `solvePnPRansac` | 已封装 RANSAC PnP 并测试。 | DONE |
| P1 | `findEssentialMat` | 已封装本质矩阵估计并测试。 | DONE |
| P1 | `recoverPose` | 已封装姿态恢复并测试输出形状。 | DONE |
| P1 | `estimateAffine2D` | 已封装 2D 仿射估计并测试。 | DONE |
| P1 | `estimateAffinePartial2D` | 已封装部分仿射估计并测试。 | DONE |
| P2 | `calibrateCameraExtended` / `calibrateCameraRO` | 复杂标定扩展输出较多，暂未纳入当前轻量封装。 | HOLD |
| P2 | `solvePnPGeneric` | 多解输出数组与 Python 返回值差异较大，暂缓。 | HOLD |
| P2 | `composeRT` / `decomposeEssentialMat` / `decomposeHomographyMat` / `decomposeProjectionMatrix` | 可后续按需封装；当前主流程 API 已覆盖，扩展分解函数暂缓。 | HOLD |
| P2 | `drawChessboardCorners` / `findChessboardCorners` / `findCirclesGrid` | 棋盘 / 圆点阵检测绘制可后续按标定专题补充，当前暂缓。 | HOLD |
| P2 | `stereoCalibrate` / `stereoRectify` | 双目标定 / 校正对象输出较复杂，暂缓。 | HOLD |

## 7. highgui 对齐

| 优先级 | 函数名 | 当前结论 | 状态 |
| --- | --- | --- | --- |
| P1 | `createTrackbar` | 已增加封装；当前不反调 aardio 回调，`onChange` 仅占位保持参数位置。 | DONE |
| P1 | `getTrackbarPos` | 已增加封装。 | DONE |
| P1 | `setTrackbarPos` | 已增加封装。 | DONE |
| P1 | `setMouseCallback` | 已导出占位函数并返回明确错误；安全桥接 aardio 回调到 HighGUI 原生回调需单独设计。 | HOLD |
| P2 | `selectROI` | 已增加封装；自动测试仅验证导出，避免阻塞 UI。 | DONE |
| P2 | `selectROIs` | 已增加封装；自动测试仅验证导出，避免阻塞 UI。 | DONE |
| P2 | `getWindowProperty` | 已增加封装。 | DONE |
| P2 | `setWindowProperty` | 已增加封装。 | DONE |
| P2 | `pollKey` | 已增加非阻塞按键轮询封装。 | DONE |
| P3 | `displayOverlay` / `displayStatusBar` / `createButton` | HighGUI 扩展 UI，当前不作为迁移核心目标。 | HOLD |

## 8. video / tracking 对齐

| 优先级 | 函数 / 类名 | 当前结论 | 状态 |
| --- | --- | --- | --- |
| P1 | `createBackgroundSubtractorMOG2` | 已封装 MOG2 背景建模并测试 `apply`。 | DONE |
| P1 | `createBackgroundSubtractorKNN` | 已封装 KNN 背景建模并测试 `apply`。 | DONE |
| P2 | `KalmanFilter` | 对象属性矩阵较多，后续按专题封装。 | HOLD |
| P2 | `DISOpticalFlow_create` / `FarnebackOpticalFlow_create` / `SparsePyrLKOpticalFlow_create` | 当前已有函数式光流 API；对象工厂暂缓。 | HOLD |
| P3 | `TrackerMIL_create` / `TrackerGOTURN_create` / `TrackerDaSiamRPN_create` / `TrackerNano_create` | tracking 多属 contrib / model 相关，按需支持。 | HOLD |

## 9. photo / HDR / tonemap 对齐

| 优先级 | 函数名 | 当前结论 | 状态 |
| --- | --- | --- | --- |
| P2 | `createAlignMTB` / `createCalibrateDebevec` / `createCalibrateRobertson` | HDR 对齐 / 标定对象 API 需要多图像数组与对象生命周期设计，暂缓。 | HOLD |
| P2 | `createMergeDebevec` / `createMergeMertens` / `createMergeRobertson` | HDR 合并对象 API 需要多曝光图像、时间数组和测试素材，暂缓。 | HOLD |
| P2 | `createTonemap` / `createTonemapDrago` / `createTonemapMantiuk` / `createTonemapReinhard` | Tonemap 对象 API 可后续按 HDR 专题补充，暂缓。 | HOLD |

## 10. `Mat` / 对象方法差异说明

| 优先级 | 对象 / 方法 | 当前结论 | 状态 |
| --- | --- | --- | --- |
| P1 | `cv2.Mat` | 已在兼容文档说明 aardio 使用 `cv2.Mat` 包装 OpenCvSharp Mat，不承诺完全等价 numpy API。 | DONE |
| P1 | `Mat.get` / `Mat.set` | 已在兼容文档中增加 numpy 下标到 `Mat.get` / `Mat.set` 的迁移示例。 | DONE |
| P2 | `Mat.toBytes` / `toFloatArray` / `toDoubleArray` | 已在兼容文档中标记为 aardio 扩展便利方法。 | DONE |
| P2 | `Mat.clone` / `row` / `col` / `roi` | 已在兼容文档中说明其 C++ / OpenCvSharp 风格与 Python numpy 切片的迁移关系。 | DONE |
