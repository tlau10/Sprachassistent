# Sprachassistent

# TODO
clone repository

install python 3.7.3

install python packages
pip install pip_install.txt

## Speech-to-text
create virtualenv for deepspeech
python3 -m venv <path>

activate virtualenv
source /bin/activate

inside of the virtualenv:
pip install deepspeech
apt install sox

run deepspeech
deepspeech --model model.pbmm --scorer de-aashishag-1-prune-kenlm.scorer  --audio my_audio_file.wav
deepspeech --model deepspeech-0.9.3-models.pbmm --scorer deepspeech-0.9.3-models.scorer --audio my_audio_file.wav
