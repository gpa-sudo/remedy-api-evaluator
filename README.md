# Remedy API Accuracy Evaluator

A lightweight evaluation tool to measure the top-1 prediction accuracy of a symptom-to-remedy AI backend. The script sends batch symptom queries to a REST API and compares predicted remedies with expected labels from a CSV file.

---

## Features

- 📊 **Batch CSV testing** - Process multiple test cases at once
- 🎯 **Top-1 accuracy evaluation** - Measure prediction accuracy
- 📈 **Similarity score recording** - Track confidence scores
- 📑 **Excel-compatible output** - Easy result analysis
- ⚙️ **Command-line interface** - Simple to use and automate
- 🔧 **Configurable API endpoint** - Works with any compatible backend
- ⏱️ **Rate limiting** - Built-in delay between API calls

---

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

---

## Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/remedy-api-evaluator.git
   cd remedy-api-evaluator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Input CSV Format

Your input CSV file must contain the following columns:

| Column | Description |
|--------|-------------|
| `Symptoms` | Text description of symptoms |
| `Drug` | Expected remedy/drug name |

### Example Input File

```csv
Symptoms,Drug
Burning stomach pain,Drug_1
Severe headache with nausea,Drug_2
Chronic fatigue and weakness,Drug_3
```

See `sample_input.csv` for a complete example.

---

## Usage

### Basic Usage

Run evaluation with default settings:

```bash
python accuracy_tester.py --input sample_input.csv
```

### Custom API Endpoint

Specify a custom API endpoint:

```bash
python accuracy_tester.py --input sample_input.csv --api http://localhost:5000/analyze
```

### Custom Output File

Specify a custom output file name:

```bash
python accuracy_tester.py --input sample_input.csv --output results.csv
```

### Set API Delay

Control the delay between API calls (useful for rate limiting):

```bash
python accuracy_tester.py --input sample_input.csv --delay 0.5
```

### Complete Example

```bash
python accuracy_tester.py \
  --input my_test_cases.csv \
  --api http://localhost:5000/analyze \
  --output evaluation_results.csv \
  --delay 0.3
```

### Using Environment Variables

You can set the API URL via environment variable:

```bash
export API_URL=http://localhost:5000/analyze
python accuracy_tester.py --input sample_input.csv
```

---

## Command-Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--input` | Yes | - | Path to input CSV file |
| `--api` | No | `http://localhost:5000/analyze` | API endpoint URL (or from `API_URL` env var) |
| `--output` | No | `prediction_results.csv` | Output CSV file path |
| `--delay` | No | `0.2` | Delay between API calls in seconds |

---

## Output Format

The script generates a CSV file with the following columns:

| Column | Description |
|--------|-------------|
| `Symptom` | Original symptom description |
| `Expected Drug` | Expected remedy from input |
| `Predicted Drug` | API-predicted remedy |
| `Similarity` | Confidence/similarity score |
| `Status` | Success, Failure, or Failure (No Response) |

### Example Output

```csv
"Symptom","Expected Drug","Predicted Drug","Similarity","Status"
"Burning stomach pain","Drug_1","Drug_1","0.9542","Success"
"Severe headache with nausea","Drug_2","Drug_3","0.7234","Failure"
"Chronic fatigue","Drug_4","Drug_4","0.8891","Success"
```

The script also prints progress to the console:

```
Testing → Burning stomach pain
Testing → Severe headache with nausea
Testing → Chronic fatigue

---------------------------------------
Evaluation completed successfully
Results saved to: prediction_results.csv
---------------------------------------
```

---

## API Requirements

Your API endpoint must:

1. **Accept POST requests**
2. **Accept JSON payload** with the following structure:
   ```json
   {
     "symptoms": "Burning stomach pain",
     "dataset": "default",
     "top_k": 1
   }
   ```
3. **Return JSON response** with this structure:
   ```json
   {
     "results": [
       {
         "drug": "Drug_1",
         "score": 0.9542
       }
     ]
   }
   ```

The `score` field is optional. If not provided, the similarity column will be empty.

---

## Troubleshooting

### Connection Errors

If you see `[API ERROR]` messages:
- Ensure your API server is running
- Verify the API endpoint URL is correct (default: `http://localhost:5000/analyze`)
- Check firewall/network settings
- Verify the API timeout (currently 15 seconds) is sufficient

### Import Errors

If you see import errors:
```bash
pip install -r requirements.txt --upgrade
```

### CSV Format Errors

If you see `ValueError: CSV must contain columns: Drug, Symptoms`:
- Ensure CSV has headers `Symptoms` and `Drug` (case-sensitive)
- Use UTF-8 encoding
- Remove any empty rows
- Check for proper CSV formatting

### No Results Returned

If predictions show "None":
- Check API response format matches requirements
- Verify API is returning `results` array
- Check server logs for errors

---

## Example Workflow

1. **Prepare test cases**
   ```bash
   # Create or use sample_input.csv with your test data
   cat sample_input.csv
   ```

2. **Start your API server**
   ```bash
   # In another terminal
   python your_api_server.py
   ```

3. **Run the evaluator**
   ```bash
   python accuracy_tester.py --input sample_input.csv
   ```

4. **Review results**
   ```bash
   # Open in Excel or any CSV viewer
   cat prediction_results.csv
   ```

---

## Project Structure

```
remedy-api-evaluator/
├── accuracy_tester.py      # Main evaluation script
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore            # Git ignore rules
├── LICENSE               # MIT License
├── sample_input.csv      # Example input file
└── examples/             # Additional examples
    └── advanced_usage.md
```

---

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Security & Privacy

⚠️ **Important**: This tool sends symptom data to your API endpoint. Ensure:
- You trust the API endpoint you're using
- Sensitive data is transmitted over HTTPS in production
- You comply with relevant data protection regulations (HIPAA, GDPR, etc.)
- Test data does not contain real patient information

---

## Support

For issues or questions:
- 🐛 [Open an issue](https://github.com/yourusername/remedy-api-evaluator/issues)
- 📖 Check existing issues for solutions
- 📧 Contact: your.email@example.com

---

## Changelog

### Version 1.0.0 (Current)
- Initial release
- Basic accuracy evaluation
- CSV input/output support
- Configurable API endpoint
- Rate limiting with adjustable delay
- Environment variable support for API URL

---

**Happy Testing! 🚀**
