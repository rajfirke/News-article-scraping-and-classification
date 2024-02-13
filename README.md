# Web Scraping and Classification of News article

This application performs web scraping on the Economics Times website to collect news articles and then applies text classification to categorize the articles into different sections. The classification model is trained using Machine Learning techniques.

## Instructions to Run the Application

### Prerequisites

- Python 3.10 installed
- Required Python packages installed (`pandas`, `beautifulsoup4`, `KNeighborsClassifier`, `TfidfVectorizer`)

### Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/rajfirke/News-article-scraping-and-classification.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd News-article-scraping-and-classification
    ```

3. **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

### Web Scraping

1. **Run the web_scraping.py script to gather news articles from NPR:**

    ```bash
    python web_scraping.py
    ```

   This script scrapes articles from different sections of the NPR website and saves the data to CSV files (`scraped_data1.csv`, `scraped_data2.csv`, etc.).

### Text Classification

1. **Ensure you have the required datasets in the project folder (e.g., scraped_data1.csv, scraped_data2.csv).**

2. **Run the text_classification.py script to preprocess the text, train the classification model, and evaluate its performance:**

    ```bash
    python text_classification.py
    ```

   The script will display accuracy and classification reports for the text classification model.

## Notes

- If needed, adjust the parameters in the text classification script (`text_classification.py`) such as vectorizer settings, model parameters, etc.

- Feel free to explore and modify the code to suit your specific use case or enhance functionality.

---

# Web Scraping and Text Classification Application

This application extracts news articles from the Economic Times website using web scraping and classifies them into different sections using a machine learning model.

## Installing Dependencies

### For Web Scraping

```bash
pip install requests beautifulsoup4 pandas
```
# Screenshots
<div align="center">
    
![Final Dataset](News%20article%20scraping/Screenshots/Final%20dataset.png)

![Link based classification](News%20article%20scraping/Screenshots/Link%20based%20classification.png)

</div>
