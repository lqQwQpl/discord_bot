from keras.models import load_model  # TensorFlow 是 Keras 運作所需的
from PIL import Image, ImageOps  # 請安裝 Pillow 取代 PIL
import numpy as np

"""
import tensorflow, keras
print(tensorflow.__version__,keras.__version__)
"""

# 禁用科學記號以提高清晰度
np.set_printoptions(suppress=True)

def load_tm_model(model_path, class_name_path):

    # 載入模型
    model = load_model(model_path, compile=False)

    # 載入標籤
    class_names = open(class_name_path, "r",encoding="utf-8").readlines()
    return model,class_names


def image_tm(model, class_names, img_path):
    # 創建具有正確形狀以輸入到 Keras 模型的陣列。
    # 陣列中可以放入的圖片數量由形狀元組的第一個位置決定，
    # 在這個例子中是 1。
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # 將此替換為您圖片的路徑。 
    image = Image.open(img_path).convert("RGB")

    # 將圖片調整大小至至少 224x224，然後從中心進行裁剪。
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # 將圖片轉換為 NumPy 陣列。
    image_array = np.asarray(image)

    # 對圖片進行正規化。
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # 將圖片載入至陣列中。
    data[0] = normalized_image_array
    # 對模型進行預測。
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    #print(prediction)
    confidence_score = prediction[0][index]
    # print("Class:", class_name[2:], end="")
#   print("Confidence Score:", confidence_score)

    return class_name, confidence_score


if __name__ == '__main__':
    model_path = r"C:\\Users\\User\\python\\discord_bot\\keras_model.h5"
    class_name_path = r"C:\\Users\\User\\python\\discord_bot\\labels.txt"
    image_path = r"C:\Users\User\python\discord_bot\AI_keras\date\\images.jpg"
    model, class_names = load_tm_model(model_path, class_name_path)
    prediction, score = image_tm(model, class_names, image_path)
    print(f"{prediction}, {score}")
