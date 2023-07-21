from app import app

# In Production block the bellow 2 lines code.
# The bellow 2 lines is for run in development enviroment & python3 init.py
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
