"""
Remedy Prediction Accuracy Evaluator

This script evaluates top-1 remedy prediction accuracy
by sending symptom queries to a backend API and comparing
predicted remedies with ground truth labels from a CSV file.
"""

import csv
import requests
import time
import argparse
import os

DEFAULT_API_URL = os.getenv("API_URL", "http://localhost:5000/analyze")


def call_api(symptom, api_url):
    """Send symptom text to backend API and return (predicted_drug, similarity_score)."""

    try:
        payload = {
            "symptoms": symptom,
            "dataset": "default",
            "top_k": 1
        }

        response = requests.post(api_url, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            top_result = data["results"][0]
            return top_result["drug"], top_result.get("score", None)

        return None, None

    except Exception as e:
        print(f"[API ERROR] {e}")
        return None, None


def run_evaluation(input_file, output_file, api_url, delay):

    output_rows = []

    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        required_cols = {"Drug", "Symptoms"}
        if not required_cols.issubset(reader.fieldnames):
            raise ValueError("CSV must contain columns: Drug, Symptoms")

        for row in reader:

            expected = row["Drug"].strip()
            symptom = row["Symptoms"].strip()

            print(f"Testing → {symptom}")

            predicted, score = call_api(symptom, api_url)
            time.sleep(delay)

            if predicted is None:
                status = "Failure (No Response)"
                predicted_str = "None"
                score_str = ""
            else:
                status = "Success" if predicted.lower() == expected.lower() else "Failure"
                predicted_str = predicted
                score_str = f"{score:.4f}" if score is not None else ""

            output_rows.append([
                symptom,
                expected,
                predicted_str,
                score_str,
                status
            ])

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(["Symptom", "Expected Drug", "Predicted Drug", "Similarity", "Status"])
        writer.writerows(output_rows)

    print("\n---------------------------------------")
    print("Evaluation completed successfully")
    print(f"Results saved to: {output_file}")
    print("---------------------------------------")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Remedy Prediction Accuracy Evaluator")

    parser.add_argument("--input", required=True, help="Input CSV file with Symptoms and Drug columns")
    parser.add_argument("--output", default="prediction_results.csv", help="Output CSV filename")
    parser.add_argument("--api", default=DEFAULT_API_URL, help="Backend API endpoint URL")
    parser.add_argument("--delay", type=float, default=0.2, help="Delay between API calls (seconds)")

    args = parser.parse_args()

    run_evaluation(
        input_file=args.input,
        output_file=args.output,
        api_url=args.api,
        delay=args.delay
    )
