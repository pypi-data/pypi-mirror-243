from transformers import TFBertForSequenceClassification, BertTokenizer
import tensorflow as tf
import pandas as pd

def test_models(model_trained,tokenize,csv_cat,text):
    # Carrega o modelo e o tokenizer
    df = pd.read_csv(csv_cat, index_col=False)
    # Carrega o modelo e o tokenizer
    model = TFBertForSequenceClassification.from_pretrained(model_trained)
    tokenizer = BertTokenizer.from_pretrained(tokenize)

    # Tokenize the text and get the model's prediction
    inputs = tokenizer(text, return_tensors='tf')
    outputs = model(inputs)[0]

    # Get the predicted category index
    predicted_index = tf.argmax(outputs, axis=1).numpy()[0]

    # Get the predicted category label
    predicted_label = df['cat'].unique()[predicted_index]

    # Print the predicted category label
    print(predicted_label)