from simpletransformers.classification import ClassificationModel, ClassificationArgs
import time


# 預測情緒
def predict(listTestData):
    # 輸出模型存在的目錄名稱
    dir_name = 'bert-base-chinese-bs-64-epo-3/checkpoint-20000' 

    # 自訂參數
    model_args = ClassificationArgs()
    model_args.train_batch_size = 64
    model_args.num_train_epochs = 3

    # 讀取 ClassificationModel
    model = ClassificationModel(
        'bert', 
        f"outputs/{dir_name}", # 這裡要改成訓練完成的模型資料夾路徑
        use_cuda=True, 
        cuda_device=0, 
        num_labels=6, 
        args=model_args
    )

    # 預測
    predictions, raw_outputs = model.predict(listTestData)

    # 回傳預測結果，會是一個 list
    return predictions


# 主程式
if __name__ == "__main__":
    # 計時開始
    tStart = time.time()

    # 準備預測情緒類別。語料可以不只一句！
    listTestData = [
        "現在刷朋友圈最大的快樂就是看代購們各種直播 。 。 。 。 。", 
        "你幹了什麼", 
        "不愁吃,不愁穿,不愁住,不愁行,還愁啥呢?",
        "今天考試考了100分，好開心"
    ]

    # 進行預測
    print( predict(listTestData) )

    # 計時結束
    tEnd = time.time()

    # 輸出程式執行的時間
    print(f"執行花費 {tEnd - tStart} 秒。")