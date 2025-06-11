# Logisim Draw

### circ 文件结构

```html
<a>
  ...
  <circuit name="test">
    ...
    <appear>
      <rect fill="#ff4d75" height="1" stroke="none" width="1" x="60" y="100" />
      <rect fill="#ff4d75" height="1" stroke="none" width="1" x="70" y="100" />
      <rect fill="#ff4d75" height="1" stroke="none" width="1" x="80" y="110" />
      ...
      <rect fill="#ffffff" height="65" stroke="#000000" stroke-width="2" width="88" x="90" y="112" />
      <circ-port height="8" pin="140,210" width="8" x="46" y="66" />
      <circ-anchor facing="east" height="6" width="6" x="77" y="57" />
    </appear>
  </circuit>
</a>
```

### 参数

| 参数        | 功能                   |
| ----------- | ---------------------- |
| -m          | 指定 模式              |
| -t          | 指定 目标              |
| -s          | 指定 源                |
| -l          | 指定 circuit 标签名称  |
| -h --help   | 打印帮助信息           |
| -rm_current | 是否删除原先的像素信息 |

### 模式

| 模式         | 功能                                                                                                                | -t                 | -t1               | -s                  | -l               | -rm_current |
| ------------ | ------------------------------------------------------------------------------------------------------------------- | ------------------ | ----------------- | ------------------- | ---------------- | ----------- |
| del          | 删除指定目标 circuit 标签下的所有像素                                                                               | circ 文件地址      | 无效              | 无效参数            | circuit 标签名称 | 无效        |
| add          | 将图片添加到目标 circ 文件                                                                                          | circ 文件地址      | 无效              | 待加载图像地址      | circuit 标签名称 | 有效        |
| conv         | 将图片转换为像素信息                                                                                                | 像素库的文件夹路径 | 无效              | 待加载图像地址      | circuit 标签名称 | 无效        |
| load         | 从像素库的 html 文件加载像素信息到目标 circ 文件                                                                    | circ 文件地址      | 无效              | 像素库的文件夹路径  | circuit 标签名称 | 有效        |
| store        | 将指定 circ 文件的指定 circuit 标签下的像素信息存储到指定的 HTML 文件中                                             | 像素库的文件夹路径 | 无效              | circ 文件地址       | circuit 标签名称 | 无效        |
| 去图         | 从目标 circ 文件中去除**所有** circuit 标签下的所有像素，并保存到目标地址                                           | 目标 circ 文件地址 | 无效              | 源 circuit 文件地址 | 无效             | 无效        |
| 上图（todo） | 将像素库的**所有**像素信息添加到目标 circ 文件的相对应的 circuit 标签下 <br> 然后把更新后的 circ 文件保存到指定位置 | 目标 circ 文件地址 | circ 文件保存地址 | 源像素库文件夹路径  | 无效             | 有效        |

### 主要函数

```python

def 解析图像文件(图片地址: str, dx: int, dy: int) -> str:
def 清除原有像素(目标circ文件地址: str, 目标circuit名称: str) -> None:
def 添加新像素(目标circ文件地址: str, 目标circuit名称: str, 新内容: str) -> None:
def 获取像素信息(目标circ文件地址: str, 目标circuit名称: str) -> str:

```
