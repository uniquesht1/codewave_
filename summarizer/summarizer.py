import pandas as pd
from transformers import pipeline
from collections import Counter
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


# text = """In a world often dominated by negativity, it's important to remember the power of kindness and compassion. Small acts of kindness have the ability to brighten someone's day, uplift spirits, and create a ripple effect of positivity that can spread far and wide. Whether it's a smile to a stranger, a helping hand to a friend in need, or a thoughtful gesture to a colleague, every act of kindness has the potential to make a difference in someone's life.Beyond individual actions, there is also immense power in collective efforts to create positive change. When communities come together to support one another, incredible things can happen. From grassroots initiatives to global movements, people are uniting to tackle pressing social and environmental issues, driving meaningful progress and inspiring hope for a better future.It's also important to recognize the strength that lies within each and every one of us. We all have the ability to make a positive impact, no matter how small our actions may seem. By tapping into our innate compassion and empathy, we can cultivate a culture of kindness and empathy that enriches our lives and those around us.So let's embrace the power of kindness, and strive to make the world a better place one small act at a time. Together, we can create a brighter, more compassionate future for all."""

# nlp = spacy.load('en_core_web_sm')
# doc = nlp(text)
# tokens = [token.text.lower() for token in doc 
#           if not token.is_stop and 
#           not token.is_punct and 
#           token.text !='\n']

# word_freq = Counter(tokens)
# max_freq = max(word_freq.values())
# for word in word_freq.keys():
#     word_freq[word] = word_freq[word]/max_freq
    
# sent_token = [sent.text for sent in doc.sents]

# sent_score = {}
# for sent in sent_token:
#     for word in sent.split():
#         if word.lower() in word_freq.keys():
#             if sent not in sent_score.keys():
#                 sent_score[sent] = word_freq[word]
#             else:
#                 sent_score[sent] +=word_freq[word]
#         print(word)

# pd.DataFrame(list(sent_score.items()),columns=['Sentence','Score'])

# num_sentences =3
# n = nlargest(num_sentences,sent_score,key=sent_score.get)
# " ".join(n)


summarizer=pipeline("summarization",model='t5-base',tokenizer='t5-base',framework='pt')
text = """In a world often dominated by negativity, it's important to remember the power of kindness and compassion. Small acts of kindness have the ability to brighten someone's day, uplift spirits, and create a ripple effect of positivity that can spread far and wide. Whether it's a smile to a stranger, a helping hand to a friend in need, or a thoughtful gesture to a colleague, every act of kindness has the potential to make a difference in someone's life.Beyond individual actions, there is also immense power in collective efforts to create positive change. When communities come together to support one another, incredible things can happen. From grassroots initiatives to global movements, people are uniting to tackle pressing social and environmental issues, driving meaningful progress and inspiring hope for a better future.It's also important to recognize the strength that lies within each and every one of us. We all have the ability to make a positive impact, no matter how small our actions may seem. By tapping into our innate compassion and empathy, we can cultivate a culture of kindness and empathy that enriches our lives and those around us.So let's embrace the power of kindness, and strive to make the world a better place one small act at a time. Together, we can create a brighter, more compassionate future for all."""
summary = summarizer(text,max_length=100,min_length=10,do_sample=False)


# Initialize the summarizer pipeline
summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="pt")

def summarize_text(text):
    # Summarize the text
    summary = summarizer(text, max_length=1000, min_length=10, do_sample=False)
    return summary[0]['summary_text']

# Get user input from the terminal
text = input("Enter the text to summarize: ")

# Summarize and display the result
summary = summarize_text(text)
print("\nSummary:\n", summary)


