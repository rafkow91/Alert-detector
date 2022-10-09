# Alert-detector
App detects alerts on the screen and save it's message to file.

## Instalation
* Create venv and activate it (*for example in Ubuntu*)
```
python -m venv .venv
source .venv/bin/activate
```

* Install requirements (*for example in Ubuntu*)
```
pip install -r requirements.txt
```

* Create file **.env** with config of FTP connection (*example is in **.env.default***)

* Open in your browser testing website - file **index.html** from folder **web**

* Start script **main.py** (*for example in Ubuntu's terminal*)
```
python main.py
```

## Default settings
In default script reads screen and save reports in 10 loops and save reports on FTP in folders ***/Alarm-detect/{date}/***

* number of repetion you can change in ***main.py*** (*line 8*)
* dir name you can change in ***controllers.py*** (*line 119*)


## To improve in future
I want to add definition of repetations and folder to copy as console parameters.

## A request to you
Thanks for reading this file to end. I want to request to you, because I'm beginner programmer, if you can review my code, please add comment what I can upgrade, imporve or correct.

******
The project created over PyCamp course - the realisation of task is my private sollution.<br>
Other my PyCamp's projects: [click here](https://github.com/rafkow91/PyCamp)
