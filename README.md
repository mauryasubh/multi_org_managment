# Multi-Organizational Management System with Role-Based Access Control

This project is a Django-based web application designed to manage multiple organizations with role-based access control. It enables the main organization to create and manage sub-organizations, while each sub-organization can independently manage its users and roles.

---

## Features
1. **Main Organization Management**:
   - Superuser can create, update, and delete sub-organizations.
2. **Sub-Organization Management**:
   - Admins can manage users and assign roles like Admin, Editor, and Viewer.
3. **Custom User Model**:
   - Each user belongs to a specific organization and has a defined role.
4. **Role-Based Access**:
   - Secure role assignment and restricted user access based on organization membership.

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment setup (optional but recommended)
- Git

### Steps to Set Up Locally

1. **Clone the Repository**:
   - Open a terminal and run the following commands to clone the repository:
     ```bash
     git clone <repository-url>
     cd <repository-folder>
     ```

2. **Create a Virtual Environment**:
   - Run the following commands to create and activate a virtual environment:
     ```bash
     python -m venv env
     source env/bin/activate       # For Linux/macOS
     env\Scripts\activate          # For Windows
     ```

3. **Install Dependencies**:
   - Install all required Python packages by running:
     ```bash
     pip install -r requirements.txt
     ```

4. **Apply Migrations**:
   - Set up the database by applying migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

5. **Create Superusers**:
   - Create the Admin Superuser:
   - use any password and username 
   
     ```bash
     python manage.py createsuperuser
     ```
     -to test directlty use below credentials
     Use the following credentials when prompted:
     - Username: `admin`
     - Password: `admin`
   - Create the Test Sub-Organization Superuser:
     ```bash
     python manage.py createsuperuser
     ```
     Use the following credentials when prompted:
     - Username: `test2`
     - Password: `subh@88790`

6. **Run the Development Server**:
   - Start the Django development server by running:
     ```bash
     python manage.py runserver
     ```

7. **Access the Application**:
   - Open your browser and navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
   - Login using one of the superuser credentials above.

---

## Testing the Application
1. **Admin Access**:
   - Login using `admin:admin`.
   - Create, update, and delete sub-organizations.
   - View the list of all users and their roles in the system.

2. **Sub-Organization Access**:
   - Login using `test2:subh@88790`.
   - Manage users within the sub-organization.
   - Assign roles to users, restricting actions to your sub-organization.

3. **Role Assignment**:
   - Verify that roles like Admin, Editor, and Viewer affect user permissions appropriately.

---

## Notes
- Default credentials are for testing purposes only. Update passwords and roles as needed.
- For additional configuration, refer to Django's [official documentation](https://docs.djangoproject.com/).

---

## License
This project is licensed under the MIT License.
