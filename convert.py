# 根据用户提供的template_conversion.json
# 将csds的数据格式转化为国家平台的格式
# template_conversion.json 定义了一系列键值对
# 键 是国家平台模板字段的路径
# 值 是csds模板值的路径
# 本程序就是根据template_conversion提供的键值对，将csds的值填充到国家平台模板中

import os
import sys
import json
import re
from functools import reduce
from jsonpath_ng import jsonpath, parse


# project_path = os.path.abspath('.')
# sys.path.append(project_path)
# from utils.parse_tree import parse

def parse_field(expr):
  """
  将"('规定非比例延伸强度', '强度')"解析为['规定非比例延伸强度', '强度']
  """
  l = re.split(r"[',]", expr[1: -1])
  l = [i for i in l if i not in ['', ' ']]
  return l

def data_convert(template, data, tc):
  """
    template  要填充的模板
    data      数据来源
    tc        对应关系
  """
  for dst, src in tc.items():
    if '(' in dst:
      values = []
      src_groups = re.match(r'(.*?)\.\((.*?)\)', src)
      dst_groups = re.match(r'(.*?)\.\((.*?)\)', dst)
      records = parse(src_groups.group(1) + '.[*]').find(data)
      for record in records:
        t = {}
        for field, value in zip(parse_field(dst_groups.group(2)), parse_field(src_groups.group(2))):
          matches = parse(value).find(record)
          if matches:
            t[field] = parse(value).find(record)[0].value
        values.append(t)
      # 获取要更新的字段
      template = parse(dst_groups.group(1)).update(template, values)
      
    else:
      matchs = parse(src).find(data)
      if len(matchs) == 1:
        print(matchs[0].value)
        template = parse(dst).update(template, matchs[0].value)
    
  return template

if __name__ == '__main__':
  with open('json_files/性能数据.json', 'r', encoding='UTF-8') as f:
    file_template = json.load(f)
  data_template = file_template['data'][0]

  with open('json_files/template_conversion.json', encoding='UTF-8') as f:
    tc = json.load(f)

  with open('json_files/data.json', encoding='UTF-8') as f:
    data_list = json.load(f)

  for data in data_list[:5]:
    res = data_convert(data_template, data, tc)
    
    print(res)



