from scipy.special import softmax
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class BertClassifier:
    """ """

    def __init__(self, input_phrase):
        save_dir = "app"
        model_name = "cardiffnlp/twitter-roberta-base-sentiment"
        self.model = AutoModelForSequenceClassification.from_pretrained(save_dir)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model.save_pretrained(save_dir)
        self.preprocessing(input_phrase)
        self.formatting()
        self.calc_sentiment()

    def preprocessing(self, input_phrase):
        encoded_input = self.tokenizer(input_phrase, return_tensors="pt")
        output = self.model(**encoded_input)
        scores = output[0][0].detach().numpy()
        self.scores = softmax(scores)

    def formatting(self):
        self.positive_score = "{:.2}".format(self.scores[2])
        self.neutral_score = "{:.2}".format(self.scores[1])
        self.negative_score = "{:.2}".format(self.scores[0])

    def calc_sentiment(self):
        if (
            self.positive_score >= self.negative_score
            and self.positive_score >= self.neutral_score
        ):
            self.sentiment = "Positive"
        elif (
            self.negative_score >= self.positive_score
            and self.negative_score >= self.neutral_score
        ):
            self.sentiment = "Negative"
        else:
            self.sentiment = "Neutral"

    def return_list(self):
        return [
            self.sentiment,
            self.positive_score,
            self.neutral_score,
            self.negative_score,
        ]
