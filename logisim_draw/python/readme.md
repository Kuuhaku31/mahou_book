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

| 参数        | 功能                      |
| ----------- | ------------------------- |
| -m          | 指定模式                  |
| -t          | 指定目标文件地址          |
| -s          | 指定源文件地址            |
| -l          | 指定目标 circuit 标签名称 |
| -h --help   | 打印帮助信息              |
| -rm_current | 是否删除原先的像素信息    |

### 模式

| 模式 | 功能                                           | -t                           | -s                             | -l               | -h --help    | -rm_current |
| ---- | ---------------------------------------------- | ---------------------------- | ------------------------------ | ---------------- | ------------ | ----------- |
| del  | 删除指定目标 circuit 标签下的所有像素          | circ 文件地址                | 无效参数                       | circuit 标签名称 | 打印帮助信息 | 无效        |
| add  | 将图片添加到目标 circ 文件                     | circ 文件地址                | 待加载图像地址                 | circuit 标签名称 | 打印帮助信息 | 有效        |
| conv | 将图片转换为像素信息                           | 保存像素信息的 html 文件地址 | 待加载图像地址                 | circuit 标签名称 | 打印帮助信息 | 无效        |
| load | 从指定的 html 文件加载像素信息到目标 circ 文件 | circ 文件地址                | 待加载像素信息的 html 文件地址 | 无效参数         | 打印帮助信息 | 有效        |
