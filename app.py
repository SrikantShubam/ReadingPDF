from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2


import nltk
nltk.download('punkt')  # Required for word tokenization
nltk.download('stopwords')  # Required for stop words removal
nltk.download('wordnet') 
from nltk import word_tokenize
from nltk.corpus import wordnet
from word2number import w2n
# import string

import wordninja
app = Flask(__name__)
CORS(app)
import csv
conversation = []

def convert_numeric_words(text):
    tokens = word_tokenize(text)
    converted_tokens = []
    for token in tokens:
        if token.isdigit():
            converted_tokens.append(token)
        else:
            synsets = wordnet.synsets(token)
            if synsets:
                pos = synsets[0].pos()
                if pos == 'n' and token.lower() != 'and':
                    try:
                        number = word_to_number(token)
                        converted_tokens.append(str(number))
                    except ValueError:
                        converted_tokens.append(token)
                else:
                    converted_tokens.append(token)
            else:
                converted_tokens.append(token)
    converted_text = ' '.join(converted_tokens)
    return converted_text


def word_to_number(word):
    try:
        return w2n.word_to_num(word)
    except ValueError:
        return word

# Example usage
def replace_abbreviations(text, abbreviations_file):
    abbreviations = {}

    # Load abbreviations from file
    with open(abbreviations_file, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # Skip the header row
        for row in reader:
            abbreviation = row[0].strip()
            word = row[1].strip()
            abbreviations[word] = abbreviation

    # Replace words with abbreviations
    words = text.split()
    replaced_words = [abbreviations.get(word, word) for word in words]
    replaced_text = ' '.join(replaced_words)
    return replaced_text

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    # Check if the required NLTK resources are installed
    # nltk_resources = ['punkt', 'stopwords', 'wordnet']
    # missing_resources = []

    # for resource in nltk_resources:
    #     if not nltk.corpus.util.find_corpus(resource):
    #         missing_resources.append(resource)

    # if missing_resources:
    #     print(f"The following NLTK resources are missing: {', '.join(missing_resources)}")
    # else:
    #     nltk.download('punkt')  # Required for word tokenization
    #     nltk.download('stopwords')  # Required for stop words removal
    #     nltk.download('wordnet')  # Required for stemming
    from nltk.stem import SnowballStemmer
    from nltk.corpus import stopwords    
    if 'pdfFile' not in request.files:
        return 'No PDF file provided.', 400
    
    pdf_file = request.files['pdfFile']
    pdf_file.save('temp.pdf') 
    # Perform processing on the PDF file
    text=""
    with open('temp.pdf', 'rb') as pdfFileObj:
        # pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        for i in range(len(pdfReader.pages)):
            page = pdfReader.pages[i]
            # text=str(page.extra)
            # print(re.sub(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', ' ', page.extract_text()))
            # print(re.sub(r'(?<=\w)(?=[A-Z])|(?<=[a-z])(?=[A-Z])', ' ', page.extract_text()))
            words=wordninja.split( page.extract_text())
            text += ' '.join(words) + ' '
    # print("original"+"8"*40,text)        
           

    stop_words = stopwords.words('english')
    words = word_tokenize(text)
    filtered_words = [word for word in words if word not in stop_words]
    
    text = ' '.join(filtered_words)
    # print(text)
    # print("stop words removal"+"8"*40,text)        

    # print(filtered_words)
   
    porter = SnowballStemmer('english')
    # stemmer = SnowballStemmer('english')

    stemmed = [porter.stem(word) for word in filtered_words]
    # print(stemmed)
    joined_string = ' '.join(stemmed)
    # print(joined_string)
    # result = replace_abbreviations(joined_string, 'abbr.csv')
    # print(result)
    # print(joined_string)
    print("stemming"+"8"*40,joined_string)        
    text = replace_abbreviations(joined_string, 'abbr.csv')
    # print("abbr"+"8"*40,text)        

    text = convert_numeric_words(text)
    # print("numeric"+"8"*40,text) 
    # print(converted_text)
    # print(joined_string)
# Print the formatted text

            # print(page.extract_text())
            
       
  
# # creating a page object
#     pageObj = pdfReader.getPage(0)
#     # extracting text from page
#     print(pageObj.extractText())
    
#     # closing the pdf file object
#     pdfFileObj.close()
    # You can access the file using `pdf_file` object and perform operations like saving, parsing, or extracting text from it
  
    # Placeholder response
    conversation = [
          {'role': 'assistant', 'message': 'Hi there! How can I assist you?'},
            {'role': 'user', 'message': 'Hello!'}
          
        ]

    return {'conversation': conversation}
@app.route('/send-message', methods=['POST'])
def send_message():
    message = request.json['message']
    role = 'user'  # Set the role as desired

    # Perform any necessary processing or actions based on the message
    
    new_message = {'role': role, 'message': message}
    conversation.append(new_message)  # Add the new message to the conversation
    
    return jsonify({'conversation': conversation})
if __name__ == '__main__':
    app.run()
