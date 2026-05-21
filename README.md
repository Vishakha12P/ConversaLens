# ConversaLens

ConversaLens is a WhatsApp Chat Analysis and Intelligence System developed using Python and Streamlit. The application processes exported WhatsApp chat files and provides meaningful insights through statistical analysis, visualizations, and activity tracking.

The project is designed to transform raw chat data into an interactive analytical dashboard that helps users understand communication patterns, user engagement, activity trends, emoji usage, and overall chat behavior.

---

## Features

### Chat Statistics
- Total messages
- Total words
- Media shared count
- Links shared count

### Timeline Analysis
- Monthly timeline
- Daily timeline
- Activity trends over time

### User Analysis
- Most active users
- Individual participant analysis
- User-wise message contribution

### Text Analysis
- Word frequency analysis
- Word cloud generation
- Most common words

### Emoji Analysis
- Most frequently used emojis
- Emoji distribution visualization

### Activity Analysis
- Weekly activity map
- Monthly activity map
- Heatmap visualization for chat activity

### Interactive Dashboard
- User selection support
- Dynamic visualizations
- Streamlit-based responsive UI

---

## Tech Stack

### Programming Language
- Python

### Libraries and Frameworks
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Seaborn
- WordCloud
- Emoji
- URLExtract

### Concepts Used
- Data preprocessing
- Regular expressions
- Data visualization
- Natural Language Processing basics
- Exploratory Data Analysis (EDA)

---

## Project Structure

```bash
ConversaLens/
│
├── app.py
├── helper.py
├── preprocessor.py
├── stop_hinglish.txt
├── requirements.txt
├── README.md
├── .gitignore
│
└── assets/
```

---

## How It Works

1. User exports WhatsApp chat as a `.txt` file.
2. The file is uploaded into the Streamlit application.
3. The preprocessing pipeline extracts:
   - Dates
   - Time
   - Users
   - Messages
4. The processed data is analyzed using Pandas.
5. Visual insights and statistics are generated dynamically.

---

## Installation and Setup

### Clone the Repository

```bash
git clone https://github.com/Vishakha12P/ConversaLens.git
```

### Navigate to Project Directory

```bash
cd ConversaLens
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### macOS/Linux

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
streamlit run app.py
```

After running the command, the application will start locally in your browser.

---

## Input Format

The application supports exported WhatsApp chat files in `.txt` format.

### Export Chat Steps
1. Open WhatsApp
2. Open any chat
3. Click on:
   - More Options
   - Export Chat
4. Export without media
5. Upload the `.txt` file into the application

---

## Deployment

- streamlit community cloud : https://vishakha12p-conversalens-app-fkllge.streamlit.app/

---

## Future Enhancements

- AI-based sentiment analysis
- Chat summarization
- Toxicity detection
- PDF report generation
- Multi-language support
- Deployment with authentication
- Real-time analytics

---

## Challenges Solved

- Handling inconsistent WhatsApp chat formats
- Regex-based message parsing
- Cleaning noisy chat data
- User-wise segmentation
- Dynamic visualization generation

---

## Learning Outcomes

This project helped in understanding:
- Real-world data preprocessing
- Streamlit application development
- Data visualization techniques
- Regex handling
- Analytical dashboard creation
- End-to-end project structuring

---

## Author

Vishakha Rajak

GitHub: https://github.com/Vishakha12P
