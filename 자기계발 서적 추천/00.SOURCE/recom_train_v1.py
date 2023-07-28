import tensorflow as tf
import numpy as np
from book.book_recom_data import make_train_set



x_train, y_train = make_train_set()

# 라벨로 사용할 책번호의 가장 큰값 
label_num = y_train[np.argmax(y_train)] + 1

# 3. 모델 구성
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(5,)),
    tf.keras.layers.Dense(512, activation=tf.nn.relu),
    tf.keras.layers.Dense(512, activation=tf.nn.relu),
    tf.keras.layers.Dense(512, activation=tf.nn.relu),
    tf.keras.layers.Dense(512, activation=tf.nn.relu),
    tf.keras.layers.Dense(512, activation=tf.nn.relu),
    tf.keras.layers.Dense(512, activation=tf.nn.relu),
    tf.keras.layers.Dense(label_num, activation=tf.nn.softmax)
])

# 4. 모델 컴파일
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 5. 모델 훈련
model.summary()
model.fit(x_train, y_train, epochs=300)
# model.save("book_recom.h5")


predict = model.predict(x_train)

print(np.argmax(predict[1]))
print(np.argmin(predict[0]))
# print(predict)
# print(x_train)
# print(y_train)


