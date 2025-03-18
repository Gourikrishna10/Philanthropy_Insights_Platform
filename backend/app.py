from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Philanthropy Insights Platform"

if __name__ == '__main__':
    app.run(debug=True)
