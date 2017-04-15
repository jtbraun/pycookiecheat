This Dockerfile works -- kind of -- to test
[pycookiecheat](https://github.com/n8henrie/pycookiecheat).

To use it, you can just pretend that Selenium isn't even there, run it with:

```shell_session
$ docker build -t pycookiecheat .
$ docker run -P -it pycookiecheat
# /opt/bin/entry_point.sh
```

Then exit the docker environment while the VNC server is running with `ctrl p`,
`ctrl q` and find the VNC port mapped from 5900 with `docker ps` (or `docker
port`).

On OSX, run the built-in VNC server (`Finder` -> `Go` -> `Connect to
Server...`) and use `vnc://localhost:PORT` with the port number from the
previous step.

The Selenium VNC password is `secret`.

In the screen, right click on the Desktop and run Chrome from the menu (in one
of the top submenus), open <http://html-kit.com/tools/cookietester> and put in
`TestCookie` :: `Just_a_test!` (the values I've used in the pycookiecheat
tests).

Then, `docker atttach` to the container, `ctrl c` to quit the VNC process, and
run `/venv/bin/python -c 'import pycookiecheat;
print(pycookiecheat.chrome_cookies("http://www.html-kit.com",
cookie_file="/root/.config/google-chrome/Default/Cookies"))'` and it should
give you back the test cookie.

Alternatively, while the `entry_point.sh` server is running, open a local
Python session on your Mac and use the port mapped from the Docker container's
`:4444` to use Selenium, and replace `PORT` below with the proper mapped port.

```python
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=/root/.config/google-chrome")

driver = webdriver.Remote("http://localhost:32843/wd/hub",
                          desired_capabilities=options.to_capabilities())
driver.get("http://html-kit.com/tools/cookietester/")

cookie_name = driver.find_element_by_name("cn")
cookie_name.clear()
cookie_name.send_keys("TestCookie")

cookie_value = driver.find_element_by_name("cv")
cookie_value.clear()
cookie_value.send_keys("Just_a_test!")

cookie_value.submit()
driver.quit()
```

This script will take a little while to complete, then afterwards you should be
able to attach to the Docker container, kill the server process, and run the
script as above to get the cookies.
