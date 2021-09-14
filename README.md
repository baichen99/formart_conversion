## 文件结构

- json_files                              存放json文件
- json_files/性能数据.json                  国家平台上的数据模板
- json_files/data.json                     mdcs数据
- json_files/template_conversion.json     用户配置的文件

现在写了两个版本
## test/test2.ipynb

1. 从mdcs下载原始数据的json文件 A
2. 在国家平台上新建模板，这个字段要包含学校平台上使用的数据的字段
3. 下载模板json文件 B
4. 用json模块把所有字段提取出来，再将其写入数据模板`data_template`
5. 处理多个文件，并且下载其中的文件

这种方法需要在代码中提取每一个字段，坏处是对每个模板都要写一个脚本

## convert.py

1. 用户创建`template_conversion.json`文件，其中键为模板字段的路径，值为mdcs数据的值的路径

```json
{
  "meta.'标题'": "title",
  "meta.'数据生产者'": "dict_content.data-source.SJTU-al-mmc-property.information.data-source",
  "meta.'上传日期'": "dict_content.data-source.SJTU-al-mmc-property.information.upload-date",
  "content.'力学性能'.'测试样品编号'": "dict_content.SJTU-al-mmc-property.mechanical-property.number-of-test-sample",
  "content.'力学性能'.'测试样品含量'": "dict_content.SJTU-al-mmc-property.mechanical-property.volume-ratio-of-reinforcement-in-test-sample.value",
  "content.'力学性能'.'测试日期'": "dict_content.SJTU-al-mmc-property.mechanical-property.test-date",
  "content.'力学性能'.'测试人'": "dict_content.SJTU-al-mmc-property.mechanical-property.tester",
  "content.'力学性能'.'规定塑性延伸强度'.('规定非比例延伸强度', '强度')": "dict_content.SJTU-al-mmc-property.mechanical-property.specifies-the-plastic-elongation-strength.specifies-the-plastic-elongation-strength-record.('strength.value', 'rp')"
}
```

2. 根据用户的配置来处理，这样灵活性比较强，只需要每个模板写一个配置文件`template_conversion.json`就可以

### todo

- 处理文件字段，要对文件下载，并且把保存路径写到模板中
- 实现数据ID自增
- 一些常量元数据不需要重复在`template_conversion.json`里配置
