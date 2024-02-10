# COUNTER-Release-5.1
Group Project CS-4820
This project uses the SUSHI API to request usage reports from library vendors. The JSON data received is used to generate TSV reports that follow the COUNTER 5 standards.
The project is written with Python 3.11. The PyQt GUI framework is used to create a user friendly (hopefully) GUI.

## Developer Contact Info - original developers (Counter 5.0)
- Adam McGuigan apmcguigan@upei.ca
- Chandler Acorn cjacorn@upei.ca
- Samuel Esan sesan@upei.ca
- Urvesh Boodhun uboodhun@upei.ca
- Ziheng Huang Zihhuang@upei.ca

## Developer Contact Info - Student Project Developers (Counter 5.1)
- Karan Goel karan1611goel@gmail.com 
- Shubham Kaura gotoshubham@gmail.com
- Vishav Pratap Chauhan vishurana7479@gmail.com
- Abhimanyu Rana Abhimanyu27882rana@gmail.com
- Anushri Garg aanushri@upei.ca
- Manan Mutereja mmutreja@upei.ca
- Boyu Wu bwu7676@upei.ca

## Future developer contact info
- Melissa Belvadi, mbelvadi@upei.ca

## Download Project 
https://github.com/shubhamkaura04/COUNTER-Release-5.1.git

## Developer Documentation

## How to use pyinstaller for executables
https://github.com/CS-4820-Library-Project/COUNTER-5-Report-Tool/blob/master/docs/pyinstaller-how-to.md

## Setup Instructions (Windows)

## Setup Instruction (MacOS)

### Download the project from Github
- Close and re-open command prompt
- type cd
- Open the location you downloaded the project to and drag the folder into the command prompt window
- Your command prompt window should now show "C:\Users\NAME>cd C:\Users\NAME\DOWNLOAD_LOCATION
- Hit ENTER
- type: pip install -r requirements.txt
- This installs all the neccessary packages to run the project.

### Run the project
- Type: python maindriver.py
- A User-Interface window should open with the project working
- To run the project from now on, you only need to double click or right click and open MainDriver.py and the project should open

## Developer Setup (using Anaconda, Pycharm, Visual Studio Code)
- Download and install Anaconda: https://www.anaconda.com/distribution/#download-section
- Download and install PyCharm: https://www.jetbrains.com/pycharm/download/
- Download and install Visual Studio Code: https://code.visualstudio.com/ 

### Using Anaconda
- Launch Anaconda Navigator (Anaconda GUI)
- Go to Environments on the left pane
- Search for and ensure that pyqt and requests packages are installed

### Using PyCharm
- Download and open the project using PyCharm
- Go to File->Settings
- On the left pane, select Project->Project Interpreter
- Click the cog wheel on the right of the project interpreter drop down, click add
- Choose Existing environment and set the location to anaconda_install_location/python.exe, OK, OK
- Allow the IDE to complete set up then launch the program from MainDriver.py. There should be a play icon next to the line "if __name__ == "__main__":"
- We Good To Go!
Test