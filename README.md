# Shirokobot
Discord bot for manimaniAC server & studying.

## How To Run

First of all, you need MongoDB client installed on your server.

1. Run following commands
```
conda create ./.conda python=3.11.4
conda activate ./.conda
pip install -U -r requirements.txt
```

2. Configure backend app <br>
Change values in ```backend/config.json``` to fit your enviornments.

3. Configure Discord bot app <br>
Make ```constants.txt``` file to fit your enviornments. <br>
the format is:
```
TOKEN=<YOUR DISCORD APP TOKEN>
OWNER_USER_ID=<YOUR USER ID>
BACKEND_HOST=<BACKEND_HOST SET IN config.json>
BACKEND_PORT=<BACKEND_PORT SET IN config.json>
```

4. Run backend app
```
cd backend
python index.py
```

5. Run Discord bot app <br>
run new terminal and 
```
python app.py
```