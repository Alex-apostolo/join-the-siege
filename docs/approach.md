# File Classifier

I built a file classifier which can process `pdf`, `png`, `jpg`, `xlsx`, `xls`, `docx` and `txt` files. When no selectable text is available on a PDF or if its an image OCR is used; otherwise specific loaders to handle text extraction are used.

Once the text is extracted, the classifier assigns a label based on the content.

For the model, I fine-tuned DistilBERT. I chose to use a transformer as it excels at NLP tasks and in this case we are dealing with structured data that have high variability in their format and content. Other models would struggle to generalise without the use of contextual embeddings. DistilBERT keeps most of BERT’s strengths but it is a distilled model meaning its significatly smaller making it faster at training and inferencing without sacrificing much of the performance.

For the dataset, I generated realistic training data for fine-tuning the model using OpenAI's chat completions with a custom prompt. The synthetic data are very easy to scale to new industries by just adding a new key value pair on the `content_types`. The model was fine tuned only in the synthetic dataset and the accuracy on the test set was 100%.

The app is optimized for real-time performance and supports asynchronous requests. I configured Gunicorn with 4 worker processes, which can be scaled further on more powerful machines. Inference runs on the CPU, as there’s no major benefit to using a GPU in this case.

The app is Dockerized for easy deployment, making it ready for production environments like AWS EC2.

## Testing and Scaling

I tested the classifier using real documents, running `test_classifier_on_unseen_data` all 12 documents were correctly predicted. For scalability testing, I simulated 1,000 concurrent request calls which was completed in 40 seconds in my low performance laptop. With enough compute this time can drop drastically.

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

This classifier was extended to be useful for the insurance industry since insurers can analyse a companys balance sheets and income statements to understand the financial state of a company before creating an underwriting for them.

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
