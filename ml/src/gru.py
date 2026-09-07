import tensorflow as tf
def build(sequence_length,n_features):
    i=tf.keras.Input((sequence_length,n_features))
    x=tf.keras.layers.GRU(64)(i)
    x=tf.keras.layers.Dense(32,activation="relu")(x)
    o=tf.keras.layers.Dense(1,activation="sigmoid")(x)
    m=tf.keras.Model(i,o)
    m.compile("adam","binary_crossentropy",metrics=["accuracy",tf.keras.metrics.AUC(name="auc")])
    return m
