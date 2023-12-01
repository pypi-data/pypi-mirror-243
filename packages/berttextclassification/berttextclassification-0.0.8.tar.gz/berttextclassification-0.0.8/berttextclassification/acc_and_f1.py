from sklearn.metrics import f1_score

def acc_and_f1(preds, labels):
    acc = (preds == labels).mean()
    f1 = f1_score(
        y_true=labels,
        y_pred=preds,
        average='weighted'
    )
    return {
        "acc": acc,
        "f1": f1,
        "acc_and_f1": (acc + f1) / 2
    }
