
import pandas as pd

all_data = pd.read_csv('dataFinal.csv',sep=',',header='infer')
all_data = all_data.dropna()
keywords_lower = ['python','sql','r', 'tableau', 'power bi','azure','google cloud','databricks','git','aws','nosql','spark','docker','gcp','looker','etl','snowflake','redshift','excel','sas','javascript']
for keyword in keywords_lower:
    all_data[keyword] = all_data['summary'].str.lower().str.contains(keyword).astype(int)

print(all_data)

all_text = all_data['summary'].str.cat(sep=' ')
word_counts = pd.Series(all_text.split()).value_counts()

import nltk
from nltk.corpus import stopwords
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
    
nltk.download('stopwords')
cachedStopWords = stopwords.words("french")

for stop_word in cachedStopWords:
    word_counts = word_counts.drop(stop_word, errors='ignore')

word_counts.to_csv('output/word_counts.csv', index=True)


import pandas as pd
import spacy

languages = pd.read_csv('./data/languages.csv')
platforms = pd.read_csv('./data/platforms.csv')
databases = pd.read_csv('./data/databases.csv')
frameworks_tools = pd.read_csv('./data/frameworks_tools_etc.csv')

patterns = []
for x in languages.name.tolist():
    patterns.append({"label": "PROG_LANG", "pattern": [{"lower": w.lower()} for w in str(x).split()],"id": "SKILLS"})

for x in databases.name.tolist():
    patterns.append({"label": "DB","pattern": [{"lower": w.lower()} for w in str(x).split()], "id": "SKILLS"})

for x in platforms.name.tolist():
    patterns.append({"label": "PLATFORM", "pattern": [{"lower": w.lower()} for w in str(x).split()], "id": "SKILLS"})

for x in frameworks_tools.name.tolist():
    patterns.append({"label": "FRAMEWORKS", "pattern": [{"lower": w.lower()} for w in str(x).split()], "id": "SKILLS"})

nlp = spacy.load("fr_core_news_sm")
ruler = nlp.add_pipe("entity_ruler", before="ner")
ruler.add_patterns(patterns)
ruler.to_disk("./output/patterns.jsonl")

doc = nlp(all_text)
ents = [{'label': entity.label_, 'text': entity.text} for entity in doc.ents if entity.ent_id_ == 'SKILLS']
print(ents)


def extract_tech(description):
    doc = nlp(description)
    frameworks, databases, platforms, prog_langs = [], [], [], []

    for entity in doc.ents:
        if entity.ent_id_ == 'SKILLS':
            if entity.label_ == 'PROG_LANG' and entity.text not in prog_langs:
                prog_langs.append(entity.text)
            if entity.label_ == 'PLATFORM' and entity.text not in platforms:
                platforms.append(entity.text)
            if entity.label_ == 'DB' and entity.text not in databases:
                databases.append(entity.text)
            if entity.label_ == 'FRAMEWORKS' and entity.text not in frameworks:
                frameworks.append(entity.text)

    #prog_langs = " ".join(prog_langs)
    #platforms = " ".join(platforms)
    #databases = " ".join(databases)
    #frameworks = " ".join(frameworks)
    data = (prog_langs, platforms, databases, frameworks)
    data = tuple([x for x in data if x])
    if data:
        return data 
    else:
        return None

all_data['keywords'] = all_data['summary'].apply(extract_tech)
teste = all_data[['keywords']].explode("keywords").reset_index(drop=True)
teste = teste[teste["keywords"].notna()]
teste["keywords"] = teste["keywords"].apply(lambda x: ",".join(x))
exploded_df = teste.assign(keywords=teste["keywords"].str.split(",")).explode("keywords").reset_index(drop=True)
print(exploded_df)
a=exploded_df
exploded_df = exploded_df[exploded_df["keywords"] != "Access"]
exploded_df["keywords"].value_counts().head(10).values/len(all_data)

counts = pd.DataFrame(a["keywords"].value_counts())
print(counts.columns)
counts['pct'] = counts['count']/len(all_data)
counts.head(10)
counts = counts.head(10).iloc[::-1]


import plotly.express as px

#exploded_df[,]
#px.bar(counts.head(10), x=counts.head(10).index, y=counts.head(10).values, labels={"x": "Industry", "y": "Count"})
fig = px.bar(counts.head(10), x='pct', y=counts.head(10).index,text=counts.head(10)['pct'].apply(lambda x: f'{x:,.2%}'), orientation='h')

# Customize the layout
fig.update_layout(
    title='Keyword Distribution in Job Ads',
    xaxis_title='Percentage',
    yaxis_title='Keywords',
    margin=dict(l=100, r=20, t=70, b=70),
    xaxis_tickformat=".2%",
    width=700
)
fig.update_traces(hovertemplate='%{x:,.2%}')
# Show the plot
fig.show()

counts.reset_index().to_csv("counts.csv",index=False)

counts2 = pd.read_csv("counts.csv")
counts2.rename(columns={'Unnamed: 0':'skill'})
ig = px.bar(counts2.head(10), x='pct', y=counts2.index,text=counts2['pct'].apply(lambda x: f'{x:,.2%}'), orientation='h')

# Customize the layout
fig.update_layout(
    title='Keyword Distribution in Job Ads',
    xaxis_title='Percstreamlit run appentage',
    yaxis_title='Keywords',
    margin=dict(l=100, r=20, t=70, b=70),
    xaxis_tickformat=".2%",
    width=700
)
fig.update_traces(hovertemplate='%{x:,.2%}')
fig.show()