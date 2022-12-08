# Mision TIC. Cycle 4 - Web development Project

This is a project done as a final test for the Misiontic(2022) course, it consists on an API developed in Python with Fastapi in the Backend and Vuejs in the Front-End


## Clone the repository:
```
git clone git@github.com:gugne/apimintic.git
```


## Set your virtual enviroment:
In the root folder create your virtual enviroment. For this project i used venv
```
python -m venv .env
```

## Active your virtual enviroment:
Now you need to activate the venv you already created.

```
.\env\Scripts\activate
```

## Install all the libraries:
You're now in the virtual enviroment you created, now you need to install all the libraries i used for this project.
```
pip install -r requirements.txt
```

## Run the server:
This is the final stept, just run the server with uvicorn. Remember, every time before running your server you need to activate your virtual enviroment.

```
uvicorn libros:app --reload
```

