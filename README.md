# Ba Zi Destiny Reader

A FastAPI web application that uses "The Eight Characters" (Ba Zi) Chinese astrology to predict a user's destiny using the Gemini API. The response is streamed back to the user in real-time.

## Features

- **Ba Zi Astrology**: Uses birth date, time, and location to generate a personalized reading.
- **Gemini API Integration**: Leverages Google's Gemini Pro model for generating the content.
- **Streaming Response**: The prediction streams to the client for a better user experience.
- **Tai Chi Bagua UI**: A themed interface inspired by traditional Chinese aesthetics.

## Prerequisites

- Python 3.11+
- A Google Cloud Project with the Vertex AI API enabled (or a direct Gemini API key).
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed (for deployment).

## Local Development

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <repo-name>
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set your Google API Key:**
    You need an API key for Google Gemini. Get one from [Google AI Studio](https://aistudio.google.com/).
    ```bash
    export GOOGLE_API_KEY="your_api_key_here"
    # On Windows (PowerShell): $env:GOOGLE_API_KEY="your_api_key_here"
    ```

5.  **Run the application:**
    ```bash
    python app/main.py
    ```
    Or using uvicorn directly:
    ```bash
    uvicorn app.main:app --reload
    ```

6.  **Access the app:**
    Open your browser and go to `http://localhost:8080`.

## Deploy to Google Cloud Run

1.  **Install and initialize gcloud CLI:**
    Follow instructions [here](https://cloud.google.com/sdk/docs/install) if you haven't already.
    ```bash
    gcloud init
    ```

2.  **Build and Deploy:**
    Replace `PROJECT_ID` with your Google Cloud Project ID and `SERVICE_NAME` with your desired service name (e.g., `bazi-reader`).

    ```bash
    gcloud run deploy SERVICE_NAME \
      --source . \
      --project PROJECT_ID \
      --region us-central1 \
      --allow-unauthenticated \
      --set-env-vars GOOGLE_API_KEY="your_api_key_here"
    ```

    ### Using Google Secret Manager (Recommended for Production)

    Instead of passing the API key directly in the command line (which can leave traces in history), use Google Secret Manager:

    1.  **Enable Secret Manager API:**
        ```bash
        gcloud services enable secretmanager.googleapis.com
        ```

    2.  **Create the secret:**
        ```bash
        echo -n "your_api_key_here" | gcloud secrets create gemini-api-key --data-file=-
        ```

    3.  **Grant access to the Cloud Run service account:**
        (Replace `PROJECT_NUMBER` with your project number, found in the dashboard)
        ```bash
        gcloud secrets add-iam-policy-binding gemini-api-key \
          --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
          --role="roles/secretmanager.secretAccessor"
        ```

    4.  **Deploy using the secret:**
        ```bash
        gcloud run deploy SERVICE_NAME \
          --source . \
          --project PROJECT_ID \
          --region us-central1 \
          --allow-unauthenticated \
          --set-secrets GOOGLE_API_KEY=gemini-api-key:latest
        ```

3.  **Access the deployed app:**
    The command will output a Service URL (e.g., `https://bazi-reader-xyz-uc.a.run.app`). Click it to view your live application.

## Project Structure

```
/
  app/
    __init__.py
    main.py           # FastAPI application and logic
    templates/
      index.html      # Frontend HTML
    static/
      style.css       # CSS styling
      script.js       # Client-side JavaScript
  Dockerfile          # Container configuration
  requirements.txt    # Python dependencies
  README.md           # Documentation
```
