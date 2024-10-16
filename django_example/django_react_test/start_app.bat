@echo off
:: Start the virtual environment
echo Activating virtual environment...
call env\Scripts\activate

:: Navigate to Django backend and run the server
echo Starting Django server...
cd backend
start cmd /k "python manage.py runserver"

:: Navigate back to the root directory and then start the React frontend
cd ..
echo Starting React frontend...
cd frontend
start cmd /k "npm start"

:: Wait for both servers to start
echo Both Django and React servers are starting. Press any key to close this window.
pause
