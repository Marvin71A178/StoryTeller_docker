import json, os
from transformers import AutoTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import torch
import argparse

from Utils.color_print import head_print

parser = argparse.ArgumentParser(description='optional arg')
parser.add_argument('-d', '--dataset', help='dataset path.')
parser.add_argument('-o', '--output', help='model saving path after trained.')

args = parser.parse_args()
dataset_path = args.dataset
mode_save_path = args.output

## ===== Config ===== ##
DATASET_FILE_PATH = dataset_path if dataset_path is not None else "assets/template_dataset.json" 
TRAINNING_ARGS_OUTPUT_DIR = "result"
SAVE_MODEL_NAME = mode_save_path if mode_save_path is not None else "test_model" 
PATH_TO_SAVE_MODEL = os.path.join(TRAINNING_ARGS_OUTPUT_DIR, SAVE_MODEL_NAME)
MODEL_NAME = "bert-base-chinese"

## ===== Trainning Settings ===== ##
NUM_TRAIN_EPOCH = 10
DEVICE_TRAIN_BATCH = 2


class BertSC:
    class Dataset(torch.utils.data.Dataset):
        """Custom Dataset Class"""
        def __init__(self, encodings, labels):
            self.encodings = encodings
            self.labels = labels

        def __getitem__(self, idx):
            item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
            item['labels'] = torch.tensor(self.labels[idx])
            return item

        def __len__(self):
            return len(self.labels)
        
    def __init__(self, model_name: str, texts: list[str], labels: list[int], training_arguments: TrainingArguments = None) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = BertForSequenceClassification.from_pretrained(model_name, num_labels=self._get_num_labels(labels))
        self.train_dataset = self._transform_to_dataset(texts, labels)
        self.training_arguments = training_arguments
        self.trainer = None
        self._apply_to_cuda()
    
    def is_cuda_avaliable(self) -> bool:
        return torch.cuda.is_available()
    
    def _apply_to_cuda(self) -> None:
        device = "cuda:0" if self.is_cuda_avaliable() else "cpu"
        self.model = self.model.to(device)
        
    def _transform_to_dataset(self, texts: list[str], labels: list[any]) -> "BertSC.Dataset":
        """Transform the text list & label list to Dataset"""
        encodings = self.tokenizer(texts, truncation=True, padding=True)
        dataset = BertSC.Dataset(encodings, labels)
        return dataset

    def _get_num_labels(self, labels) -> int:
        "Get the number of labels by find the maximum. (label range)"
        return max(labels) + 1

    def train(self, training_arguments: TrainingArguments = None) -> None:
        """Start training data"""
        if training_arguments is not None:
            self.training_arguments = training_arguments
        
        self.trainer = Trainer (
            model= self.model,
            args = self.training_arguments,
            train_dataset = self.train_dataset
        )
        
        self.trainer.train()
        
    def save_model(self, save_path: str) -> None:
        self.trainer.save_model(save_path)

def get_data_json(filename: str) -> any:
    with open(filename, "r", encoding='UTF-8') as file:
        data_json = json.load(file)
    return data_json

def main() -> None:
    if not os.path.isfile(DATASET_FILE_PATH):
        raise Exception(f"[ERROR] {DATASET_FILE_PATH} not exist!")
    
    ## ===== Info Print ===== ##
    head_print("[CUDA SUPPORT] ", torch.cuda.is_available())
    
    ## ===== Import Train Data ===== ##
    train_raw_data = get_data_json(DATASET_FILE_PATH)
    texts = [x[0] for x in train_raw_data]
    labels = [int(x[1]) for x in train_raw_data]
    
    ## ===== Trainning Settings ===== ## 
    training_args = TrainingArguments(
        output_dir = TRAINNING_ARGS_OUTPUT_DIR,
        num_train_epochs = NUM_TRAIN_EPOCH,
        per_device_train_batch_size = DEVICE_TRAIN_BATCH,
        # warmup_steps=10,
        weight_decay=0.01,
    )
    
    bsc = BertSC(
        model_name = MODEL_NAME,
        texts = texts,
        labels = labels,
        training_arguments = training_args
    )
    
    bsc.train()
    bsc.save_model(PATH_TO_SAVE_MODEL)

if __name__ == "__main__":
    main()