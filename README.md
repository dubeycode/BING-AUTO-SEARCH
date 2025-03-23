# Flask Blogging App

## Introduction
This is a **Flask-based Blogging Application** where users can create, edit, and delete blog posts. The application uses **Flask** as the backend framework and **MySQL** as the database.

## Features
- 📝 Create, Read, Update, and Delete (CRUD) blog posts
- 🔐 User authentication (Login/Signup)
- 📂 Image upload support
- 📊 Dashboard for managing posts
- 💬 Comment section for posts
- 🌎 SEO-friendly URLs

## Installation

### Prerequisites
Make sure you have the following installed:
- Python (3.7 or later)
- Flask
- MySQL (running on XAMPP, Port: 8080)
- Virtual environment (optional but recommended)

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/dubeycode/python-flask-blog.git
   cd python-flask-blog
   ```

2. **Create Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Database**
   - Start XAMPP and ensure MySQL is running.
   - Open MySQL and create a new database:
     ```sql
     CREATE DATABASE flask_blog;
     ```
   - Update the `config.py` file with your database credentials.

5. **Run Migrations**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the Application**
   ```bash
   flask run
   ```
   The app will be live at **http://127.0.0.1:5000** 🚀

## Folder Structure
```
flask_blog/
│-- app/
│   │-- static/  # CSS, JS, Images
│   │-- templates/  # HTML Templates
│   │-- routes.py  # Application Routes
│   │-- models.py  # Database Models
│   │-- forms.py  # Flask Forms
│-- config.py  # Configuration Settings
│-- requirements.txt  # Dependencies
│-- run.py  # Main Entry Point
```

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make changes and commit (`git commit -m "Added new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License
This project is licensed under the **MIT License**.

## Contact
📧 Email: dubeysatyam3635@gmail.com
🐙 GitHub: [dubeycode](https://github.com/dubeycode)

