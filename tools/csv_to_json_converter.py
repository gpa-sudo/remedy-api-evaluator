import csv
import json
import re
import argparse


def convert_csv_to_json(input_file, output_file):
    """
    Converts CSV file to structured JSON.

    Required CSV columns:
    - Remedy
    - Category_Name
    - Symptom
    """

    data = {"Drug": {}}

    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            remedy_raw = (row.get("Remedy") or "").strip()
            category = (row.get("Category_Name") or "").strip()
            symptom = (row.get("Symptom") or "").strip()

            if not remedy_raw or not symptom:
                continue

            # Extract remedy name from patterns like "ABC. (Full Name)"
            match = re.match(r"^(.*)\.\s*\((.*)\)\.?$", remedy_raw)
            if match:
                remedy = match.group(2).strip().upper()
            else:
                remedy = remedy_raw.rstrip(".").strip().upper()

            if remedy not in data["Drug"]:
                data["Drug"][remedy] = {"symptoms": []}

            data["Drug"][remedy]["symptoms"].append({
                "heading": category,
                "text": symptom
            })

    # Add metadata
    for remedy in data["Drug"]:
        data["Drug"][remedy]["total_symptoms"] = len(
            data["Drug"][remedy]["symptoms"]
        )
        data["Drug"][remedy]["source_url"] = "optional"

    # Save JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("✅ Conversion complete!")
    print("Output saved to:", output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSV to JSON Remedy Dataset Converter")

    parser.add_argument("--input", required=True, help="Input CSV file")
    parser.add_argument("--output", required=True, help="Output JSON file")

    args = parser.parse_args()

    convert_csv_to_json(args.input, args.output)
