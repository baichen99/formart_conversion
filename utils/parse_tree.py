import json
import re

def parse(data_json, path):
  """
    给定 "a.b.c"  返回c的值
    如果是有列表 {a: [{value: 1, unit: pa}, {value: 2, unit: pa}]} 用@选择第几个
    a.0.value
  """
  fields = re.split(r'\.', path)
  if len(fields) <= 0:
    raise Exception('分割后的元素个数为0')
  value = data_json
  for f in fields:
    # 检查f这个字段是dict还是list
    if isinstance(value, dict):
      value = value.get(f, {})
    elif isinstance(value, list):
      value = value[int(f)]
  return value
    


  return fields

if __name__ == '__main__':
  with open('test.json') as f:
    data = json.load(f)

  list_path = 'dict_content.SJTU-al-mmc-property.mechanical-property.\
specifies-the-plastic-elongation-strength.\
specifies-the-plastic-elongation-strength-record.0.strength.value'

  dict_path = 'dict_content.SJTU-al-mmc-property.\
mechanical-property.tensile-strength.value'

  res1 = parse(data, list_path)
  res2 = parse(data, dict_path)
  print(res1, res2)