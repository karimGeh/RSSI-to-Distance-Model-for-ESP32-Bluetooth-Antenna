# RSSI to Distance Model for ESP32 Bluetooth Antenna

## Summary

* [An Overview of the Repo](#an-overview-of-the-repo)
  * [Software](#software)
  * [Hardware](#hardware)
  * [The Code](#the-code)
    * [The server]()
    * [ESP32 / Arduino]()
    * [Identification]()
* [How to use this repo]()
  * [Installation]()
  * [Start the server]()
  * [Upload ESP32 code]()
  * [Get the RSSI to Distance Model]()
* [License / Donation]()


In this repository we will try to identify the Bluetooth Antenna model of an **ESP32**.

This model should be able to convert **RSSI** to Distance.

To be able to identify this model we will place a **BLE Tag** in some predefined distances from the **ESP32**, and we'll record 50 **RSSI** readings of each distance.

Some points to clear out before we start:

* The distances Range is **5 cm** to **14 meters** from the **ESP32**
* The experience will be in open space, meaning no obstacles will be placed between the Tag and the **ESP32**
* The distance steps between each iteration and the other will increase as the distance increases

## An Overview of the Repo

A brief explaination of different parts of the experience

### Software

* Python installed (don't know what you doing in your life if you dont have python already installed).
* VSCode 🙃
* Jupyter (or you can simply use the vscode extension)
* The Arduino IDE (or you can simply use the vscode extension)
* Postman to send POST requests to our server (or you can simply use the REST vscode extension)

### Hardware

* ESP32.
* BLE Tag.
* A computer (obviously).

### The Code

#### The server (`./src/server`):

In this experience we will have to code a API/Server that will save the readings comming from the ESP32 and save it to the csv file

End points:

* POST `/save-scan` : To which we will post values of the scans from the ESP32 to be saved in a csv file
* POST `/set-distance` : will be used to set the distance between the antenna and the tag
* POST `/start-recording` : will enable recording, recording will be automatically stopped after receiving 50 readings
* POST `/stop-recording` : will stop recording, without reseting the readings counter to 0
* POST `/reset-counter` : will reset counter to 0.

#### ESP32 / Arduino software (`./src/esp32`):

In this experience we'll use the Arduino IDE to code the ESP32

The code will first connect to the WiFi and start scaning for bluetooth devices, if it founds our BLE Tag, which will be identified with its mac address, the ESP32 will send a POST request to our

http://{server_ip_addr}:5000/save-scan?maxAddress={theTagAddress}&rssi={the_rssi_value}

#### Identification(`./src/model`)

After saving the values to the csv file. we will then load the csv file to a python notebook to perform the following.

* First, a simple visualization of the readings wont be harmful and will give us a sense of what we are dealing with.
* We will take 40 random readings from the data on which we will calculate the model, and keep 10 reading for accuracy evaluation.
* Then we will take the 40 readings corresponding to each distance and calculate its median, the median here is used to not be affected by outliers.
* We will then write some code to get a valid model (explained in the jupyter notebook).
* Finally, We test the our model on the remaining 20% of the data, to get the accuracy of the model.

## How to use this repo

##### Installation

I'm using a virtual env for this project with python 3.8, you can do the same or just take responsibility of your own decisions.

if you want to use a venv and your main installed python version is the 3.8, execute the following commands in the root directory

* Create a virtual env

```powershell
python -m venv .venv
```

* Activate the venv

```powershell
./.venv/Scripts/activate
```

* Install the reuired packages

```powershell
pip install -r ./requirements.txt
```

##### Start the server

You need to activate your venv first, then execute the following command in the root direcotry of the repo

```sh
python ./src/server/main.py
```

Notes:

* The server won't save any readings from your ESP32 unless you send a post request to the start recording endpoint mentionend above.
* Before changing the distance between the antenna and the tag, you need to send  a POST request to the stop recording endpoint mentioned above.
* The reset counter endpoint won't only reset the counter, but also deletes all readings from the csv file that has the currented setted distance value.

##### Upload ESP32 code

Really? you don't know 🙃

* Open Arduino IDE.
* Open the `./src/esp32/esp32.ino` file
* Select the esp32 board under tools>boards>esp32 tab.
* Select the port to which the esp32 is connectd to under tools>ports tabs.
* Hit the Upload button "→" (right arrow icon)

Ohh before you upload! I totally forgot to mention that you need to connect your ESP32 to your computer, I assume you don't know that.

Aaaand you need to set your own WiFi SSID and Password.

Aaaand update the server url with your computer IP address

Aaaand ... hahaha nothing that's all, you can upload now and move to next step.

##### Get the RSSI to DISTANCE model

* Open the jupyter notebook under `./src/model/model.ipynb`.
* Edit what you have to edit in the first cell
* Execute all cells (in order ofc 😒).
* Scroll down
* TARA 🎉🎉 Here is your model, hope you like it.
* You can check the graphs btw because I really liked them.

You will find explaination of the code in the code.

## License

MIT **Free Software, Enjoy!**

You can donate from here: [donation link](https://youtu.be/dQw4w9WgXcQ)
