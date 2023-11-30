import logging
import argparse

from berttextclassification.BertModel import set_seed, init_model, load_model, save_model
from berttextclassification.DataLawlaw import LawlawProcessor
from berttextclassification.evaluate import evaluate
from berttextclassification.train import train

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", default='./outs', type=str, required=False,
        help="The output directory where the model predictions and checkpoints will be written.")
    parser.add_argument("--data_dir", default='./data', type=str, required=False,
        help="The data directory where the train data and evaluate data already set.")
    parser.add_argument("--cache_dir", default='./cache', type=str, required=False,
        help="The directory where train model already set.")
    parser.add_argument("--max_seq_length", default=128, type=int,
        help="The maximum total input sequence length after tokenization. Sequences longer "
             "than this will be truncated, sequences shorter will be padded.")
    parser.add_argument("--do_train", default=False, action='store_true',
        help="Whether to run training.")
    parser.add_argument("--do_eval", default=True, action='store_true',
        help="Whether to run eval on the dev set.")
    parser.add_argument("--train_batch_size", default=8, type=int,
        help="Batch size per GPU/CPU for training.")
    parser.add_argument("--eval_batch_size", default=16, type=int,
        help="Batch size per GPU/CPU for evaluation.")
    parser.add_argument("--num_train_epochs", default=50.0, type=float,
        help="Total number of training epochs to perform.")
    parser.add_argument('--save_steps', type=int, default=12500,
        help="Save checkpoint every X updates steps.")
    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S',
        level=logging.INFO
    )
    set_seed()

    logging.info("Training/evaluation parameters %s", args)
    task = 'lawlaw'
    processor = LawlawProcessor(task, args.data_dir)
    if args.do_train:
        label_list = processor.get_labels()
        model, tokenizer = init_model(task, len(label_list), args.cache_dir)
        train_dataset = processor.load_train_examples(tokenizer, args.max_seq_length)
        global_step, tr_loss = train(
            model,
            train_dataset,
            args.train_batch_size,
            args.num_train_epochs,
            args.save_steps,
            args.output_dir
        )
        logging.info(" global_step = %s, average loss = %s", global_step, tr_loss)
        save_model(model, tokenizer, args.output_dir)
    if args.do_eval:
        model, tokenizer = load_model(args.output_dir)
        eval_dataset = processor.load_dev_examples(tokenizer, args.max_seq_length)
        result = evaluate(
            model,
            eval_dataset,
            args.eval_batch_size,
            args.output_dir
        )
        print(result)

if __name__ == "__main__":
    main()
