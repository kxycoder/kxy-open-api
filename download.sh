#!/bin/bash  
  
# 指定目标文件夹  
target_folder="./code"  
uiPath="/myspace/source/workspace/yudao-python/kxy-open-ui"
uiSrc="$target_folder"/vue3/src
backSrc="$target_folder"/python/app
apiPath=$(pwd)

# 获取URL参数  
url="$1"
model="$2"

  
# 检查URL参数是否为空  
if [ -z "$url" ]; then  
  echo "请提供URL参数！"  
  exit 1  
fi

if [ -z "$model" ]; then  
  model="all"
fi 
# 解压code.tar到code文件夹  
mkdir -p $target_folder

# 下载文件并保存为code.tar  
wget -O "$target_folder"/code.tar "$url"  
  
# 检查是否下载成功  
if [ $? -eq 0 ]; then  
  echo "文件下载成功！"  
else  
  echo "文件下载失败！"  
  exit 1  
fi  
  


tar -xvf "$target_folder"/code.tar -C "$target_folder"
# 检查解压是否成功  
if [ $? -eq 0 ]; then  
  echo "解压成功！"  
else  
  echo "解压失败！"  
  exit 1  
fi

if [ $model = "ui" ]; then  
  echo "只替换前端"
  cp -r "$uiSrc" "$uiPath"
  rm -rf "$target_folder"
  exit 0
fi

if [ $model = "back" ]; then  
  echo "只替换后端"
  # apiPath
  cp -r "$backSrc" "$apiPath/"
  rm -rf "$target_folder"
  exit 0
fi

echo "全部替换"
cp -r "$uiSrc" "$uiPath"
cp -r "$target_folder"/python/app "$apiPath/"
# cp -r "$target_folder"/python/dal "$apiPath/"
# cp -r "$target_folder"/python/models "$apiPath/"
# cp -r "$target_folder"/python/utils "$apiPath/"
cp -r "$target_folder/sql" "$apiPath/sql/"
rm -rf "$target_folder"
echo "全部替换成功"