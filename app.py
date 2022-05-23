from flask import Flask,render_template,url_for,request,redirect, make_response
import random
import json
from time import time
from random import gauss, random
import datetime
import sqlite3
import os
import serial
#import time


currentdirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])

def main():
    return render_template('index_web.html')

@app.route('/data', methods=["GET", "POST"])

def data():
   #Initialire SQLite3 DH connection and cursor object
   conn = sqlite3.connect('store.db')
   cursor = conn.cursor()
	
   #receive data from arduino_ uart
   ser = serial.Serial(
   port = '/dev/ttyAMA0',
   baudrate = 9600,
   parity = serial.PARITY_NONE,
   stopbits = serial.STOPBITS_ONE,
   bytesize = serial.EIGHTBITS,
   timeout = 2	
   )

   while True:
      s = ser.readline()
      data = s.decode()			# decode s
      data = data.rstrip()		# cut "\r\n" at last of string
      temp,humi,ppm = data.split(',')
      #write data from sensor into sql and save in that
      cursor.execute('''INSERT INTO sensor_update(temp, humi, ppm) VALUES(?,?,?)''',(str(temp),str(humi),str(ppm)))
      conn.commit()
      #lay gia tri dua len web server
   	#lay gia tri nhiet do moi nhat cua cam bien de xuat ve bieu do
      sql_temp = "SELECT temp FROM(SELECT temp FROM sensor_update ORDER BY id DESC)SQ LIMIT 1"
      cursor.execute(sql_temp)
      Temperature = float(cursor.fetchall()[0][0])

      #lay gia tri do am moi nhat cua cam bien de xuat ve bieu do
      sql_humi = "SELECT humi FROM(SELECT humi FROM sensor_update ORDER BY id DESC)SQ LIMIT 1"
      cursor.execute(sql_humi)
      Humidity = float(cursor.fetchall()[0][0])

      #lay gia tri ppm moi nhat cua cam bien de xuat ve bieu do
      sql_ppm = "SELECT ppm FROM(SELECT ppm FROM sensor_update ORDER BY id DESC)SQ LIMIT 1"
      cursor.execute(sql_ppm)
      Gas = float(cursor.fetchall()[0][0])

      #seconds = time.time()
      #local_time = time.ctime(seconds)
      data = [time()*1000, Temperature, Humidity, Gas]
      print(time)

      response = make_response(json.dumps(data))

      response.content_type = 'application/json'

      return response

if __name__ == "__main__":
    app.run(debug=True)
