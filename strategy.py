from data_collector import get_crypto_news
from sentiment_analysis import analyze_headlines

api_key = "0530b3cedaec40d2bdd6b0706e343603"

news_data = get_crypto_news(api_key)

if news_data:
    headlines = [article['title'] for article in news_data['articles']]

    sentiment_score = analyze_headlines(headlines)
    print(f" Average sentiment Score: {sentiment_score}")

    threshold = 0.2
    if sentiment_score > threshold:
        print ("decision: LONG")
elif sentiment_score <-threshold:
    print ("decision: SHORT")
else:
    print(" No news data avaliable")
