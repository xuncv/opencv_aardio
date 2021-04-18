# opencv_aardio
dll库下载地址：https://github.com/shimat/opencvsharp/releases

opencv具有500多个跨平台的图像处理函数，是目前应用最广的数字图像库。opencv历史发展过程中由C接口慢慢转向C++接口，使其他语言（python除外）调用opencv的难度增大。最近找到一个针对.NET的封装库项目[OpenCvSharp ](https://github.com/shimat/opencvsharp) ，对opencv的接口进行了重新封装，对opencv版本的跟进也很及时。

虽然这个库面向.NET，但其封装的接口对aardio异常友好。使用aardio调用dll时，甚至比.NET更简单方便。

比如Mat类作为参数时，.NET的实现是添加一个CvPtr成员，用来存储Mat指针，然后每次需取一次CvPtr作为dll接口的指针，一次api调用需要封装3次。aardio的实现就非常优雅，在mat类代码中只需修改下属性表,就可以让dll直接使用aardio的mat对象

```
_metaProperty = ..util.metaProperty(
		_topointer = function(){
			return owner.handle; 
		}
		...
)		
```

甚至不需要声明API接口，就可以直接调用API。

```
var imread = dll["imgcodecs_imread"];
imread(srcMat,1);
```

基于以上几点，我开始尝试使用aardio对opencv进行封装，接口实现上尽量接近opencv-python风格，降低学习成本。

aardio原生支持opencv，我希望能解决以下问题：

1. 充分融合aardio的胶水特性，增强aardio图像处理能力。
2. 结合aardio桌面优势，如制作上位机软件时可提高工程进度。
3. 使opencv项目轻量化。（我的conda文件夹已经10+G了）。
4. 提高opencv启动速度，在算法测试中提高效率。

`2021年4月18日`

