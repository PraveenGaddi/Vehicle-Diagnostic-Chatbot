# 02_augment_and_prepare_data.py
"""
This script augments the vehicle diagnostic dataset by creating simple paraphrased
versions of the original questions. This helps the model generalize better
to different phrasings of the same problem.

It creates a new CSV file with the augmented data.
"""
import pandas as pd
import random

def simple_paraphrase(question: str) -> list:
    """Creates a few simple variations of a question."""
    question = question.strip()
    variations = {question}  # Use a set to avoid duplicates

    # Variation 1: Add a leading phrase
    leading_phrases = ["What should I do if", "What does it mean when", "Help,"]
    if not any(question.lower().startswith(p.lower()) for p in ["what", "why", "how"]):
         variations.add(f"{random.choice(leading_phrases)} {question[0].lower() + question[1:]}")

    # Variation 2: Change "My car" to "My vehicle"
    if "my car" in question.lower():
        variations.add(question.lower().replace("my car", "my vehicle").capitalize())

    # Variation 3: Change "shows code" to "has code"
    if "shows code" in question.lower():
        variations.add(question.lower().replace("shows code", "has code").capitalize())
        variations.add(question.lower().replace("shows code", "is throwing code").capitalize())

    # Variation 4: Simple rephrasing for common patterns
    if "won't start" in question.lower():
        variations.add(question.lower().replace("won't start", "doesn't start").capitalize())

    if "vibrates a lot" in question.lower():
        variations.add(question.lower().replace("vibrates a lot", "is shaking badly").capitalize())

    return list(variations)

def augment_dataset(input_path: str, output_path: str):
    """
    Reads the original CSV, augments the questions, and saves to a new CSV.
    """
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: The file '{input_path}' was not found.")
        return

    augmented_data = []
    for _, row in df.iterrows():
        original_question = row["question"]
        answer = row["answer"]

        if not isinstance(original_question, str) or not isinstance(answer, str):
            continue

        paraphrased_questions = simple_paraphrase(original_question)
        for q in paraphrased_questions:
            augmented_data.append({"question": q, "answer": answer})

    augmented_df = pd.DataFrame(augmented_data)
    augmented_df.to_csv(output_path, index=False)
    print(f"✅ Successfully augmented dataset!")
    print(f"Original questions: {len(df)}")
    print(f"Augmented questions: {len(augmented_df)}")
    print(f"Saved to '{output_path}'")


if __name__ == "__main__":
    # The script reads the raw data and outputs a new, augmented file.
    augment_dataset("01_raw_vehicle_data.csv", "02_augmented_vehicle_data.csv")
