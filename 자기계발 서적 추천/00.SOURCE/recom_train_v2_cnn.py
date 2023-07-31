import tensorflow as tf
import numpy as np
from book.book_recom_data import make_train_set

# 훈련 데이터 불러오기
x_train, y_train = make_train_set()

# 학습 데이터 전처리
# 여기서는 예시로 학습 데이터가 이미 숫자로 변환된 상태로 가정합니다.
# 만약 숫자로 변환되지 않은 문자열 데이터라면 적절한 전처리 과정을 수행해야 합니다.

# CNN에 맞게 입력 데이터 형태 변경
x_train = x_train.reshape((-1, 5, 1))

# CNN 모델 생성
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv1D(64, 2, activation='relu', input_shape=(5, 1)),
    tf.keras.layers.MaxPooling1D(2),
    tf.keras.layers.Conv1D(128, 2, activation='relu'),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(120, activation='softmax')
])

# 모델 컴파일
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 모델 훈련
model.fit(x_train, y_train, epochs=400)
# model.save("book_recom.h5")

# 예측 수행
predict = model.predict(x_train)

print(np.argmax(predict[1]))
print(np.argmin(predict[0]))
