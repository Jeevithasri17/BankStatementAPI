Open git bash.

Add the project directory.

Run the following commands.

1) virtualenv venv
2) source venv/scripts/activate
3) pip install python-multipart
4) pip install pymongo fastapi uvicorn pdfplumber
5) uvicorn index:app --reload
