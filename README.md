# FaceBlur Django Project

FaceBlur Django Project is a web application that allows users to manually blur faces in photos. The application is built using Django and provides various features including a gallery to view the uploaded images and the ability to download the processed images in a zip archive.

## Features

- **Manual Face Blurring**: Users can manually blur faces in uploaded photos.
- **Gallery Display**: View all uploaded images in a user-friendly gallery.
- **Download Processed Images**: After blurring faces, users can download the processed images in a zip archive.

## Installation

### Prerequisites

- Python 3.x
- Django

### Installation Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/ruslan-kornich/faces_blure_django.git
    ```
2. Navigate to the project directory:
    ```bash
    cd faces_blure_django
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Setup

1. Run migrations to set up the database:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
2. Start the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

1. Access the web application by visiting `http://127.0.0.1:8000/` in your web browser.
2. Register or log in to your account.
3. Upload a zip file containing the images you want to process.
4. Open the gallery to view the uploaded images.
5. Click on an image to manually blur faces.
6. After blurring faces, download the processed images by clicking the "Download" button.


