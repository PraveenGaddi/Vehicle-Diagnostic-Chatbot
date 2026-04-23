# Vehicle Diagnostics Chatbot

## Project Overview
This is a full-stack AI-powered chatbot designed to help vehicle owners diagnose common car problems and interpret OBD-II trouble codes. It features a React frontend, a Flask backend serving a fine-tuned T5 model, and a custom dataset for specialized vehicle diagnostics.

## Features
* **AI-Powered Diagnostics:** Answers queries about car symptoms and error codes.
* **Intuitive UI:** Responsive chat interface with a welcome screen.
* **Dark Mode:** User-selectable dark/light mode.
* **Modular Architecture:** Clear separation of frontend and backend components.

## Project Structure
```

vehicle-diagnostics-chatbot/
├── backend/
│   ├── models/
│   │   └── vehicle\_chatbot\_model\_base/ \# Fine-tuned T5 model files
│   ├── app.py                      \# Flask API for model serving
│   ├── requirements.txt            \# Backend Python dependencies
│   └── (other Flask related files)
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js                  \# Main React component, handles routing
│   │   ├── Chatbot.js              \# Core chatbot interface component
│   │   └── Welcome.js              \# Welcome page component
│   │   └── index.js                \# React entry point
│   │   └── index.css               \# Global styles (Tailwind CSS)
│   ├── package.json                \# Frontend Node.js dependencies
│   └── (other React related files)
├── data/
│   ├── 01\_raw\_vehicle\_data.csv     \# Initial raw dataset
│   └── 02\_augmented\_vehicle\_data.csv \# Augmented dataset (generated)
├── scripts/
│   ├── 02\_augment\_and\_prepare\_data.py \# Script to augment raw data
│   └── 03\_train\_chatbot\_model.py    \# Script to fine-tune T5 model
└── README.md                       \# This file

````

## Setup and Execution Guide
Follow these steps to set up and run the Vehicle Diagnostics Chatbot.

### **Step 1: Clone the Repository**
```bash
git clone <https://github.com/LokeshDasarla/Vehicle-Diagnostics-Bot>
cd vehicle-diagnostics-bot
````

### **Step 2: Data Preparation & Model Training**

1.  **Create Python Virtual Environment (Optional but Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows: .\venv\Scripts\activate
    ```

2.  **Install Python Dependencies:**

    ```bash
    pip install pandas transformers torch scikit-learn
    ```

3.  **Augment Dataset:**

      * This script takes `data/01_raw_vehicle_data.csv` and generates more training examples.

    <!-- end list -->

    ```bash
    python scripts/02_augment_and_prepare_data.py
    ```

      * This will create `data/02_augmented_vehicle_data.csv`.

4.  **Train the T5 Model:**

      * This script fine-tunes the T5 model on the augmented data. This step can take a significant amount of time, especially without a GPU.

    <!-- end list -->

    ```bash
    python scripts/03_train_chatbot_model.py
    ```

      * The trained model will be saved in `vehicle_chatbot_model_base` in the root directory.

### **Step 3: Backend Setup & Execution**

1.  **Move Trained Model:**

      * Move the `vehicle_chatbot_model_base` folder (created in Step 2.4) into the `backend/models/` directory.

    <!-- end list -->

    ```bash
    mv vehicle_chatbot_model_base backend/models/ # On Windows: move vehicle_chatbot_model_base backend\models\
    ```

2.  **Navigate to Backend:**

    ```bash
    cd backend
    ```

3.  **Install Backend Python Dependencies:**

      * If you created a virtual environment in Step 2.1, activate it first.

    <!-- end list -->

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask Backend Server:**

    ```bash
    python app.py
    ```

      * The server should start and be accessible at `http://127.0.0.1:5000`. Keep this terminal open and running.

### **Step 4: Frontend Setup & Execution**

1.  **Open New Terminal & Navigate to Frontend:**

    ```bash
    # If you are in the 'backend' directory
    cd ../frontend
    # If you are in the root directory 'vehicle-diagnostics-chatbot'
    cd frontend
    ```

2.  **Install Node.js Dependencies:**

    ```bash
    npm install
    ```

3.  **Run the React Frontend Application:**

    ```bash
    npm start
    ```

      * This will open the chatbot application in your web browser (usually `http://localhost:3000`).

## Usage

1.  Access the application via your web browser (`http://localhost:3000` by default).
2.  You will first see the Welcome Page. Click "Access the Chatbot" to proceed.
3.  Type your vehicle-related questions or OBD-II codes into the input field.
4.  The chatbot will provide diagnostic information and guidance.
5.  Use the dark/light mode toggle in the header for preferred viewing.

## Acknowledgements

  * Built with React, Flask, and Hugging Face Transformers.
  * Powered by a fine-tuned T5 model.

<!-- end list -->

```

---
```
