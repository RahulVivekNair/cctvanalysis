# AI Powered CCTV Analysis

## Installation Instructions

To get started with the project, follow these steps:

1. **Clone the repository:**

```
git clone <repository-url>
```

2. **Set up a virtual environment**

```
cd <repository-directory>
python -m venv venv
```

3. **Activate the virtual environment**

For Windows:

```
.\venv\Scripts\activate
```

For Unix/macOS:

```
source venv/bin/activate
```

4. **Install required packages**

```
pip install -r requirements.txt
```

For GPU support (PyTorch):

```
pip install --pre torch torchvision --index-url https://download.pytorch.org/whl/nightly/cu121
```

For CPU only (PyTorch):

```
pip install torch torchvision
```

Navigate to frontend directory and run Streamlit:

```
cd frontend
streamlit run home.py
```

Navigate to backend directory and run UVicorn with fastapi:

```
cd backend
uvicorn annotater:app --reload
```

Now, you should be all set up and running with the project!
