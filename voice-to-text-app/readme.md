Voice-to-Text Application
This project is a web-based voice-to-text application that converts speech to text using the Web Speech API and stores the transcriptions in a MongoDB database. It uses Node.js and Express for the backend and HTML/JavaScript for the frontend.
Features

Records speech and converts it to text in real-time using the Web Speech API.
Stores transcriptions in a MongoDB database.
Displays a history of stored transcriptions with timestamps.

Prerequisites
Before setting up the project, ensure you have the following installed:

Node.js:

Download and install the LTS version of Node.js from nodejs.org. As of May 2025, Node.js v20.x is recommended for stability.
Verify installation:node --version
npm --version

Example output: v20.x.x for Node.js and 10.x.x for npm.


MongoDB Community Edition:

Download and install MongoDB Community Server from MongoDB's official site.
During installation, choose the "Complete" setup type and ensure "Install MongoDB Compass" is checked (Compass is a GUI for MongoDB).
Default installation path on Windows: C:\Program Files\MongoDB\Server\<version>.


Google Chrome:

Install Google Chrome, as it fully supports the Web Speech API. Download from google.com/chrome.


Visual Studio Code (VS Code):

Download and install VS Code from code.visualstudio.com.
Optional: Install extensions like "JavaScript (ES6) code snippets" and "MongoDB for VS Code" for a better development experience.



Project Setup in VS Code
Step 1: Create the Project Directory

Create a new folder for your project, e.g., voice-to-text-app, in a location like C:\Users\<YourUsername>\OneDrive\Documents\my codes\.
Open VS Code and select File > Open Folder, then choose your project folder.

Step 2: Add Project Files

Create index.html:

In VS Code, click File > New File and name it index.html.
This file contains the frontend HTML, CSS, and JavaScript:
HTML structure with a "Start Recording" button, sections for current and stored transcriptions.
CSS for styling the interface.
JavaScript to handle speech recognition using the Web Speech API, send transcriptions to the backend, and fetch stored transcriptions.


Save the file.


Create server.js:

Create a new file named server.js (File > New File).
This file contains the backend Node.js/Express server:
Sets up an Express server with CORS and JSON middleware.
Connects to MongoDB using Mongoose.
Defines a schema for transcriptions (text and timestamp).
Includes routes to serve the frontend (/), save transcriptions (/save), and fetch transcriptions (/transcriptions).


Save the file.


Create package.json:

Create a new file named package.json (File > New File).
This file defines the project metadata and dependencies:
Includes fields like name, version, main (set to server.js), and type (set to commonjs).
Lists dependencies: cors, express, mongoose, and object-assign.
Includes a start script to run the server (node server.js).


Save the file.




Note: The exact code for these files is not included here. Refer to the project requirements or source documentation for the implementation details. Alternatively, you can initialize package.json with npm init -y and manually add the required fields and dependencies.

Step 3: Set Up MongoDB

Add MongoDB to System PATH:

Locate the MongoDB bin directory, typically C:\Program Files\MongoDB\Server\<version>\bin.
Add this path to your system’s PATH environment variable:
Right-click on This PC > Properties > Advanced system settings > Environment Variables.
Under "System variables", find Path, click Edit…, and add the MongoDB bin path.
Click OK to save changes.


Verify by opening a new terminal in VS Code and running:mongod --version




Create a Data Directory:

MongoDB requires a data directory to store its database files. Create it at C:\data\db:mkdir C:\data\db


Ensure your user has read/write permissions for this directory (right-click C:\data\db > Properties > Security).


Start the MongoDB Server:

Open a terminal in VS Code (Terminal > New Terminal).
Start MongoDB:mongod


You should see output indicating MongoDB is listening on 127.0.0.1:27017.
Keep this terminal running.


Connect MongoDB Compass:

Open MongoDB Compass (installed with MongoDB).
Click + Add new connection.
Use the connection string: mongodb://localhost:27017.
Click Connect. You should see default databases like admin, config, and local.



Step 4: Fix PowerShell Execution Policy (Windows Only)
If you encounter an error like "running scripts is disabled on this system" when running npm commands in PowerShell:

Open PowerShell as Administrator:

Search for "PowerShell" in the Start menu, right-click, and select Run as administrator.


Change the Execution Policy:

Run:Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned


Type Y and press Enter to confirm.
Verify:Get-ExecutionPolicy

It should return RemoteSigned.


Close the Admin PowerShell Window.


Step 5: Install Dependencies

Open a Terminal in VS Code:

Ensure you’re in the project directory:cd C:\Users\<YourUsername>\OneDrive\Documents\my codes\voice-to-text-app




Install Dependencies:

Run:npm install


This installs cors, express, mongoose, and object-assign as specified in package.json.



Step 6: Run the Application

Start the Node.js Server:

In a new terminal (while mongod is running in another terminal), run:npm start


Or:node server.js


You should see:Server running at http://localhost:3000
Connected to MongoDB




Open the Application:

Open Google Chrome and navigate to http://localhost:3000.
You should see the application interface with a "Start Recording" button.


Test the Application:

Click "Start Recording" and allow microphone access.
Speak clearly (e.g., "Hello, this is a test").
Click "Stop Recording". The transcription should appear in the "Current Transcription" section and then in the "Stored Transcriptions" section.
In MongoDB Compass, refresh the database list and check the voiceToText database and transcriptions collection for the saved data.



Troubleshooting

MongoDB Connection Issues:
Ensure mongod is running and listening on 127.0.0.1:27017.
Verify the connection string in server.js and MongoDB Compass.


PowerShell Script Errors:
Switch to Command Prompt in VS Code (Terminal > New Terminal > Select Default Profile > Command Prompt).


Module Not Found Errors:
Delete node_modules and package-lock.json, then run npm install again.


Speech Recognition Issues:
Use Chrome for the best Web Speech API support.
Check microphone permissions in Chrome.



Optional Enhancements

Run MongoDB as a Service (Windows):
Configure MongoDB to start automatically:"C:\Program Files\MongoDB\Server\<version>\bin\mongod.exe" --config "C:\Program Files\MongoDB\Server\<version>\bin\mongod.cfg" --install
net start MongoDB




Add Features:
Add functionality to delete transcriptions.
Support other languages by changing recognition.lang in index.html (e.g., 'es-ES' for Spanish).



Notes

This project was developed and tested as of May 28, 2025.
If you encounter compatibility issues with Node.js v22.x, consider using Node.js v20.x (LTS) via nvm.

