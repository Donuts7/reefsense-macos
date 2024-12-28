# Coral Analysis Tool

A GUI application for analyzing coral coverage in images.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Place your model files in the `models` directory:
   - `models/hc.pt` for hard coral detection
   - `models/groups.pt` for coral groups detection

## Running the Application

Simply run:
```bash
python main.py
```

## Usage

1. Select the model type (Hard Coral or Groups)
2. Choose the folder containing your images
3. (Optional) Select a labels folder for ground truth comparison
4. (Optional) Set an image limit
5. Click "Analyze" to process the images

Results will be displayed in the application window.