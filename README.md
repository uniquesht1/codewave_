# CodeWave LegalSathi

CodeWave LegalSathi is an AI-powered chatbot designed to improve access to justice in Nepal. This chatbot provides users with legal document explanations, basic legal advice, and assistance in understanding their rights. It's built with modern web technologies and uses advanced machine learning models to generate accurate legal responses.

<a href="https://legalsathi.netlify.app/" target="_blank">DEMO Site</a>

<a href="https://www.youtube.com/watch?v=d1sSLV4-Mns" target="_blank">DEMO Video</a>


## Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Legal Document Explanation**: Simplifies legal terms and documents into easy-to-understand language.
- **Basic Legal Advice**: Offers foundational legal guidance for common legal issues.
- **Know Your Rights**: Educates users on their basic legal rights.
- **Document Routing**: Assists users in accessing the required legal documents or forms.
- **Attorney Referrals**: Connects users to legal professionals for deeper legal guidance.

## Technology Stack
- **Frontend**: React.js
    - Provides a dynamic user interface for interacting with the chatbot.
- **Backend**: FastAPI (Python)
    - Handles the chatbot logic and communication between the AI model and frontend.
- **AI/ML**: Langchain and Meta Llama 3 70B (Together.ai API)
    - Utilizes Langchain for chaining legal queries and responses with embeddings.
    - Meta Llama 3 70B model powers the natural language understanding and response generation.
- **Database**: ChromaDB
    - Used for storing and retrieving vector embeddings for fast, relevant legal responses.
  
## Setup and Installation

### Prerequisites
- Python 3.9+
- Node.js & npm

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/uniquesht1/codewave_legalsathi.git
    cd codewave_legalsathi
    ```

2. Set up the backend:
    - Navigate to the backend directory:
      ```bash
      cd backend
      ```
    - Install the required Python packages:
      ```bash
      pip install -r requirements.txt
      ```
    - Set up environment variables:
      Create a `.env` file in the `backend` folder and add the necessary environment variables:
      ```bash
      TOGETHER_AI_API_KEY=your_api_key
      TOGETHER_API_URL=your_URL_key
      ```

3. Set up the frontend:
    - Navigate to the frontend directory:
      ```bash
      cd ../frontend
      ```
    - Install the frontend dependencies:
      ```bash
      npm install
      ```

### Running the Application

1. **Run the Backend**:
    - Start the FastAPI backend server:
      ```bash
      cd backend
      uvicorn main:app --reload
      ```
    - The backend should now be running on `http://127.0.0.1:8000`.

2. **Run the Frontend**:
    - Start the React development server:
      ```bash
      cd ../frontend
      npm start
      ```
    - The frontend should now be accessible at `http://localhost:5173`.

## Usage

Once the application is running, visit the frontend at `http://localhost:5173` and interact with the chatbot. You can ask legal questions, seek advice on rights, or request assistance with legal documentation.

## Contributing

We welcome contributions! Here's how you can help:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-xyz`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-xyz`).
5. Open a Pull Request.

Please ensure all pull requests follow our code style and include relevant tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to reach out if you encounter any issues or want to contribute!
