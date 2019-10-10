#!/usr/bin/env python
from __future__ import print_function	# print() as a function not as a statement
import string	# Common string operations
import random	# Generate pseudo-random numbers
import subprocess	# Spawn new processes, connect to their input/output/error pipes, and obtain their return codes
from flask import Flask, jsonify, make_response

# Here we build the string of allowed characters
# as "a-z" + "A-Z" + "0-9" + "special characters"
alphaChars = string.ascii_letters + string.digits
allChars = string.ascii_letters + string.digits + '!@#$%^&*()'
minLen = 3
Lchar = ['Guybrush Threepwood', 'Elaine Marley', 'LeChuck', 'Stan', 'Voodoo Lady', 'Herman Toothrot', 'Meathook', 'Carla', 'Otis', 'Wally B. Feed', 'Rapp Scallion', 'Rum Rogers Sr.', 'Men of Low Moral Fiber', 'Murray']

# Actual random password generator, takes two arguments:
# lenN = password length
# alpha = if eq 'True' password will contain alphanumeric characters only or special ones as well
def generate_password(lenN, alpha):
	# We first build a "mask", whose length is the same as the password itself,
	# to hold the "position" of at least one Capital letter and one Numeric character
	pwMask = ['-'] * lenN
	# reqChar is a non-repeating list of "positions" within the boundaries of the password length
	reqChar = random.sample(range(lenN),2)
	pwMask[reqChar[0]] = 'C'
	pwMask[reqChar[1]] = 'N'

	result = ''

	if alpha: # switch "-a" or "--alpha" present
		pwChars = alphaChars
	else: # switch "-a" or "--alpha" not present
		pwChars = allChars

	for ij in range(lenN): # add one password character for each "position" in list pwMask
		if pwMask[ij] == 'C': # force Capital letter
			result += random.choice(string.ascii_uppercase)
		elif pwMask[ij] == 'N': # force Numeric character
			result += random.choice(string.digits)
		else: # truly random character
			result += random.choice(pwChars)

	return result

app = Flask(__name__)

@app.route('/tokenizer/api/v1.0/<int:tk_len>', methods=['GET'])
def get_token(tk_len):
    if tk_len <= minLen: return jsonify(error = 'Length too short')
    if tk_len > minLen:
      yourfriend = random.sample(Lchar, 1)[0]
      msg1 = string.split(subprocess.check_output(["fortune"]), '\n')[2]
#      tokenL = print(msg1) | sha256sum | base64 | head -c 64
      tokenS = generate_password(tk_len, False)
      return jsonify(
		Operator = yourfriend,
		Lame_excuse = msg1,
		Unpronounceable_ticket_number = tokenS,
#		Magic_spell = tokenL,
#		Length = tk_len,
		)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
