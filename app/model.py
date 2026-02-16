import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Conv1D, MaxPooling1D
from tensorflow.keras.layers import Embedding, GlobalMaxPooling1D
from tensorflow.keras.layers import Input, Dropout


def create_dcnn_model(vocab_size, max_length, num_classes):

    input_layer = Input(shape=(max_length,))

    x = Embedding(vocab_size, 128)(input_layer)

    x = Conv1D(128, 5, activation='relu')(x)
    x = MaxPooling1D(2)(x)

    x = Conv1D(128, 5, activation='relu')(x)
    x = GlobalMaxPooling1D()(x)

    x = Dense(64, activation='relu')(x)
    x = Dropout(0.5)(x)

    output = Dense(num_classes, activation='sigmoid')(x)

    model = Model(inputs=input_layer, outputs=output)

    model.compile(
        loss='binary_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )

    return model
