import requests
from bs4 import BeautifulSoup
import pandas as pd

"""**For** **Classification**"""

import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

from google.colab import files

"""# **Web Scraping links of news article**"""

def extract_links(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = set()
            for link in soup.find_all('a', href=True):
                links.add(link['href'])

            links_list = list(links)[:]
            return links_list

        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

website_url = 'https://economictimes.indiatimes.com/'
result_links = extract_links(website_url)

print("Extracted links:")
for idx, link in enumerate(result_links):
    print(f"{idx + 1}. {link}")

"""**Kepping links that are of certain category/section**"""

valid_prefixes = ('/news', '/markets', '/opinion', '/tech', '/rise', '/industry', '/politics', '/careers', '/wealth', '/nri', '/jobs', '/opinion')

filtered_list = [item for item in result_links if item.startswith(valid_prefixes)]
for art in filtered_list:
    print(art)

"""**Adding the base url to make it accessible**"""

result = ["https://economictimes.indiatimes.com/news/politics/" + row for row in filtered_list if len("https://economictimes.indiatimes.com/news/politics" + row) > 100]

print(len(result))

"""# **Extracting news and heading**"""

def scrape_usa_today_links(link_list):
    dfs = []

    for idx, url in enumerate(link_list, start=1):
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            news_heading_element = soup.find('h1')
            news_heading = news_heading_element.text.strip() if news_heading_element else None

            synopsis_element = soup.find('h2', class_='summary')
            synopsis = synopsis_element.text.strip() if synopsis_element else None

            data = {'sr. no.': [idx], 'heading': [news_heading], 'synopsis': [synopsis], 'link': [url]}
            df = pd.DataFrame(data)

            dfs.append(df)
        else:
            print(f"Error: Unable to fetch content from {url}")

    result_df = pd.concat(dfs, ignore_index=True)

    return result_df

list_of_links = result
result_df = scrape_usa_today_links(list_of_links)

print(result_df)

result_df

"""**Preprocessing the extracted text**"""

result_df.isna().sum()

df = result_df.dropna()

df

df_trial = df

"""**Getting the Category**"""

def extract_section(link):
    without_prefix = link.replace("https://economictimes.indiatimes.com/news/politics//", "")
    section = without_prefix.split('/')[0]
    return section

df_trial['section'] = df_trial['link'].apply(extract_section)

df_trial

# number of sections
df_trial.section.unique()

"""**Convert to CSV**"""

df_trial.to_csv('extracted_news_article.csv', index=False)

files.download('extracted_news_article.csv')

"""# **Classifing using Model**"""

X = df_trial['synopsis']
y = df_trial['section']

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TF-IDF vectorization
tfidf_vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

knn_classifier = KNeighborsClassifier(n_neighbors=5)

# Evaluate KNN using cross-validation
cv_scores = cross_val_score(knn_classifier, X_train_tfidf, y_train, cv=10, scoring='accuracy')

print('K-Nearest Neighbors:')
print(f'Cross-validated accuracy scores: {cv_scores}')
print(f'Mean accuracy: {cv_scores.mean()}')
print('---')

# Train KNN on the full training set and evaluate on the test set
knn_classifier.fit(X_train_tfidf, y_train)
y_pred = knn_classifier.predict(X_test_tfidf)
test_accuracy = accuracy_score(y_test, y_pred)

print(f'K-Nearest Neighbors Test Accuracy: {test_accuracy}')

"""# **Test for a link**"""

link1 = input("Enter the link of a article of economies time : ")

def extract_section(link):
    without_prefix = link.replace("https://economictimes.indiatimes.com/", "")
    section = without_prefix.split('/')[0]
    return section

def scrape_synopsis_and_predict_section(link, vectorizer, classifier):
    try:
        response = requests.get(link)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            news_heading_element = soup.find('h1')
            news_heading = news_heading_element.text.strip() if news_heading_element else None

            synopsis_element = soup.find('h2', class_='summary')
            synopsis = synopsis_element.text.strip() if synopsis_element else None

            # Vectorize the synopsis using the pre-trained vectorizer
            synopsis_tfidf = vectorizer.transform([synopsis])

            # Predict the section using the pre-trained classifier
            predicted_section = classifier.predict(synopsis_tfidf)[0]

            return {
                'heading': news_heading,
                'synopsis': synopsis,
                'predicted_section': predicted_section
            }

        else:
            return f"Error: Unable to fetch content from {link}"

    except Exception as e:
        return f"An error occurred: {e}"

result1 = scrape_synopsis_and_predict_section(link1, tfidf_vectorizer, knn_classifier)

# Print the result
print(result1)
