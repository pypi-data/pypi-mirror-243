import os
import pandas as pd
import re
import contractions
from pathlib import Path
from tokenizers  import BertWordPieceTokenizer
from transformers import BertTokenizer,BertConfig, TFBertForSequenceClassification,AdamWeightDecay
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.metrics import SparseCategoricalAccuracy
from tensorflow.keras.callbacks import EarlyStopping
import numpy as np

def readictionary():
    # Gets the current working directory where your script is located
    current_directory = os.path.abspath(os.getcwd())

    # Constructs the full path to the "categorie"
    categories_folder = os.path.abspath(os.path.join(current_directory, 'categorie'))

    # List of categorys and arquives
    categories = {}

    # Listar os arquivos na pasta
    arquives = os.listdir(categories_folder)

    # Iterate trough the arquives
    for arquive in arquives:
        # Extract the category name from the file name (without the .xlsx extension)
        category = os.path.splitext(arquive)[0]
        # Build the full file path
        arquive_path = os.path.join(categories_folder, arquive)
        # add the category and path of the file to the dictionary
        categories[category] = arquive_path

    return categories

#----------------------------Function to process the text data--------------------------------
def process_text_data(categories):
    print('Phase 1 start')
    # Create an empty list to store the text data
    text_data = []

    # Process text data for each category
    for category, filepath in categories.items():
        df = pd.read_excel(filepath, index_col=False, engine='openpyxl')
        # Convert float values to string
        df['texto'] = df['texto'].astype(str)
        # Remove duplicates from the dataframe
        df = df.drop_duplicates()

        # Perform pre-tokenization tasks on each element of the 'texto' column
        for text in df['texto']:
            # Convert the text to lowercase
            text = text.lower()

            # Expand contractions
            text = contractions.fix(text)

            # Replace numbers with 'NUM'
            text = re.sub(r'\d+', 'NUM', text)

            # Replace URLs, emails, and phone numbers with special tokens
            text = re.sub(r'\b(?:https?://|www\.)\S+\b', 'URL', text)
            text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 'EMAIL', text)
            text = re.sub(r'\b[0-9\+\-\(\)]{9,}\b', 'PHONE', text)

            # Remove HTML tags
            text = re.sub('<[^<]+?>', '', text)

            # Remove punctuation
            text = re.sub(r'[^\w\s]', '', text)

            # Add the processed text to the text_data list
            text_data.append(text)

    # Join all the text data into a single string
    all_text = '\n'.join(text_data)

    # Write the all_text string to a file
    #with open('vocab-builder-test.txt', 'w', encoding='utf-8-sig') as f:
        #f.write(all_text)
    print('Phase 1 complete')

    return all_text
    
    


#----------------------Function that creates the tokenizer--------------------------------
def create_tokenizer(all_text):
    print('Phase 2 start')
    def create_tokenizer_savepath():
        savepath = Path("./training_files")
        if not savepath.exists():
            savepath.mkdir()
        return str(savepath)

    # Initialize a tokenizer with a maximum vocabulary size of 30,000 tokens
    tokenizer = BertWordPieceTokenizer(
        clean_text=True,
        handle_chinese_chars=True,
        strip_accents=True,
        lowercase=True,
        wordpieces_prefix="##",
        unk_token="[UNK]",
        sep_token="[SEP]",
        cls_token="[CLS]",
        pad_token="[PAD]",
        mask_token="[MASK]"
    )

    # Train the tokenizer on the corpus
    tokenizer.train_from_iterator(
        [all_text],
        vocab_size=30500,
        min_frequency=2,
        special_tokens=[
            "[PAD]",
            "[UNK]",
            "[CLS]",
            "[SEP]",
            "[MASK]",
            "[NUM]",
            "[URL]",
            "[EMAIL]",
            "[PHONE]"
        ],
    )

    # Save the tokenizer to disk
    savepath = create_tokenizer_savepath()
    tokenizer.save_model(str(savepath),"bert-token-uncased")
    print("Tokenizer saved.")
    print('Phase 2 complete')
    

#--------------------------Function to tokenize data-----------------------------------------
def tokenize_data(categories):
    print('Phase 3 start')
    def preprocess_text(text):
        # Lowercase the text
        text = text.lower()

        # Expand contractions
        text = contractions.fix(text)

        # Replace numbers with 'NUM'
        text = re.sub(r'\d+', 'NUM', text)

        # Replace URLs, emails, and phone numbers with special tokens
        text = re.sub(r'\b(?:https?://|www\.)\S+\b', 'URL', text)
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 'EMAIL', text)
        text = re.sub(r'\b[0-9\+\-\(\)]{9,}\b', 'PHONE', text)

        # Remove HTML tags
        text = re.sub('<[^<]+?>', '', text)

        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)

        return text

    # Load data
    dfs = {}
    for category_name, category_path in categories.items():
        df = pd.read_excel(category_path, index_col=False,engine='openpyxl')
        df['texto'] = df['texto'].astype(str)

        df['cat'] = category_name
        df.dropna(subset=['texto'], inplace=True)
        dfs[category_name] = df

    # Concatenate all the preprocessed dataframes
    df = pd.concat(list(dfs.values()), ignore_index=True)
    df = df.drop_duplicates()
    #colocar as linhas do csv random
    df = df.sample(frac=1).reset_index(drop=True)
    print(df)

    # Get the unique categories in the order they first appear
    unique_categories = df['cat'].drop_duplicates(keep='first')

    # Filter the dataframe to include only the unique categories in the original order
    df_filtered = df[df['cat'].isin(unique_categories)]

    # Remove the duplicates from the 'cat' column
    df_filtered = df_filtered.drop_duplicates(subset='cat')

    # Remove the 'texto' column from the filtered dataframe
    df_filtered = df_filtered.drop('texto', axis=1)

    # Save the filtered dataframe to the encoder data file
    df_filtered.to_excel('training_files/categories_order.xlsx', index=False, encoding='utf-8', engine='xlsxwriter')

    print(df_filtered)

    df.to_excel('temp_folder/encoder_data.xlsx',index=False, encoding='utf-8', engine='xlsxwriter')

    #text_data = preprocess_text(categories)
    text_data = [preprocess_text(text) for text in df['texto']]
    #Load the tokenizer
    tokenizer = BertTokenizer.from_pretrained('training_files/bert-token-uncased-vocab.txt',do_lower_case=True)
    input_ids = []
    attention_masks = []

    # Tokenize texts with dynamic padding
    encoded_dict = tokenizer.batch_encode_plus(
        text_data,
        #df['texto'].tolist(),
        add_special_tokens=True,
        max_length=100,#default é 100
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        return_tensors='tf'
    )
    input_ids = encoded_dict['input_ids']
    attention_masks = encoded_dict['attention_mask']

    input_ids_np = input_ids.numpy()
    attention_masks_np = attention_masks.numpy()

    # Save arrays to file
    np.save('temp_folder/input_ids.npy', input_ids_np)
    np.save('temp_folder/attention_masks.npy', attention_masks_np)

    print('Fase 3 completed')
    return input_ids, attention_masks


#----------------------------Function to train the model--------------------------------
def model_train(input_ids, attention_masks):
    print('Phase 4 start')
    # Carregar os dados
    df = pd.read_excel('temp_folder/encoder_data.xlsx', index_col=False, engine='openpyxl')
    print(df['cat'])
    # Converter os arrays de volta para tensors
    input_ids = input_ids
    attention_masks = attention_masks

    # Encode labels
    label_encoder = LabelEncoder()
    df['cat'] = label_encoder.fit_transform(df['cat'])
    labels = tf.constant(df['cat'])

    # Criar um novo modelo Bert
    num_labels = len(df['cat'].unique()) #2,2,64,32,0.4
    config = BertConfig(num_hidden_layers=2, num_attention_heads=2, intermediate_size=64,
                        hidden_size=32, num_labels=num_labels, hidden_dropout_prob=0.4)
    model = TFBertForSequenceClassification(config)

    early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    #val_accuracy

    # Fine-tune the BERT model
    optimizer = AdamWeightDecay(learning_rate=1e-4, weight_decay_rate=0.01)
    loss = SparseCategoricalCrossentropy(from_logits=True)
    metric = SparseCategoricalAccuracy('accuracy')
    model.compile(optimizer=optimizer, loss=loss, metrics=[metric])
    history = model.fit(
        [input_ids, attention_masks],
        labels,
        validation_split=0.2,
        epochs=40,
        batch_size=16,#16
        callbacks=[early_stop]
    )

    # Avaliar o modelo
    test_input_ids = input_ids[-400:]
    test_attention_masks = attention_masks[-400:]
    test_labels = labels[-400:]
    test_loss, test_accuracy = model.evaluate(
        [test_input_ids, test_attention_masks],
        test_labels,
        batch_size=32
    )

    print('Test Loss:', test_loss)
    print('Test Accuracy:', test_accuracy)

    model.save_pretrained('training_files/final_model')
    print("model_trainned")


def create_directory():
    try:
        # Check if the directory exists
        if not os.path.exists("./temp_folder"):
            # If it doesn't exist, create the directory
            os.makedirs("./temp_folder")
            print("Directory 'temp_folder' created successfully.")
        else:
            print("Directory 'temp_folder' already exists.")
            
    except Exception as e:
        print(f"Error while creating directory: 'temp_folder' - {e}")


def delete_directory():
    try:
        # List all files and directories in the given path
        items = os.listdir("./temp_folder")

        for item in items:
            item_path = os.path.join("./temp_folder", item)

            # If it's a file, delete it
            if os.path.isfile(item_path):
                os.remove(item_path)

            # If it's a directory, recursively call the function to delete its contents
            elif os.path.isdir(item_path):
                delete_directory(item_path)

        # Finally, remove the empty directory
        os.rmdir("./temp_folder")

    except Exception as e:
        print(f"Error while deleting directory: 'temp' - {e}")

def train_main():

    create_directory()
    # Call the function to get the dictionary of categories
    categories = readictionary()
    
    # Checkpoint system WITH temp file
    if not os.path.exists('training_files/bert-token-uncased-vocab.txt'):
        text_processed = process_text_data(categories) # Process and write the text data to the file
        create_tokenizer(text_processed)

    if not os.path.exists('temp_folder/input_ids.npy'):
        input_ids, attention_masks = tokenize_data(categories)
    else:
        input_ids_np = np.load('temp_folder/input_ids.npy')
        attention_masks_np = np.load('temp_folder/attention_masks.npy')
        input_ids = tf.convert_to_tensor(input_ids_np)
        attention_masks = tf.convert_to_tensor(attention_masks_np)

    model_train(input_ids, attention_masks)

    #Delete checkpoint files
    delete_directory()

if __name__ == "__main__":
    # Call the main function when the script is run directly
    train_main()