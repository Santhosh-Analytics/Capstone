# YouTube Data Harvesting and Warehousing
This project focuses on harvesting data from YouTube and storing it in a data warehouse. It utilizes tools like SQL, MongoDB, and Streamlit for creating an interactive platform to view and manage the harvested YouTube data.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

In this project, we harvest data from YouTube using the YouTube API. The harvested data includes channel, playlist information, video details, and related statistics. This data is then stored and managed using SQL databases and MongoDB. Streamlit is used to create a user-friendly interface for interacting with the data.


## Features

- Harvest YouTube data, including channel information and video details.
- Store the harvested data in SQL databases and MongoDB.
- Present the data in an interactive and user-friendly way using Streamlit.
- Querying data using MySQL with the predefined questions

## Setup

### Prerequisites

- Python 3.11.0 or higher.
- Jupyter notebook.
- MySQL.
- MongoDB.
- Youtube API key.
- Necessary Python packages (specified in [`requirements.txt`](https://github.com/Santhosh-Analytics/Capstone/blob/main/requirements.txt))

### Installation

To run the YouTube Data Harvesting and Warehousing project, follow these steps:

1. Install Python 3.11.0 or higher: Install the Python programming language on your machine.
2. Install Required Libraries: Install the necessary Python libraries using pip or conda package manager. Required libraries (specified in [`requirements.txt`](https://github.com/Santhosh-Analytics/Capstone/blob/main/requirements.txt)).
3. Set Up Google API: Set up a Google API project and obtain the necessary API credentials for accessing the YouTube API. Click [here](https://developers.google.com/youtube/v3/getting-started) for more guides & references.
4. Configure Database: Set up a MongoDB database and SQL database (MySQL).
5. Configure Application: Update the configuration file or environment variables with the necessary API credentials and database connection details.
6. Run the Application: Launch the Streamlit application using the command-line interface. Clone this repository in your local machine. Open terminal /cmd and navigate to the directory and run this command 'streamlit run Main_mod.py'.

## Usage

