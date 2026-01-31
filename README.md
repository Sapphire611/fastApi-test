# FastAPI Scaffold

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Database Setup

### MongoDB

Make sure MongoDB is running:
```bash
# Windows: Check if MongoDB service is running
# Or start manually: mongod
```

### Initialize Users

Run the initialization script to create default users:
```bash
# Initialize with default users
python scripts/init_users.py

# Create a new user
python scripts/init_users.py create <username> <email> <password> [type]
```

Examples:
```bash
# Create admin user
python scripts/init_users.py create admin admin@test.com admin123 admin

# Create regular user
python scripts/init_users.py create testuser test@example.com 123456 user
```

## Testing

Run tests with pytest:
```bash
pytest
```

## VS Code Setup

### Enable Go to Definition (Ctrl+Click)

If Ctrl+Click is not working to jump to definitions:

1. **Install Python Extension**
   - Press `Ctrl+Shift+X` to open Extensions
   - Search for "Python"
   - Install the official Python extension by Microsoft

2. **Select Python Interpreter**
   - Press `Ctrl+Shift+P`
   - Type and select: `Python: Select Interpreter`
   - Choose: `./venv/Scripts/python.exe`

3. **Wait for Pylance to Index**
   - Look for "⚡Pylance: Ready" in the bottom right corner
   - Pylance needs to index your codebase first

4. **Reload Window (if needed)**
   - Press `Ctrl+Shift+P`
   - Type: `Developer: Reload Window`
