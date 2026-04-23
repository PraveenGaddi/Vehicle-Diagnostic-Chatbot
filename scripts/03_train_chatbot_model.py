# 03_train_chatbot_model.py
"""
Train a generative vehicle diagnostic chatbot using the T5 model.
This script is now configured to load the base model from a local folder
to avoid download errors.
"""

import argparse
import pandas as pd
import torch
from datasets import Dataset
from transformers import (
    T5ForConditionalGeneration,
    T5TokenizerFast,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
    EarlyStoppingCallback,
)


def load_csv_dataset(path):
    df = pd.read_csv(path)
    assert "question" in df.columns and "answer" in df.columns, "CSV must have `question` and `answer` columns"
    df = df.dropna(subset=["question", "answer"]).reset_index(drop=True)
    return Dataset.from_pandas(df)


def preprocess_examples(examples, tokenizer, max_input_length=256, max_target_length=128):
    inputs = [f"diagnose: {q.strip()}" for q in examples["question"]]
    model_inputs = tokenizer(inputs, max_length=max_input_length, truncation=True, padding="max_length")

    labels = tokenizer(
        text_target=[a.strip() for a in examples["answer"]],
        max_length=max_target_length,
        truncation=True,
        padding="max_length",
    )
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs


def main(args):
    dataset = load_csv_dataset(args.train_csv)
    dataset = dataset.train_test_split(test_size=0.1, seed=42)
    train_ds = dataset["train"]
    val_ds = dataset["test"]

    print(f"Attempting to load model from local path: {args.model_name}")
    tokenizer = T5TokenizerFast.from_pretrained(args.model_name)
    model = T5ForConditionalGeneration.from_pretrained(args.model_name)
    print("✅ Model and tokenizer loaded successfully from local files.")

    def map_fn(ex):
        return preprocess_examples(ex, tokenizer, args.max_input_length, args.max_target_length)

    train_tokenized = train_ds.map(map_fn, batched=True, remove_columns=["question", "answer"])
    val_tokenized = val_ds.map(map_fn, batched=True, remove_columns=["question", "answer"])

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    training_args = Seq2SeqTrainingArguments(
        output_dir=args.output_dir,
        eval_strategy="steps" if args.eval_steps else "epoch",
        eval_steps=args.eval_steps if args.eval_steps else None,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        predict_with_generate=True,
        logging_steps=50,
        save_total_limit=3,
        save_steps=max(500, args.eval_steps if args.eval_steps else 500),
        num_train_epochs=args.epochs,
        learning_rate=args.lr,
        weight_decay=0.01,
        fp16=torch.cuda.is_available(),
        push_to_hub=False,
        load_best_model_at_end=True,
        metric_for_best_model="loss",
        greater_is_better=False,
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_tokenized,
        eval_dataset=val_tokenized,
        tokenizer=tokenizer,
        data_collator=data_collator,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],
    )

    trainer.train()
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    print(f"✅ Training finished. Final model saved to '{args.output_dir}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_csv", type=str, default="02_augmented_vehicle_data.csv")
    # THE KEY CHANGE: This points to your local folder to prevent download errors.
    parser.add_argument("--model_name", type=str, default="./local_flan_t5_base")
    parser.add_argument("--output_dir", type=str, default="./vehicle_chatbot_model_base")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--lr", type=float, default=3e-4)
    parser.add_argument("--max_input_length", type=int, default=256)
    parser.add_argument("--max_target_length", type=int, default=128)
    parser.add_argument("--eval_steps", type=int, default=500)
    args = parser.parse_args()
    main(args)

