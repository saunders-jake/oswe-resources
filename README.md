# OSWE Resources
Here is my repo for many of the resources/scripts I used to pass the OffSec Web Expert exam.

### Code
#### `exploit.py`
My skeleton script for writing web exploits with python requests.

**Features**:
- Custom Logging

![image](https://github.com/user-attachments/assets/b089afee-e865-4580-be72-f7f45d1667b9)

- Utility functions
  - `random_string(n)`: generates a random string of `n` length. Useful for when you're testing but need a unique account name, password, etc. on each execution.
  - `cmd(command)`: A shortcut for `subprocess.check_output()` that returns the output of the entered command.
  - `start_listener(port)`: This function allows the user to catch a reverse shell within the exploit script. By starting the listener on another thread, the script can finish execution while still waiting for a callback.

It also has two command line options, `--proxy` and `--debug`:
- `--proxy`: Runs every single request through a proxy.
- `--debug`: `dbg()` statements will only be printed if this flag is set.

#### `callback.py`
This is my custom implemenation of a webserver that can be used to receive callbacks for XSS, CSRF, etc...

By default, the server will run on all interfaces (0.0.0.0) using port 8000 with no extra functionality. In order to have a request be displayed and saved to the `messages` array, a HTTP `GET` or `POST` request with the `msg` parameter is required. 

Here's an example that runs the server and shows you how to access the received text:
```python
from callback import Callback

server = Callback(port=80)
# Exploit code goes here
server.stop() # Don't forget to stop the server

print('\nReceived messages:')
for message in server.messages:
  print(message)
```
![image](https://github.com/user-attachments/assets/e6f209bf-4854-41cd-9f80-bee74591ab65)

If you instantiate it like `Callback(port=80, headers=True, serve=True)`, it will print out all of the HTTP headers from each request, and serve files from the cwd of the script.
### Other resources
By no means an extensive list, but a few things that I found helpful

- [Exploit Writing for OSWE](https://github.com/rizemon/exploit-writing-for-oswe): This is an amazing resource that breaks down all of the important concepts for the python `requests` library.
- [cURL Converter](https://curlconverter.com/): When you have a request in burpsuite, you can right click it and `copy as a curl command`. Then, put it into this website, and it spits out the python requests equivilent. 
- [Portswigger XSS Cheat Sheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet): An extensive list of XSS payloads.
- [Java Runtime Exec Command Generator](https://ares-x.com/tools/runtime-exec/): It can be painful to make your reverse shell payload work with Runtime exec, this website makes it a breeze.

**Extra reading/videos:**

xxe:
- https://www.youtube.com/watch?v=0fdpFQXWVu4
- https://www.youtube.com/watch?v=qOt2HrKTyEM

csrf:
- https://www.youtube.com/watch?v=eWEgUcHPle0

postgres:
- https://pulsesecurity.co.nz/articles/postgres-sqli





