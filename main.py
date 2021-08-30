import xmltodict
import json
import os
import requests

def convert(filename):
  """
  return data   格式化后的单个data
  """
  with open(filename, 'r') as f:
    text = f.read()
  j = json.loads(text)

  # 力学特性的字段
  mechanical_property = j['SJTU-al-mmc-property']['mechanical-property']

  number_of_test_sample = mechanical_property.get('number-of-test-sample')
  volume_ratio_of_reinforcement_in_test_sample = mechanical_property.get('volume-ratio-of-reinforcement-in-test-sample')['value']
  test_date = mechanical_property.get('test-date')
  tester = mechanical_property.get('tester')
  youngs_modulus = mechanical_property.get('youngs-modulus', {}).get('value')
  if mechanical_property.get('specifies-the-plastic-elongation-strength'):
    record = mechanical_property['specifies-the-plastic-elongation-strength']['specifies-the-plastic-elongation-strength-record']
    rp = record.get('rp')
    strength = record.get('strength', {}).get('value')
  tensile_strength = mechanical_property.get('tensile-strength', {}).get('value')
  break_strength = mechanical_property.get('break-strength', {}).get('value')
  percentage_elongation_at_maximum_force = mechanical_property.get('percentage-elongation-at-maximum-force', {}).get('value')
  tensile_curve = mechanical_property.get('tensile-curve')['file']['name']

  download_url = 'http://matdata.shu.edu.cn' + mechanical_property.get('tensile-curve')['file']['url']

  # 获取文件名
  _, file = os.path.split(filename)
  print(file)
  # 创建 output/xxxx  文件夹  二进制文件存放于此
  files_dir = os.path.join('output/', file[0:-5])

  if not os.path.exists(files_dir):
      os.makedirs(files_dir)
  # 下载二进制文件
  r = requests.get(download_url).content
  with open(os.path.join(files_dir, tensile_curve), 'wb+') as f:
    f.write(r)

  data = {
              "meta": {
                  "数据 ID": "1",
                  "标题": "铝基复合材料 性能数据1",
                  "DOI": "",
                  "数据摘要": "铝基复合材料 性能数据1",
                  "关键词": "铝基复合材料 性能数据",
                  "来源": "MGE-SOURCE_HEADER v1 0100 10 #",
                  "引用": "",
                  "其他信息": "project: 2018YFB0704400；subject: 2018YFB0704401",
                  "数据生产机构": "SJTU",
                  "数据生产者": "SJTU",
                  "公开时间": "0",
                  "公开范围": "public"
              },
              "content": {
                  "力学性能": {
                      "测试样品编号": number_of_test_sample,
                      "测试样品含量": volume_ratio_of_reinforcement_in_test_sample,
                      "测试日期": test_date,
                      "测试人": tester,
                      "弹性模量": youngs_modulus,
                      "规定塑性延伸强度": [
                          {
                              "规定非比例延伸强度": rp,
                              "强度": strength,
                          },
                      ],
                      "抗拉强度": tensile_strength,
                      "断裂强度": break_strength,
                      "最大力总伸长率": percentage_elongation_at_maximum_force,
                      "拉伸曲线": [
                          os.path.join(file[0:-5], tensile_curve),
                      ]
                  }
              }
          }

  return data

def process(filenames):
  """
  return datas  包含多个数据的模板
  """
  # 处理多个数据
  datas = []
  for filename in filenames:
    data = convert(filename)
    datas.append(data)

  with open('性能数据.json', 'r') as f:
    file_template = json.load(f)
  file_template['data'] = datas
  save_to_json(file_template, 'output/final.json')
  return file_template


def save_to_json(obj, filename):
  with open(filename, 'w+') as f:
    json.dump(obj, f, ensure_ascii=False)


if __name__ == '__main__':
  file1 = 'LD10/F600+Mg-1.b2d886ac/LD10/F600+Mg-1.b2d886ac.json'
  file2 = 'LD10/F600+Mg-2.1ecea3ad/LD10/F600+Mg-2.1ecea3ad.json'
  filenames = [file1, file2]
  template = process(filenames)

