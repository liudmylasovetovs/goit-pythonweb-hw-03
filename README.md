Build the Docker Image:
docker build -t fullstack-web-app .

Run the Docker Container:
docker run -d -p 3000:3000 -v $(pwd)/storage:/app/storage fullstack-web-app

-p 3000:3000 maps port 3000 in the container to port 3000 on your host machine.

-v $(pwd)/storage:/app/storage ensures that the data.json file persists outside the container.

Running the App Without Docker
Set Up a Virtual Environment (Optional):

python -m venv venv

Activate the Virtual Environment:

venv\Scripts\activate

Install Required Dependencies:

pip install -r requirements.txt

Run the Application:

python main.py