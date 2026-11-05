# Expense Tracker AI

Expense Tracker AI is a simple REST API that helps users record their daily expenses. It uses Google Gemini AI to automatically identify the category of each expense.

The project is built using Python, FastAPI, and SQLite.

## What Does It Do?

- **Add Expenses:** Users can add an expense by providing its description and amount.
- **Automatic Categorization:** Gemini AI reads the expense description and selects a suitable category.
- **View Expenses:** Users can view all the expenses they have saved.
- **Expense Categories:** Food, Transport, Shopping, Bills, Entertainment, Health, Education, and Other.

   ```http
   POST /expenses
   {"description": "Swiggy dinner", "amount": 450}
   ```
   Response:
   ```json
   {"id": 1, "description": "Swiggy dinner", "amount": 450, "category": "Food"}
   ```

## How Does It Work?

1. The user sends an expense description and amount.
2. FastAPI receives the request and checks whether the input is valid.
3. Google Gemini AI analyzes the description and selects a category.
4. The expense and its category are saved in the SQLite database.
5. The user can retrieve the saved expenses through the API.

**Simple flow:**

User → FastAPI → Gemini AI → SQLite Database

## Handling Errors

I added some features to make the application work more reliably:

- If Gemini temporarily fails with a 503 error, the application tries again after waiting.
- If Gemini returns a 429 error because of usage limits, the application stops retrying.
- The application checks whether the AI-selected category is one of the allowed categories.
- If the AI is unavailable or fails, the expense is still saved as "Uncategorized".
- If the same expense description is entered again, the application can reuse the previously identified category through an in-memory cache.

## Accuracy Testing

I tested the AI using 30 expense descriptions that I categorized manually.

- Correct predictions: 25
- Incorrect predictions: 5
- Accuracy: **83%**

Some descriptions were difficult for the AI to categorize because they could belong to more than one category.

For example:
- Medicine could be classified as Health or Bills.
- Skin care products could be classified as Health or Shopping.

This was a small test, so the result should only be considered an initial check of how well the AI works.

To run the accuracy test:

```bash
python accuracy_check.py
```

## Technologies Used
Gemini model is set in categorizer.py (gemini-3.5-flash-lite); model names change often, so check Google’s current list.
- Python – Main programming language.
- FastAPI – To create the REST API.
- Pydantic – To check and validate user input.
- SQLite – To store expense details.
- Google Gemini API – To automatically categorize expenses.
- Pytest – To test the application.

## How to Run the Project

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the virtual environment.

For Windows:

```bash
venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=your_key
```

5. Start the application:

```bash
uvicorn main:app --reload
```

6. Open the following link in your browser to test the API:

http://127.0.0.1:8000/docs

## Testing

The project includes 7 automated tests using Pytest.

The tests use a fake AI response, so you don't need to call the actual Gemini API while running them.

Run the tests using:

```bash
pytest -v
```

## Current Limitations

- The application uses the Gemini free tier, which has usage limits.
- If the AI fails, the expense is saved as Uncategorized.
- Previously identified categories are stored in memory and are cleared when the application restarts.
- The application does not currently have user registration or login features.

## Future Improvements

- Use PostgreSQL instead of SQLite for better database support.
- Add database migrations to manage changes to the database.
- Use Docker to make the application easier to run on different systems.
- Allow users to correct incorrect expense categories and use those corrections to improve future AI categorization.

## Live Demo

Coming soon!