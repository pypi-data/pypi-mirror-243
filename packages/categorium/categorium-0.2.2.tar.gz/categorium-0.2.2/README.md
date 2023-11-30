# Introduction

This package enables the creation and training of language models for text classification using BERT, with prescribed parameters for smaller dataset training. It also comprises six pre-trained models with 27 categories each for experimentation, along with a feature for testing out language models.

# The models were trained in these languages, each with its corresponding validation accuracy:

   - English    | 92%
   - French     | 88%
   - German     | 92%
   - Italian    | 89%
   - Portuguese | 92%
   - Spanish    | 93%

# Each model comprises 27 categories, including:
Adult | Animals | Autos | Beauty |Business | Electronics | Entertainment | Finance | Food | Games | Health | Hobbies | Home | Jobs | Law | Literature | News | Online Communities | Real Estate | Reference | Science | Sensitive Subjects | Shopping | Society | Sports | Telecom | Travel


# Where to get it
```bash
pip install categorium
```

# Functions

## The package defines the following functions:

   - select_csv_file(language): This function loads the category names and order from CSV files.
   - select_language_model(language): This function loads the pre-trained language models.
   - select_token(language): This function loads the tokenizer to be used.
   - test_models(model_trained,tokenize,csv_cat,text): This function tests the trained models.
   - train_main(): This function tokenizes the text data using the BERT tokenizer.

# Usage

## Guide to use the functions

To utilize pre-trained models, import the function select_language_model() and specify the language in its parameters. For instance, select_language_model('english') will load the English language model. If you enter a language that doesn't contain a trained model for it, then a message will be displayed indicating that there is no trained model for that language. This principle applies to both select_csv_file() and select_token() functions.

## Guide to use the test models function

To test the models' functionality, import the test_models() function using these parameters: (model_trained, tokenize, csv_cat, text). "Model_trained" refers to the model that has been trained. "Tokenize" refers to the created tokenizer. "Csv_cat" refers to the file with the categories' names and their order. Lastly, the "text" parameter refers to the text which needs to be categorised.

## Example of using a pre-trained model
```bash
from categorium import select_language_model, select_csv_file, select_token

# Load the labels name
df = pd.read_csv(select_csv_file('english'), index_col=False)
# Load the pre-trained model
model = TFBertForSequenceClassification.from_pretrained(select_language_model('english'))
#Load the tokenizer
tokenizer = BertTokenizer.from_pretrained(select_token('english'))

# Text to classify
text = "Insert example text"

# Tokenize the text and get the model's prediction
inputs = tokenizer(text, return_tensors='tf')
outputs = model(inputs)[0]

# Get the predicted category index
predicted_index = tf.argmax(outputs, axis=1).numpy()[0]

# Get the predicted category label
predicted_label = df['cat'].unique()[predicted_index]

# Print the predicted category label
print(predicted_label)
```

## Example of using the package function to test the models
```bash
from categorium import select_language_model, select_csv_file, select_token,test_model_utils

# Load the labels name
df = pd.read_csv(select_csv_file('english'), index_col=False)
# Load the pre-trained model
model = TFBertForSequenceClassification.from_pretrained(select_language_model('english'))
#Load the tokenizer
tokenizer = BertTokenizer.from_pretrained(select_token('english'))

test_models(model,tokenizer,df,text):
```

## The following dependencies must be installed to use the training feature:

   - TensorFlow
   - Transformers
   - Pandas
   - NumPy

## Guide to use the training feature

To use the train the model function, create a folder named 'category' in the directory of the script that calls the train_main() function. In this folder, place xlsx format files that contain text in the first column and the respective category in the second column. Once the initial step has been completed, run the script to start training the models and generate a folder named training_files in the same directory as the train_main() function. This folder comprises all the ultimate files for the trained model.