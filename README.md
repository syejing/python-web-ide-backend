# python-web-ide-backend

#### 介绍
Python Web IDE 后端，采用Tornado，一种Python Web框架。

#### 软件架构
![avatar](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA+IAAAC0CAYAAAAQJZY8AAAgAElEQVR4Xu2dCfht1fjHd39lDBFChQxxQ2aVIclQKmOhNBhKE6nMIlcis0pUIkODQhkrZawMFTKEIkOoECJcoaL/89nu+ll333PO7/zOOXvftfb6rOe5D9179t5rfda73/V+13rX2itdc80111cWCUhAAhKQgAQkIAEJSEACEpCABDohsJJCvBPOPkQCEpCABCQgAQlIQAISkIAEJFATUIhrCBKQgAQkIAEJSEACEpCABCQggQ4JKMQ7hO2jJCABCUhAAhKQgAQkIAEJSEACCnFtQAISkIAEJCABCUhAAhKQgAQk0CEBhXiHsH2UBCQgAQlIQAISkIAEJCABCUhAIa4NSEACEpCABCQgAQlIQAISkIAEOiSgEO8Qto+SgAQkIAEJSEACEpCABCQgAQkoxLUBCUhAAhKQgAQkIAEJSEACEpBAhwQU4h3C9lESkIAEJCABCUhAAhKQgAQkIAGFuDYgAQlIQAISkIAEJCABCUhAAhLokIBCvEPYPkoCEpCABCQgAQlIQAISkIAEJKAQ1wYkIAEJSEACEpCABCQgAQlIQAIdElCIdwjbR0lAAhKQgAQkIAEJSEACEpCABBTi2oAEJCABCUhAAhKQgAQkIAEJSKBDAgrxDmH7KAlIQAISkIAEJCABCUhAAhKQgEJcG5CABCQgAQlIQAISkIAEJCABCXRIQCHeIWwfJQEJSEACEpCABCQgAQlIQAISUIhrAxKQgAQkIAEJSEACEpCABCQggQ4JKMQ7hO2jJCABCUhAAhKQgAQkIAEJSEACCnFtQAISkIAEJCABCUhAAhKQgAQk0CEBhXiHsH2UBCQgAQlIQAISkIAEJCABCUhAIa4NSEACEpCABCQgAQlIQAISkIAEOiSgEO8Qto+SgAQkIAEJSEACEpCABCQgAQkoxLUBCUhAAhKQgAQkIAEJSEACEpBAhwQU4h3C9lESkIAEJCABCUhAAhKQgAQkIAGFuDYgAQlIQAISkIAEJCABCUhAAhLokIBCvEPYPkoCEpCABCQgAQlIQAISkIAEJKAQ1wYkIAEJSEACEpCABCQgAQlIQAIdElCIdwjbR0lAAhKQgAQkIAEJSEACEpCABBTi2oAEJCABCUhAAhKQgAQkIAEJSKBDAgrxDmH7KAlIQAISkIAEJCABCUhAAhKQgEJcG5CABCQgAQlIQAISkIAEJCABCXRIQCHeIWwfJQEJSEACEpCABCQgAQlIQAISUIhrAxKQgAQkIAEJSEACEpCABCQggQ4JKMQ7hO2jJCABCUhAAhKQgAQkIAEJSEACSQvxK664ojrhhBOqSy65pLrsssuqyy+/3B6TwFgE1lxzzWqttdaq1llnnWq77bar1lhjjbGu80cSkEC6BE477bTqnHPOqceDSy+9tFqyZEm6lbVmyRBYddVVq7XXXrseEzbaaKNqiy22SKZuVkQCEhhOQJ+vdUxCICefn6wQP/7446sjjzyyuvbaayfpA6+RwByBVVZZpdp9992r7bffXioSkECGBC6++OLqiCOOqEW4RQLTEkCM77HHHtW666477a28XgISaIGAPr8FqAXfMmWfn6QQR4QfdthhBZuMTW+DwF577aUYbwOs95RAiwSYjN1mm20qMqQsEpgVAbKkTjrppIqJWosEJJAOAX1+On3Rp5qk6vOTE+IEWwRdYSV80aJF1a677lqnlfFn5ZVX7pNd2JYWCFx33XV12ip/jjrqqOqiiy6qn0LAReBlmnoL0L2lBFoiwKQsk7Oh7LTTTtUmm2xSpxmvvvrqLT3V2/aJwJVXXllvZzjzzDOrY445Zq5pZEkxQWuRgATSIaDPT6cvcq1JTj4/OSF+yCGHVCeeeGLd94jw4447Llc7sN6JENhhhx3mxPi2225b7bPPPonUzGpIQAKjCFx11VXV5ptvPveTAw44oNpqq62EJoGJCZxyyinV4sWL564//fTTq9VWW23i+3mhBCQwOwL6/Nmx9E7/JZC6z09OiO+9997VeeedV8M7+OCDq4033lhbksBUBM4+++xq3333re+xwQYbVIceeuhU9/NiCUigGwIXXHBBnRFFWW+99apjjz22mwf7lF4T2HHHHasLL7ywbiNZU+uvv36v22vjJJALAX1+Lj2VVz1T9vnJCfGtt9567nR00og59doigWkIcOo+2x0onKZ+8sknT3M7r5WABDoicOqpp1YHHnhg/bTNNtusOuiggzp6so/pM4H99tuvOuOMM+om7r///tWWW27Z5+baNglkQ0Cfn01XZVXRlH1+ckJ8ww03nOtcVsbdE56VrSdZWfaMsxIeyrnnnptkPa2UBCSwLIH3v//9FX8oO++8c7XnnnuKSAJTEzj8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)

前端用vue2框架，后端用tornado框架，交互式解释器是对CPython进行封装。

##### 版本描述

node == v10.20.0

npm == 6.14.5

vue == 2.5.2

@vue/cli == 3.8.4

python == 3.7.0

tornado == 6.0.4

libzmq == 4.3.2

pyzmq == 19.0.2

anaconda == 4.9.1

numpy == 1.19.2

pandas == 1.16.4

matplotlib == 3.2.2

seaborn == 0.10.1

alphalens == 0.4.0

#### 安装教程

``` bash
# serve at localhost:8090
python server.py
```

#### 使用说明

1. 输出

   - 加法计算

     ```python
     1+1
     ```

   - 打印输出

     ```python
     print('hello repl')
     ```

   - 赋值计算

     ```python
     a=3
     b=4
     c=a+b
     c
     ```

   - 多行打印

     ```python
     a
     b
     c
     ```

     ```python
     print(a)
     print(b)
     print(c)
     ```

   - 循环判断

     ```python
     for i in [1,2,3,4,5,6]:
         if i%2 == 0:
             print(i)
     ```

2. 输入

   ```python
   a = input('请输入值:')
   a
   ```

   ```python
   a = input('请输入a值:')
   b = input('请输入b值:')
   print(a)
   print(b)
   ```

3. 报错

4. 补全

5. numpy

   ```python
   import numpy as np
   arr = np.array([1,2,3,4,5])
   arr
   ```

6. pandas

   ```python
   import pandas as pd
   data = {
       'state':['Ohio','Ohio','Ohio','Newvda','Newvda','Newvda'],
       'year': [2000,2001,2003,2001,2002,2003],
       'pop': [1.5,1.7,3.6,2.4,2.9,3.2]
   }
   df = pd.DataFrame(data)
   df
   ```

7. matplotlib

   ```python
   from matplotlib import pyplot as plt
   plt.figure()
   plt.plot([1,2,3])
   plt.show()
   ```

   ```python
   plt.figure()
   plt.plot([1,3,2])
   plt.figure()
   plt.scatter([1,2,3],[3,2,3],color="crimson")
   plt.show()
   ```

#### 网络协议

<img src="websocket协议.jpg" alt="websocket协议" style="zoom:100%;" />

###### 请求JSON对象

| 属性     | 类型   | 描述                              |
| -------- | ------ | --------------------------------- |
| mode     | string | 模式：edit 编辑、command 命令行   |
| language | string | 内核语言：python3                 |
| type     | string | 类型：compute 计算、complete 补全 |
| data     | string | 数据                              |
| desc     | object | 描述对象                          |

1. 计算

```javascript
{"mode":"edit","language":"python3","type":"compute","data":"","desc":{}}
```

2. 补全


```javascript
{"mode":"edit","language":"python3","type":"complete","data":"","desc":{}}
```

###### 响应JSON对象

| 属性 | 类型                  | 描述                                                         |
| ---- | --------------------- | ------------------------------------------------------------ |
| id   | string                | 唯一ID                                                       |
| type | string                | 类型：code 代码、output 输出、stream 流、input 输入、error 报错、complete 补全、sequence 序列 |
| code | string                | 代码，非必须                                                 |
| data | object、string、array | 数据                                                         |
| desc | object                | 描述对象                                                     |

1. 代码

   ```javascript
   {"id": "", "type": "code", "data": "", "desc": {}}
   ```

2. 输出

   - 无代码

     ```javascript
     {"id": "", "type": "output", "data": {"type": "text", "content": ""}, "desc": {}}
     ```

   - 文本

     ```javascript
     {"id": "", "type": "output", "code": "", "data": {"type": "text", "content": ""}, "desc": {}}
     ```

   - markdown

     ```javascript
     {"id": "", "type": "output", "code": "", "data": {"type": "markdown", "content": ""}, "desc": {}}
     ```

   - 图片

     ```javascript
     {"id": "", "type": "output", "code": "", "data": {"type": "image", "content": ""}, "desc": {}}
     ```

3. 流

   ```javascript
   {"id": "", "type": "stream", "code": "", "data": "", "desc": {}}
   ```

4. 输入

   ```javascript
   {"id": "", "type": "input"}
   ```

5. 报错

   ```javascript
   {"id": "", "type": "error", "code": "", "data": [], "desc": {}}
   ```

6. 补全

   ```javascript
   {"id": "", "type": "complete", "data": "", "desc": {}}
   ```

7. 序列

   ```javascript
   {"id": "", "type": "sequence", "data": 1, "desc": {}}
   ```

###### 响应数据JSON对象

| 属性    | 类型   | 描述 |
| ------- | ------ | ---- |
| type    | 字符串 | 类型 |
| content | 字符串 | 内容 |

1. 文本

   ```javascript
   {"type": "text", "content": ""}
   ```

2. markdown

   ```javascript
   {"type": "markdown", "content": ""}
   ```

3. 图片

   ```javascript
   {"type": "image", "content": ""}
   ```