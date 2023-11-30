# https://www.cnblogs.com/zhangxianrong/p/15066981.html
from berttextclassification.BertModel import load_model
from berttextclassification.DataLawlaw import LawlawProcessor
import torch

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
labels = LawlawProcessor('lawlaw').get_labels()
model = None
tokenizer = None

def init_model(model_path):
    global model
    model, tokenizer = load_model(model_path)

def predict(lines):
    model.eval()
    tokenized_text = tokenizer(
        lines,
        max_length=128,
        add_special_tokens=True,
        truncation=True,
        padding=True,
        return_tensors="pt"
    )
    tokenized_text = tokenized_text.to(DEVICE)
    with torch.no_grad():
        logits = model(**tokenized_text, labels=None)
    pred = logits[0].argmax() % len(labels)
    return labels[pred]
