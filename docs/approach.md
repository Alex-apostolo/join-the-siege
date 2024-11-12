# File Classifier

I built a file classifier with support for `.xlsx`, `.xls`, `.docx`, and `.txt` files. When no selectable text is available on a PDF or if its an image OCR is used; otherwise, rely on format-specific loaders to handle text extraction.

Once the text is extracted, the classifier assigns a label based on the content.

For the model, I fine-tuned DistilBERT. This choice was due to the high variability in text data and the importance of context, which transformer models like BERT excel at. DistilBERT keeps most of BERT’s strengths but is faster and more efficient. I generated realistic training data for fine-tuning using OpenAI's chat completions with a custom prompt.

The app is optimized for real-time performance and supports asynchronous requests. I configured Gunicorn with 4 worker processes, which can be scaled further on more powerful machines. Inference runs on the CPU, as there’s no major benefit to using a GPU in this case.

The app is Dockerized for easy deployment, making it ready for production environments like AWS EC2.

## Testing and Scaling

I tested the classifier using real documents, running `test_classifier_on_unseen_data` all 12 documents were correctly predicted. For scalability testing, I simulated 1,000 concurrent documents which was completed in 20 seconds in my low performance laptop. With enough compute this time can drop drastically.

The output of `test_classifier_on_unseen_data`:

| File Name              | Label            |
| ---------------------- | ---------------- |
| drivers_license_1.jpg  | drivers_license  |
| drivers_license_3.jpg  | drivers_license  |
| drivers_license_2.jpg  | drivers_license  |
| balance_sheet_3.xlsx   | balance_sheet    |
| balance_sheet_1.pdf    | balance_sheet    |
| bank_statement_1.pdf   | bank_statement   |
| balance_sheet_2.pdf    | balance_sheet    |
| bank_statement_3.pdf   | bank_statement   |
| bank_statement_2.pdf   | bank_statement   |
| income_statement_1.png | income_statement |
| income_statement_2.png | income_statement |
| income_statement_3.png | income_statement |
| invoice_3.pdf          | invoice          |
| invoice_2.pdf          | invoice          |
| invoice_1.pdf          | invoice          |

### Industry Use Case

This classifier could be especially useful for the insurance industry, where insurers can quickly analyze financial documents like income statements and balance sheets to assess the risk of an insurance claim for the specific company.

## Future Enhancements

Potential improvements include model quantization for faster inference and leveraging distributed computing if more scalability is needed.

## Running the Application

1. Build the Docker container:

   ```bash
   docker build -t file_classifier .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 file_classifier
   ```

The app will be accessible at `http://127.0.0.1:8000/classify_file`.
