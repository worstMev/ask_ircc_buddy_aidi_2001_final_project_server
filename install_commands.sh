#!/bin/bash

#ubuntu commands
echo "INFO : update and installing python and libsm6 libxext6 installed" &&
sudo apt update && 
sudo apt install python3-pip &&
echo "INFO : create virtual environment python" &&
sudo apt install python3.12-venv &&
python3 -m venv myvenv &&
echo "INFO : pip install fastapi and  uvicorn" &&
./myvenv/bin/pip install "fastapi[standard]" uvicorn &&
./myvenv/bin/pip install -qU crewai &&
./myvenv/bin/pip install -qU crewai-tools &&
./myvenv/bin/pip install -qU "crewai[tools]" &&
./myvenv/bin/pip install -qU firecrawl-py &&
