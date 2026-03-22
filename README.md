# DataNarrate - Data Storytelling & Insights Platform

## Project Description
DataNarrate is a full-stack web application built using Flask and Bootstrap.
It allows users to enter raw data and instantly generates:
- Interactive charts (Bar, Line, Pie, Doughnut, Radar)
- Auto-generated data insights (trend, peak, average analysis)
- A gallery of all saved stories
- Data table with percentage share

## Technologies Used

| Layer      | Technology        |
|------------|-------------------|
| Backend    | Python + Flask    |
| Database   | SQLite3           |
| Templates  | Jinja2            |
| Frontend   | HTML5 + Bootstrap 5 |
| JavaScript | jQuery 3.7        |
| Charts     | Chart.js 4.4      |
| Icons      | Bootstrap Icons   |
| Fonts      | Google Fonts      |
| Version Control | Git + GitHub |

## Project Structure
```
datanarrrate/
├── app.py               # Flask routes + insight engine
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
├── templates/
│   ├── base.html        # Master layout
│   ├── index.html       # Home page
│   ├── create.html      # Story creation form
│   ├── result.html      # Chart + insights page
│   └── gallery.html     # All stories gallery
└── static/
    ├── css/style.css    # Custom styles
    └── js/
        ├── main.js      # Shared JavaScript
        └── create.js    # Form validation + live preview
```

## Setup Instructions

### Step 1 - Clone the repository
```
git clone https://github.com/YOUR_USERNAME/datanarrrate.git
cd datanarrrate
```

### Step 2 - Create virtual environment
```
python -m venv venv
venv\Scripts\activate
```

### Step 3 - Install dependencies
```
pip install -r requirements.txt
```

### Step 4 - Run the application
```
python app.py
```

### Step 5 - Open in browser
```
http://127.0.0.1:5000
```

## Features
- Create data stories with Label, Value input
- 5 chart types - Bar, Line, Pie, Doughnut, Radar
- Auto-generated insights (trend, peak, average)
- Live chart preview while typing
- jQuery form validation
- Story gallery with category filter
- SQLite database storage
- Responsive design - works on mobile

## Screenshots

### Home Page
<img width="1915" height="956" alt="image" src="https://github.com/user-attachments/assets/a184e118-be58-4d6f-b340-9fa21bcf1cf1" />


### Create Story
<img width="1913" height="953" alt="image" src="https://github.com/user-attachments/assets/ff83b73e-53a8-4136-893d-d88b1d818b69" />


### Insights Result
<img width="881" height="655" alt="image" src="https://github.com/user-attachments/assets/76f779b3-b38d-4624-bb0c-782f36c1b5e0" />


### Gallery
<img width="1909" height="958" alt="image" src="https://github.com/user-attachments/assets/139b7dcf-bfed-44fc-87bf-424d8f381e3e" />


## Author
- Name: Gogineni Venkata Maha Lakshmi
- Roll No: AV.SC.U4AIE23052
- College: Amrita Vishwa Vidyapeetham
- Subject: Full Stack Development
