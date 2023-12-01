# https://blog.csdn.net/qq_43645301/article/details/108811403
import logging
import os
import torch
import json
import os
from transformers import DataProcessor, InputExample
from transformers import glue_convert_examples_to_features
from torch.utils.data import TensorDataset

class LawlawProcessor(DataProcessor):
    def __init__(self, task, data_dir):
        super(DataProcessor, self).__init__()
        self.task = task
        self.data_dir = data_dir

    '''
    def get_example_from_tensor_dict(self, tensor_dict):
        print("=======AAAAAAAAAAAAA=======")
        return InputExample(
            tensor_dict['idx'].numpy(),
            tensor_dict['sentence'].numpy().decode('utf-8'),
            None,
            str(tensor_dict['label'].numpy())
        )
    '''

    def get_labels(self):
        return [
            "法律法条",
            "法律书籍",
            "法律文书模板",
            "法律案例",
            "法律考试"
        ]

    def get_train_examples(self):
        return self._create_examples(
            self._read_json(os.path.join(self.data_dir, f"{self.task}_data.json")),
            "train"
        )

    def get_dev_examples(self):
        return self._create_examples(
            self._read_json(os.path.join(self.data_dir, f"{self.task}_dev.json")),
            "dev"
        )

    def _read_json(self, input_file):
        with open(input_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def _create_examples(self, lines, set_type):
        return [
            InputExample(
                guid=f"{set_type}-{i}",
                text_a=line[1],
                text_b=None,
                label=line[0]
            )
            for (i, line) in enumerate(lines)
        ]

    def load_train_examples(self, tokenizer, max_seq_length):
        cached_features_file = os.path.join(
            self.data_dir,
            f'cached_train_{max_seq_length}_{self.task}'
        )
        if os.path.exists(cached_features_file):
            logging.info("Loading features from cached file %s", cached_features_file)
            features = torch.load(cached_features_file)
        else:
            logging.info("Creating features from dataset file at %s", self.data_dir)
            features = glue_convert_examples_to_features(
                self.get_train_examples(),
                tokenizer,
                max_length=max_seq_length,
                task=None,
                label_list=self.get_labels(),
                output_mode="classification",
            )
            logging.info("Saving features into cached file %s", cached_features_file)
            torch.save(features, cached_features_file)
        return self._create_dataset(features)

    def load_dev_examples(self, tokenizer, max_seq_length):
        cached_features_file = os.path.join(
            self.data_dir,
            f'cached_dev_{max_seq_length}_{self.task}'
        )
        if os.path.exists(cached_features_file):
            logging.info("Loading features from cached file %s", cached_features_file)
            features = torch.load(cached_features_file)
        else:
            logging.info("Creating features from dataset file at %s", self.data_dir)
            features = glue_convert_examples_to_features(
                self.get_dev_examples(),
                tokenizer,
                max_length=max_seq_length,
                task=None,
                label_list=self.get_labels(),
                output_mode="classification",
            )
            logging.info("Saving features into cached file %s", cached_features_file)
            torch.save(features, cached_features_file)
        return self._create_dataset(features)

    def _create_dataset(self, features):
        # Convert to Tensors and build dataset
        all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
        all_attention_mask = torch.tensor([f.attention_mask for f in features], dtype=torch.long)
        all_token_type_ids = torch.tensor([f.token_type_ids for f in features], dtype=torch.long)
        all_labels = torch.tensor([f.label for f in features], dtype=torch.long)
        return TensorDataset(
            all_input_ids,
            all_attention_mask,
            all_token_type_ids,
            all_labels
        )
