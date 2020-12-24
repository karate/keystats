A simple python program that generates keypress statistics.

It reads every keypress from the keyboard, and calculates the total count per key.

It saves the data in a JSON file when the user kills the program (Ctrl-C or `kill` command), and every 1000 keypresses (just to be sure)

# Usage
```bash
# Use virtualenv (optional)
$ virtualenv venv
$ source venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt

# Run keystats
$ python keystats.py
# OR
$ python keystats.py output.json
```
