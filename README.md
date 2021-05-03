# ads_captcha_recognition

针对数据安全部的产品的验证码，用tesseract-ocr训练了一套自己的识别库，并将整套代码docker化，打包成了镜像。
本次训练数据使用了200张的验证码，识别准确率可达95%+

### 使用方法

#### 1.拉取镜像
```bash
docker pull yanqiaoyu/ads_captcha:latest
```

#### 2.运行
```bash
# --rm：器退出时就能够自动清理容器内部的文件系统
# -v {captcha_image_path}:/app/pic: 把你存放验证码的路径，映射到容器的/app/pic中
# -n {image_name}: 验证码图片的名字，与你{captcha_image_path}目录下的名字保持一致
docker run --rm \
-v {captcha_image_path}:/app/pic \
ads_captcha \
-n {image_name}
```

### 构建方法
#### 1.拉取源码
```shell
git clone https://github.com/yanqiaoyu/ads_captcha_recognition.git
```

#### 2.编译
```shell
cd ads_captcha_recognition/
docker build -t ads_captcha .
```

### 一些问题

#### 1. 为什么要自己训练？
1) 在接口测试时，执行相关的业务之前通常都需要登录，否则无法授权执行。此时我们当然可以要求关闭验证码进行测试，但这样终究是改变了测试环境，影响最终结论。
2) 如果直接使用tesseract自带的训练数据去识别这个验证码，偶尔能识别出来，但是大多数情况识别的都是错误的验证码，非常影响效率。
3) 驱动自己使用不同的技术，不同的角度去解决问题，完善自己方法论的多样性

#### 2. 为什么要封装成docker镜像？
1) 一开始我考虑的方案是嵌入代码到我们的自动化框架之中，自行配置tesseract，这样做的好处是，可以针对框架随时修改代码，体积小且轻量。但是实际落地推广时，同学们需要阅读源码之后，再嵌入代码到框架里面，或者自己的工具脚本之中。并且在配置tesseract使用自己的训练数据时，也经常遇到各种问题。这违背了我提高整体工作效率的初衷。
2) 将所有的测试工具docker化，既能够方便他人使用，也能方便自己管理。况且这个模块本身也适合服务化。这对降低落地阻碍，并帮助代码水平不高的同学解决识别验证码的问题，大有帮助。

#### 3.为什么是centos作为基础镜像？为什么不用alpine？
其实一开始尝试过alpine，后来由于有一些依赖找不到，我时间也不多，就暂时用centos的基础镜像了。后续如果对于镜像体积这一块有需求的话，再考虑优化的事情