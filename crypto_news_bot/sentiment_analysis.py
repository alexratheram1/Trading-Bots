from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_headlines(headlines):
    scores= []

    for headline in headlines:
        sentiment = analyzer.polarity_scores(headline)
        compound_score = sentiment['compound']
        scores.append(compound_score)

        if scores:
            average_score = sum(scores) / len(scores)
            return average_score
        else:
            return 0