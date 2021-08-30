## 文件结构

- LD10/ 测试文件夹，包含两个json
- output/ 存放输出的结果
- 性能数据  国家平台上的数据模板

## 流程

1. 从学校平台上下载json文件 A
2. 在国家平台上新建模板，这个字段要包含学校平台上使用的数据的字段
3. 下载模板json文件 B
4. 函数`convert`用json模块把A中的字段全部提取出来，返回一个data。下载附件并保存在`output/A`中
5. 函数`process`处理多个json文件，将data列表替换B中的data字段，并保存为`final.json`文件