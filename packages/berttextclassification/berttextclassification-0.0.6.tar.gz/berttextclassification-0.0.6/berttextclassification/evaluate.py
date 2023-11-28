import logging
import os
import torch
import numpy

from torch.utils.data import SequentialSampler, DataLoader
from tqdm import tqdm
from berttextclassification.acc_and_f1 import acc_and_f1

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def evaluate(model, eval_dataset, eval_batch_size, output_dir):
    eval_sampler = SequentialSampler(eval_dataset)
    eval_dataloader = DataLoader(eval_dataset, sampler=eval_sampler, batch_size=eval_batch_size)

    logging.info("***** Running evaluation *****")
    logging.info("  Num examples = %d", len(eval_dataset))
    logging.info("  Batch size = %d", eval_batch_size)
    eval_loss = 0.0
    nb_eval_steps = 0
    preds = None
    out_labels = None
    for batch in tqdm(eval_dataloader, desc="Evaluating"):
        model.eval()
        batch = tuple(t.to(DEVICE) for t in batch)

        with torch.no_grad():
            inputs = {
                'input_ids': batch[0],
                'attention_mask': batch[1],
                'labels': batch[3],
                'token_type_ids': batch[2]
            }
            outputs = model(**inputs)
            tmp_eval_loss, logits = outputs[:2]
            eval_loss += tmp_eval_loss.mean().item()
        nb_eval_steps += 1
        if preds is None:
            preds = logits.detach().cpu().numpy()
            out_labels = inputs['labels'].detach().cpu().numpy()
        else:
            preds = numpy.append(preds, logits.detach().cpu().numpy(), axis=0)
            out_labels = numpy.append(out_labels, inputs['labels'].detach().cpu().numpy(), axis=0)

    eval_loss = eval_loss / nb_eval_steps
    preds = numpy.argmax(preds, axis=1)
    result = acc_and_f1(preds, out_labels)

    '''
    label_mapping = {0: "法律法条", 1: "法律书籍", 2: "法律文书模板", 3: "法律案例", 4: "法律考试"}
    preds_str = [label_mapping[pred] for pred in preds]
    labels_str = [label_mapping[label] for label in out_labels]
    print(preds_str)
    print(labels_str)
    '''

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_eval_file = os.path.join(output_dir, "eval_results.txt")
    with open(output_eval_file, "w") as f:
        logging.info("***** Eval results *****")
        for key in sorted(result.keys()):
            logging.info("  %s = %s", key, str(result[key]))
            f.write("%s = %s\n" % (key, str(result[key])))
    return result
