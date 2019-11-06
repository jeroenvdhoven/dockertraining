def call_model(X, model):
    return model.predict(X)


def reverse_labels(labels, pipe):
    return pipe.inverse_transform(labels.reshape(-1, 1)).reshape(-1)
