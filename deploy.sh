#!/bin/bash

hugo

git add .

git commit -m "Updates"

git push

python -m pip install --upgrade pip
pip install flask yfinance pandas numpy matplotlib Figure
