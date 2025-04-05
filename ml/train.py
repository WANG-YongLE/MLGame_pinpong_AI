import os
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
import joblib  # 用於保存模型


import os
import pickle

def find_pickle_files(directory):
    """ 遍歷資料夾（包含子資料夾），尋找所有 .pickle 檔案 """
    pickle_files = []
    for root, _, files in os.walk(directory):  # 遞迴搜尋所有子目錄
        for file in files:
            if file.endswith(".pkl"):
                pickle_files.append(os.path.join(root, file))  # 加入完整路徑
    return pickle_files

def load_pickle_files(file_paths):
    """ 讀取所有 .pickle 檔案並合併內容 """
    collected_data = []
    for file in file_paths:
        try:
            with open(file, "rb") as f:
                data = pickle.load(f)
                if isinstance(data, list):  # 確保 data 是列表
                    collected_data.extend(data)
                else:
                    print(f"警告: {file} 的數據格式不正確，未能合併。")
      #          print(f"成功讀取: {file}")  # 顯示讀取成功的檔案
        except Exception as e:
            print(f"無法讀取 {file}，錯誤: {e}")  # 顯示錯誤訊息
    return collected_data

# 設定要搜尋的資料夾
data_directory = "./data"

# 確保資料夾存在
if not os.path.exists(data_directory):
    print(f"錯誤: 資料夾 {data_directory} 不存在！")
else:
    # 找到所有 pickle 檔案
    pickle_files = find_pickle_files(data_directory)

    if not pickle_files:
        print("未找到任何 .pickle 檔案！")
    else:
        print(f"找到 {len(pickle_files)} 個 pickle 檔案。")

    # 讀取並合併 pickle 檔案內容
    data_list = load_pickle_files(pickle_files)



#print(data_list[:3]) 
# 確保至少有一個有效的數據
if not data_list:
    raise ValueError("沒有有效的數據可用")
#print(data_list)
# 轉換為 DataFrame
data = pd.DataFrame(data_list)
data.dropna(inplace=True)
if data.isnull().sum().sum() > 0:
    raise ValueError("仍有 NaN 存在，請檢查數據！")

# 假設最後一列是標籤
X = data.iloc[:, :-1].values  # 特徵
y = data.iloc[:, -1].values   # 標籤（分類或回歸數值）



# 切分訓練集與測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)

# 訓練 KNN 模型（k=5）
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)

# 儲存模型
joblib.dump(knn, "knn_model.pkl")
print("KNN 模型已存儲為 knn_model.pkl")


accuracy = knn.score(X_test, y_test)
print(f"KNN 模型的準確度: {accuracy:.4f}") 