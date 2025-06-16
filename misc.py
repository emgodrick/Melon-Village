from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = "textdetox/xlmr-large-toxicity-classifier-v2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

text = "You are amazing!"
inputs = tokenizer(text, return_tensors="pt")

outputs = model(**inputs)
print(outputs.logits)
