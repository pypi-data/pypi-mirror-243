# Simple Config Handler
config_handler is a python module designed to manage loading and updating config files inside of a program. 
capable of a main config and a user config each simultaneously using json files, it makes it easy to locate configs for 
your programs every time.
# How to find config files!
## Config Storage Location in Windows
### General Config File
```commandline
C:/Users/$USER/APPDATA/Local/<your program name>/base-config.json
```
### User Config
```commandline
C:/Users/$USER/APPDATA/Local/<your program name>/user-config/<user>-config.json
```
## Config Storage Location in Mac
### General Config File
```shell
/Users/$USER/Library/Application Support/<your program name>/base-config.json
```
### User Config
```shell
/Users/$USER/Library/Application Support/<your program name>/user-config/<user>-config.json
```
## Config Storage Location in Linux
### General Config File
```shell
/Users/$USER/.config/<your program name>/base-config.json
```
### User Config
```shell
/Users/$USER/.config/<your program name>/user-config/<user>-config.json
```
# Install instructions
Simple! Use Pypi!
```shell
pip3 install simple_config_manager
```
# Usage
Simple!
```python
import simple_config_handler
simple_config_handler.init("Program name")
main_config = simple_config_handler.load_base_config()
# get user info and name
user_data = simple_config_handler.load_user_config(user)
```
