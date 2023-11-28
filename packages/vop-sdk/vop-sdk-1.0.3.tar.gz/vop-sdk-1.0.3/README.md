<h1 align="center"><img src="https://iam.volccdn.com/obj/volcengine-public/pic/volcengine-icon.png"></h1>
<h1 align="center">视频云私有化SDK for Python</h1> 
欢迎使用视频云私有化SDK for Python，本文档为您介绍如何获取及调用SDK。

## 前置准备

### 环境检查
Python版本需要不低于2.7。

## 获取与安装

使用pip安装SDK for Python：
```
    pip install --user vop-sdk
```
如果已经安装vop-sdk包，则用下面命令升级即可：
```
    pip install --upgrade vop-sdk
```


## 相关配置
### 安全凭证及域名配置
视频云私有化SDK for Python支持以下几种方式进行凭证管理：

*注意：代码中Your AK及Your SK, Your Host需要分别替换为您的AK及SK, 域名。*

*注意: 下面三种方式，选择一种使用，不要混用。*

**方式一**：在Client中设置AK/SK **（推荐）**
  ``` python
      iam_service = IamService()
      iam_service.set_ak('Your AK')
      iam_service.set_sk('Your SK')
      iam_service.set_host('Your Host')
  ```

**方式二**：从环境变量加载AK/SK
  ```bash
  VOP_ACCESSKEY="Your AK"  
  VOP_SECRETKEY="Your SK"
  VOP_HOST="Your Host"
  ```
**方式三**：从HOME文件加载AK/SK

在本地的~/.vop/config中添加如下内容：
  ```json
    {
      "ak": "Your AK",
      "sk": "Your SK",
      "host": "Your Host"
    }
  ```

## 其它资源
示例参见 https://www.volcengine.com/docs/4/107710
