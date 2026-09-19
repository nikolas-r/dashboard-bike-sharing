# Bike Sharing Dashboard ✨

## Setup Environment - Anaconda

conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt

## Setup Environment - Shell/Terminal

mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt

## Run Streamlit App

cd dashboard
streamlit run dashboard.py

Setelah dijalankan, buka browser ke alamat yang muncul di terminal (biasanya http://localhost:8501).

## Dashboard Online

Link dashboard yang sudah di-deploy tersedia di file url.txt, atau langsung di: https://dashboard-bike-sharing-n.streamlit.app/
