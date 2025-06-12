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

```json
{
  "offset": { "x": 0, "y": 0 },
  "pixels": [
    { "x": 60, "y": 100, "color": "#ff4d75" },
    { "x": 70, "y": 100, "color": "#ff4d75" },
    { "x": 80, "y": 110, "color": "#ff4d75" }
    ...
  ]
}
```

### 参数

| 参数    | 功能                                   |
| ------- | -------------------------------------- |
| -m      | 指定模式                               |
| -t      | circ 文件地址                          |
| -t_np   | 不带图片的 circ 文件保存地址           |
| -rep    | 像素库的文件夹路径                     |
| -lc     | circ 文件的 circuit 标签名称           |
| -lr     | 库的 circuit 标签名称                  |
| -p      | 图片地址                               |
| -pos    | 像素偏移，两个整数用逗号隔开，没有空格 |
| -rm_cur | 是否删除原先的像素信息                 |
| -h      | 打印帮助信息                           |

### 模式

O: 必须参数<br>
X: 无效参数<br>
Y: 可选参数<br>

| 模式  | -t  | -t_np | -rep | -lc | -lr | -p  | -pos | -rm_cur | 功能                                                                                                                |
| ----- | --- | ----- | ---- | --- | --- | --- | ---- | ------- | ------------------------------------------------------------------------------------------------------------------- |
| del   | O   | X     | X    | O   | X   | X   | X    | X       | 删除指定目标 circuit 标签下的所有像素                                                                               |
| add   | O   | X     | X    | O   | X   | O   | Y    | Y       | 将图片添加到目标 circ 文件                                                                                          |
| conv  | X   | X     | O    | X   | O   | O   | Y    | X       | 将图片转换为像素信息，保存到像素库                                                                                  |
| load  | O   | X     | O    | O   | O   | X   | Y    | Y       | 从像素库加载像素信息到目标 circ 文件                                                                                |
| store | O   | X     | X    | O   | O   | O   | Y    | X       | 将指定 circ 文件的指定 circuit 标签下的像素信息存储到库                                                             |
| 去图  | O   | O     | X    | X   | X   | X   | X    | X       | 从目标 circ 文件中去除**所有** circuit 标签下的所有像素，并保存到目标地址                                           |
| 上图  | O   | O     | O    | X   | X   | X   | X    | X       | 将像素库的**所有**像素信息添加到目标 circ 文件的相对应的 circuit 标签下 <br> 然后把更新后的 circ 文件保存到指定位置 |

---

### 主要函数

```python

def 解析图像文件(图片地址: str, dx: int, dy: int) -> str:
def 清除原有像素(目标circ文件地址: str, 目标circuit名称: str) -> None:
def 添加新像素(目标circ文件地址: str, 目标circuit名称: str, 新内容: str) -> None:
def 获取像素信息(目标circ文件地址: str, 目标circuit名称: str) -> str:

```
