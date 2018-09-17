# PackageToolGUI

## 修订记录

版本|时间|说明|修改人
---|---|----|---
0.0.1|2018年9月13日|1.初始化工程，移植之前的打包功能到工具GUI内。<br>2.目前实现解包操作。|[vito](https://pinode.cn)
0.0.2|2018年9月17日|1.添加状态机。<br>2.实现重打包。|[vito](https://pinode.cn)



## 说明
 1.这是一个Android分包工具。主要的目的是实现一个母包然后通过修改AndroidManifest文件里面的部分内容实现不同渠道的分发。
 2.这是个简单的工具。
 3.GUI操作
## 环境
 1.这个工具开发于 python2.7.15环境
 2.工具需要Apktool支持。
 3.工具需要java环境支持。最好是安装JDK。
 4.工具没有做好。
 
 ##  extras
 1.使用了enum  在Python 2.7上要使用enum34，并且使用上目前发现
 ```
    states = Enum('states', ('none', 'decompile', 'compile', 'waite))
```
不好用。所以使用的是现在的方法。