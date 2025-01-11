1. Збілдити докер

docker build -t fullstack-web-app .

docker run -d -p 3000:3000 fullstack-web-app


2. Запустити без докеру

  2.1. Створити енвайронмент

  python -m venv venv

  2.2. активувати

  venv\Scripts\activate

  2.3. встановити requirements

  pip install -r requirements.txt

  2.4. запустити

  python main.py