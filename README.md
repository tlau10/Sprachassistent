# Sprachassistent

## General info
This project uses python3.7.<br/>

## Setup on x86
Make sure python3.7 and the newest python3-pip version is installed.

### Create virtual python environment and activate it
```
$ python3.7 -m venv pyvenv3.7 
$ source pyvenv3.7/bin/activate
```

### Clone Repository and run pip install
``` 
$ clone https://github.com/tlau10/voice_assistant_katja.git
$ cd /voice_assistant_katja
$ python -m pip install -r pip_requirements.txt
``` 

### Start the voice assistant
``` 
$ python voice_assistant_main.py
``` 

## Setup on Arm64

### Install dependencies
```
$ sudo apt-get install libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev portaudio19-dev python-all-dev git git-lfs
```

### Install Python3.7 and pip
```
$ wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz 
$ tar xf Python-3.7.0.tar.xz 
$ cd Python-3.7.0 && ./configure && make && make altinstall 
$ sudo apt install python3-pip
$ python3.7 –m pip install -–upgrade pip
```

### Get Rust for SnipsNLU
```
$ curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh 
```

### Clone Repository and run pip install
``` 
$ git clone https://github.com/tlau10/voice_assistant_katja.git
$ cd /voice_assistant_katja
$ git lfs pull
$ python3.7 -m pip install -r pip_requirements.txt
``` 

### Install Deepspeech from wheel
``` 
$ wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-cp37-cp37m-linux_aarch64.whl 
$ Python3.7 –m pip install deepspeech-0.9.3-cp37-cp37m-linux_aarch64.whl 
``` 

### Install DE language for SnipsNLU
``` 
$ python -m snips_nlu download de
``` 

### Start the voice assistant
``` 
$ cd /voice_assistant_katja
$ python3.7 voice_assistant_main.py
``` 