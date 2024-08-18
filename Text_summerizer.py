import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from rank_bm25 import BM25Okapi
from rouge_score import rouge_scorer
 
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Function to summarize a single text file
def summarize_text_file(file_path):
    # Initialize stop words(is,I,had,etc for english) and lemmatizer(finding lemma of words)
    stop_words = set(stopwords.words('english')) 
    lemmatizer = WordNetLemmatizer()

    # Read the .txt file
    with open(file_path, 'r') as file:
        text = file.read()

    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Process sentences
    clean_sentences = []
    tokenized_sentences = []
    for sentence in sentences:
        tokens = word_tokenize(sentence)
        tokens = [token for token in tokens if token.isalnum()]  # Remove punctuation
        tokens = [token for token in tokens if token not in stop_words]
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
        clean_sentences.append(' '.join(tokens))
        tokenized_sentences.append(tokens)

    # Initialize BM25 with tokenized sentences
    bm25 = BM25Okapi(tokenized_sentences) #using okapi for ranking function

    # Calculate BM25 scores for each original sentence
    scores = []
    for sentence in tokenized_sentences:
        score = bm25.get_scores(sentence)
        scores.append(score.mean())  # Take the average score of the words in the sentence

    # Rank the sentences based on their BM25 scores
    ranked_sentences = sorted(zip(sentences, scores), key=lambda x: x[1], reverse=True)

    # Select the top-ranked sentences for the summary
    summary_sentences = [sentence for sentence, score in ranked_sentences[:5]]

    # Calculate the ROUGE score for the summary(unigram,bigram,lcs)
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL', 'rougeLsum'])
    score = scorer.score(' '.join(summary_sentences), text)

    # Return the summary and ROUGE score
    return {
        'summary': ' '.join(summary_sentences),
        'rouge_score': score
    }

# File path of the text file to summarize
file_path = r"C:\Users\LENOVO\OneDrive\Desktop\TEXT_SUMMERIZATION\archive\BBC News Summary\News Articles\business\001.txt"

# Summarize the given text file functioncall
result = summarize_text_file(file_path)

# Print the summary and ROUGE score
print("Summary:")
print(result['summary'])
print(f"ROUGE score: {result['rouge_score']}")
print()
