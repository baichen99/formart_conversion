## 文件结构

- 性能数据  国家平台上的数据模板

我们要把cdcs上的数据转化为国家平台上的格式
## test/test2.ipynb

1. 从cdcs下载原始数据的json文件 A
2. 在国家平台上新建模板，这个字段要包含学校平台上使用的数据的字段
3. 下载模板json文件 B
4. 用json模块把所有字段提取出来，再将其写入数据模板`data_template`
5. 处理多个文件，并且下载其中的文件

这种方法坏处是对每个模板都要写一个脚本

## user_test/convert

1. 用户创建`template_conversion.json`文件，其中键为模板字段的路径，值为cdcs数据的值的路径

```json
{
  "meta.标题": "title",
  "meta.数据生产者": "dict_content.data-source.SJTU-al-mmc-property.information.data-source",
  "meta.上传日期": "dict_content.data-source.SJTU-al-mmc-property.information.upload-date",
  "data.content.力学性能.测试样品编号": "dict_content.SJTU-al-mmc-property.mechanical-property.number-of-test-sample",
  "data.content.力学性能.测试样品含量": "dict_content.SJTU-al-mmc-property.mechanical-property.volume-ratio-of-reinforcement-in-test-sample",
  "data.content.力学性能.测试日期": "dict_content.SJTU-al-mmc-property.mechanical-property.test-date",
  "data.content.力学性能.测试人": "dict_content.SJTU-al-mmc-property.mechanical-property.tester",
  "data.content.力学性能.规定塑性延伸强度.(规定非比例延伸强度, 强度)": "dict_content.SJTU-al-mmc-property.mechanical-property.specifies-the-plastic-elongation-strength.specifies-the-plastic-elongation-strength-record.(strength.value, rp)"
}
```

2. 根据用户的配置来处理，这样灵活性比较强，只需要每个模板写一个配置文件`template_conversion`就可以

3. 要处理的特殊字段有表格、文件。表格是一个list，要分别对其中的表项进行提取。文件则需要下载。