# https://zhuanlan.zhihu.com/p/607909453
# https://zhuanlan.zhihu.com/p/423359955
import logging
import os
import torch

from torch.utils.data import RandomSampler, DataLoader
from transformers import AdamW, get_linear_schedule_with_warmup
from tqdm import tqdm, trange
try:
    from torch.utils.tensorboard import SummaryWriter
except:
    from tensorboardX import SummaryWriter

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
weight_decay = 0.0
learning_rate = 2e-5
adam_epsilon = 1e-8
warmup_steps = 0
max_grad_norm = 1.0

def train(model, train_dataset, train_batch_size, num_train_epochs, save_steps, output_dir):
    train_sampler = RandomSampler(train_dataset)
    train_dataloader = DataLoader(train_dataset, sampler=train_sampler, batch_size=train_batch_size)
    t_total = len(train_dataloader) // num_train_epochs

    # Prepare optimizer and schedule (linear warmup and decay)
    no_decay = ['bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
         'weight_decay': weight_decay},
        {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)],
         'weight_decay': 0.0}
    ]
    optimizer = AdamW(optimizer_grouped_parameters, lr=learning_rate, eps=adam_epsilon)
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=warmup_steps,
        num_training_steps=t_total
    )
    # Train!
    logging.info("***** Running training *****")
    logging.info("  Num examples = %d", len(train_dataset))
    logging.info("  Num Epochs = %d", num_train_epochs)
    logging.info("  Instantaneous batch size per GPU = %d", train_batch_size)
    logging.info("  Total train batch size (w. parallel, distributed & accumulation) = %d", train_batch_size)
    logging.info("  Total optimization steps = %d", t_total)

    global_step = 0
    tr_loss, logging_loss = 0.0, 0.0
    model.zero_grad()

    tb_writer = SummaryWriter('./runs/bert')
    train_iterator = trange(int(num_train_epochs), desc="Epoch", disable=False)
    for _ in train_iterator:
        epoch_iterator = tqdm(train_dataloader, desc="Iteration", disable=False)
        for step, batch in enumerate(epoch_iterator):
            model.train()
            batch = tuple(t.to(DEVICE) for t in batch)
            inputs = {
                'input_ids': batch[0],
                'attention_mask': batch[1],
                'labels': batch[3],
                'token_type_ids': batch[2]
            }
            outputs = model(**inputs)
            loss = outputs[0]  # model outputs are always tuple in transformers (see doc)
            loss.backward()

            tr_loss += loss.item()

            torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
            optimizer.step()
            scheduler.step()  # Update learning rate schedule
            model.zero_grad()
            global_step += 1

            if global_step % 100 == 0:
                tb_writer.add_scalar('lr', scheduler.get_lr()[0], global_step)
                tb_writer.add_scalar('loss', (tr_loss - logging_loss) / 100, global_step)
                logging_loss = tr_loss

            if global_step % save_steps == 0:
                model_to_save = model.module if hasattr(model, 'module') else model
                model_to_save.save_pretrained(
                    os.path.join(output_dir, f'checkpoint-{global_step}')
                )
            if global_step > 50000:
                break
    tb_writer.close()

    return global_step, tr_loss / global_step
