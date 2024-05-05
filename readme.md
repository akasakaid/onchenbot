# Onchaincoin_bot

Auto tap-tap for onchaincoin_bot telegram.

## Reminder
> I am not responsible for what happens on your account.

## Author note
> 1. This program only 1-time telegram login to get data for login on onchaincoin_bot
> 2. The program is not recommend for new telegram account

## Installation
1. Make sure your machine ha s python and git installed. If not, search on google how to install it.
2. Clone this repository
	```
	git clone https://github.com/akasakaid/onchaincoin_bot.git
	```
3. Move to onchaincoin_bot directory
	```
	cd onchaincoin_bot
	```
4. This is optional step but its recommend to use. Create a virtual environment.
	```
	python -m venv env
	```
5. Install library / module.
	```
	pip install -r requirements.txt
	```
6. Run the program
	```
	python bot.py
	```
## config.json file explanation

| Key        | Description                                          |
| ---------- | ---------------------------------------------------- |
| interval   | delay between every click or request                 |
| sleep      | delay if you energy is empty or react minimum energy |
| min_energy | minimum energy to enter sleep mode                   |