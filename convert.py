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
    # 处理表格字段
    # 两个平台上的表格都是一个列表
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

    # 处理文件字段
    # 国家平台上的文件是一个列表
    elif dst == 'files':
      pass

    else:
      matchs = parse(src).find(data)
      if len(matchs) == 1:
        print(matchs[0].value)
        template = parse(dst).update(template, matchs[0].value)
    
  return template

def download_file(url, path='files', filename=''):
  # 下载文件，并返回文件保存路径
  r = requests.get(url).content
  filename = get_file_name(url, r.headers)
  with open(os.path.join(path, filename), 'wb+') as f:
    f.write(r)
  return os.path.join(path, filename)

def get_file_name(url, headers):
  # 获取文件名
  # https://blog.csdn.net/mbh12333/article/details/103721834
  filename = ''
  if 'Content-Disposition' in headers and headers['Content-Disposition']:
    disposition_split = headers['Content-Disposition'].split(';')
    if len(disposition_split) > 1:
      if disposition_split[1].strip().lower().startswith('filename='):
        file_name = disposition_split[1].split('=')
        if len(file_name) > 1:
          filename = unquote(file_name[1])
  elif not filename and os.path.basename(url):
      filename = os.path.basename(url).split("?")[0]
  elif filename == '' and data_type != '':
    filename = str(uuid.uuid4())
  else:
    raise Exception('文件名未指定')
  return filename

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



