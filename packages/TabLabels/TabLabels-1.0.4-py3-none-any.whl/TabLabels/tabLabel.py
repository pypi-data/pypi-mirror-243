import re
import os
import json

def is_valid_path(path):
    # Sử dụng os.path.exists để kiểm tra xem đường dẫn tồn tại hay không
    return os.path.exists(path)

def phase_2(qq):
  lst_kq = []
  z = qq.split(">")
  z = list(map(lambda x: x+">", z))[:-1]
  for i in z:
    if "</td>" in i and "</td>" != i:
      z = i.split("</td>")
      z[-1] = "</td>"
      for j in z:
        lst_kq.append(j)
    else:
      lst_kq.append(i)
  e = []
  for i in range(len(lst_kq)-1):
    if lst_kq[i] == "<td>" and lst_kq[i+1] == "</td>":
      e.append(lst_kq[i])
      e.append(" ")
    else:
      e.append(lst_kq[i])
  return e

def LoaiPhanThua(s):
  s = s.replace("<b>" , "")
  k = ["</sup>", "<sup>", "<b> ", "</b>", '<tbody>', '</tbody>', '</i>', "<i>","</body>", "<body>"
  , "</html>", "<html>", "</sub>", "<sub>"]
  # Loại bỏ các chuỗi từ danh sách k khỏi chuỗi z
  for item in k:
      s = s.replace(item, "")
  return s

def KiTuHTML_Special_Limited(e):
  m = []
  for i in range(len(e)):
    if e[i] != e[i].split(" ")[0] and e[i] != " ":
      if e[i].startswith("<") and e[i].endswith(">"):
        text = e[i]
        z = e[i].split("d")
        z = [z[1].split(">")[0]]
        z.append(">")
        split_text = text.split(" ")
        result = []
        for idx, item in enumerate(split_text):
            result.append(item)
            if idx < len(split_text) - 1:
                result.append(" ")
        v = result[0:1] + z
        for j in v:
              m.append(j)
        continue
      m.append(e[i])
    else:
      if  e[i] != "<table>" and e[i] != "</table>":
        m.append(e[i])

  return m

def main(file_path, output_file_path = "data/outputZ.txt"):
    if file_path == "None":
        print("~~~~")
        return
    elif is_valid_path(file_path):
        print(f"'{file_path}' là một đường dẫn hợp lệ.")
    else:
        print(f"'{file_path}' không phải là một đường dẫn hợp lệ.")
        return
    
    # Đọc nội dung từ tệp đầu vào
    with open(file_path, "r", encoding="utf-8") as input_file:
        contents = input_file.read()
    
    lines = re.split(r'\n', contents)
    mph = []
    
    # In các dòng kết quả
    for line in lines:
        mph.append(line)
    
    new_mph = []
    
    for i in mph:
        new_mph.append((re.split(r'\t', i)))
    
    # Tạo và mở tệp đầu ra cho việc ghi
    # Mở file trong chế độ ghi mới (xóa nội dung cũ) và thiết lập indent cho đoạn JSON ghi vào là 2 để thụ động dấu xuống dòng.
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        for i in new_mph:
            # GT
            content = i[1]
            img = i[0]
            phan_du = LoaiPhanThua(i[1])
            mph = KiTuHTML_Special_Limited(phase_2(phan_du))
            html_list = [item for item in mph if item.endswith(">") or item.endswith('"') or item.endswith("td")]
            list_Cell = [item for item in mph if item not in html_list]

            # Structure
            cell1 = [x for x in html_list]
            cell1 = [x.replace('\\"', '"') if '\\"' in x else x for x in cell1]

            # Cells
            Cells = []
            for i in list_Cell:
                cell = {"tokens": [x for x in i], "bbox": [[[0, 0], [0, 0]]]}
                Cells.append(cell)

            cell2 = Cells

            cell3 = "<html><body>" + content + "</body></html>"

            data = {
                "structure" : {"tokens": cell1},
                "cells": cell2
            }
            tonken = {"filename": img , 'html': data, 'gt':cell3}
            json.dump(tonken, output_file, ensure_ascii= False)
            output_file.write("\n")  # Thêm dấu xuống dòng sau mỗi lần ghi.

#def Main():
#  if __name__ == "__main__":
#    main(input("Tên file:... "), "data/outputZ.txt")
#    print("file has been save")

