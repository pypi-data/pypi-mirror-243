import logging
import random
import numpy
import torch
import os
from transformers import BertConfig, BertForSequenceClassification, BertTokenizer

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
N_GPU  = torch.cuda.device_count()
logging.warning("device: %s, n_gpu: %s", DEVICE, N_GPU)

def set_seed(seed=42):
    random.seed(seed)
    numpy.random.seed(seed)
    torch.manual_seed(seed)

def init_model(task, num_labels, cache_dir):
    model_name_or_path = cache_dir # 'bert-base-chinese'
    config = BertConfig.from_pretrained(
        model_name_or_path,
        num_labels=num_labels,
        finetuning_task=task,
        cache_dir=cache_dir
    )
    model = BertForSequenceClassification.from_pretrained(
        model_name_or_path,
        from_tf=False,
        config=config,
        cache_dir=cache_dir
    )
    tokenizer = BertTokenizer.from_pretrained(
        model_name_or_path,
        do_lower_case=False,
        cache_dir=cache_dir
    )
    model.to(DEVICE)
    return (model, tokenizer)

def load_model(output_dir):
    logging.info("Evaluate the following checkpoint: %s", output_dir)
    model = BertForSequenceClassification.from_pretrained(output_dir)
    tokenizer = BertTokenizer.from_pretrained(
        output_dir,
        do_lower_case=False
    )
    model.to(DEVICE)
    return (model, tokenizer)

def save_model(model, tokenizer, output_dir):
    logging.info("Saving model checkpoint to %s", output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Take care of distributed/parallel training
    model_to_save = model.module if hasattr(model, 'module') else model
    model_to_save.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
