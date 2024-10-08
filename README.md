
# FlipInClassIA

FlipInClassIA is a project developed as part of an internship for the Computer Science degree program at the University of Salerno, under the supervision of Prof. Fabio Palomba. This project is based on the desire to create a support tool for the flipped classroom methodology, focusing specifically on the in-class phase. The goal is to enhance the interaction between students and teachers through a digital platform that integrates advanced features for lesson management, quizzes, and statistics, thus fostering an innovative learning environment.

The project was developed considering the state-of-the-art analysis of the integration of the flipped classroom with Artificial Intelligence. The following requirements have been implemented to provide comprehensive support for the in-class experience:

- **Programmatic Support for the Teacher**: The tool provides teachers with the means to plan and structure lessons, allowing for a well-organized and executable schedule.

- **Monitoring Learning Progress**: Teachers can visualize the progress of the entire class through a detailed interface, assessing students' content acquisition.

- **Personalized Feedback**: During in-class activities, the tool provides students with immediate and targeted feedback, identifying areas of misunderstanding and suggesting improvements.

- **Ease of Use**: The interface is designed to be intuitive, allowing users to quickly access the main features during lessons.

- **Tracking Participation**: The tool monitors student participation during lessons, evaluating the level of engagement and allowing teachers to intervene if necessary.

- **Privacy Protection**: To ensure maximum confidentiality, teachers can only view the class's overall performance without accessing individual student data.

## Index

- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Main Features](#main-features)
- [Contributions](#contributions)
- [License](#license)

## Introduction

FlipInClassIA is a web platform designed to facilitate interaction between students and teachers in the flipped classroom context. The project focuses on the in-class phase, providing advanced tools for analyzing class progress and actively engaging students. Through this platform, teachers can monitor learning, manage interactive activities such as quizzes and debates, and provide immediate feedback, improving teaching effectiveness and student engagement.

## Project Structure

The project structure is organized as follows:

- **static/**: Contains static files like images, CSS, JavaScript, plugins, and other resources.
  - **dashboardStaticFile/**: Includes CSS files, images, and scripts needed for the dashboard.
  - **indexStaticFile/**: Contains resources for the project's landing page.
  - **fileCaricati/**: Folder for files uploaded within the application.
- **templates/**: Contains HTML templates that define the structure of the various site pages, including:
  - **dashboard.html**: The dashboard page for displaying statistics.
  - **lezioneDocente.html** and **lezioneStudente.html**: Templates for lesson management by the teacher and student.
  - **index.html**: The project's landing page.
- **Database.sql**: SQL file containing the database schema required for the application to function.
- **app.py**: The main application file, managing the backend and interactions with the database.
- **README.md**: Project documentation.

## Requirements

- **Python** (version >= 3.8)
- **Flask**: Web framework for Python.
- **SQLAlchemy**: ORM for database management.
- **Bootstrap**: CSS framework for responsive design.
- **Database**: MySQL or another compatible database.
- **JavaScript**: For interactive features.
- **OpenAI API** (optional): To integrate advanced artificial intelligence functionalities.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/AntonioDG30/FlipInClassIA
   cd FlipInClassIA
   ```

2. **Install Python dependencies**:

   Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**:

   Create a database in MySQL and import the `Database.sql` file to create the necessary tables.

   ```bash
   mysql -u username -p database_name < Database.sql
   ```

4. **Configure environment variables**:

   Create a `.env` file in the project root to specify configuration variables such as database connection and API keys (if used).

5. **Run the application**:

   ```bash
   python app.py
   ```

6. **Access the application**:

   The application will be available at: `http://localhost:5000`.

## Configuration

Ensure the `.env` configuration file includes all necessary information, such as:

```
FLASK_ENV=development
DATABASE_URL=mysql://username:password@localhost/database_name
SECRET_KEY=<your_secret_key>
OPENAI_API_KEY=<your_api_key>
```

## Usage

- Users can access the platform through the login page and view available lessons.
- Teachers can create and manage quizzes, while students can participate in lessons and complete quizzes.
- The dashboard provides aggregate statistics and allows data filtering based on selected dates.

## Main Features

1. **Lesson Management**: Teachers can create, modify, and manage lessons directly within the application.

2. **Quiz Mode**: Students can participate in real-time quizzes with implemented timer and dynamic feedback.

3. **Statistics Dashboard**: Graphical visualization of lesson statistics, with the option to export data.

4. **Student Feedback**: A feedback system for students to evaluate lessons.

5. **Responsive Interface**: Design adaptable to various devices thanks to Bootstrap.

6. **OpenAI Integration**: Advanced artificial intelligence features to improve educational interaction (optional).

## Contributions

Contributions are welcome. Please follow the guidelines described in the `CONTRIBUTING.md` file.

## License

This project is distributed under the MIT license. For more details, see the `LICENSE` file.
