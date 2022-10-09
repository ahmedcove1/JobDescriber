
import pandas as pd
from  rake_nltk import Rake 
import nltk
nltk.download("stopwords")
nltk.download('punkt')
dataframe_for_ml = pd.read_csv('RawData.csv')


r = Rake()
text = dataframe_for_ml['summary'][1]
r.extract_keywords_from_text(text)
phrase_df = pd.DataFrame(r.get_ranked_phrases_with_scores(),columns=['score','phrase'])
phrases = r.get_ranked_phrases()
print(phrase_df)