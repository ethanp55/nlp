Steps to run and use the API:
1. Create a python virtual environment and install the packages found in requirements.txt
2. Activate the environment and run the following command to start the app/API: "uvicorn api:app --host 0.0.0.0 --port 8000 --reload"
    - Change the host and port, as needed
3. To use the API, make POST requests to the /convert/ endpoint
    - The request body needs to contain "text" and "n_preds" arguments, where "text" is the chat message to be converted and "n_preds" is the number of predictions to generate (for the user to select from)