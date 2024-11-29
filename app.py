from flask import Flask, render_template, request, jsonify
import subprocess
import paramiko
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate("my_key.json")
app=firebase_admin.initialize_app(cred)
db = firestore.client()
coll_ref = db.collection("Logs")
doc_ref = coll_ref.document()



# Flask app setup
app = Flask(__name__)

# Connection details
hostname = "hostname"  
username = "username"             
password = "password"


def run_script(script_path):
    try:
        # Create SSH client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to Raspberry Pi
        print("Connecting to Raspberry Pi...")
        ssh_client.connect(hostname=hostname, username=username, password=password)
        print("Connected!")

        # Run the Python script
        print(f"Executing {script_path}...")
        stdin, stdout, stderr = ssh_client.exec_command(f"python3 {script_path}")
        
        # Fetch the output and errors
        output = stdout.read().decode()
        errors = stderr.read().decode()

        if output:
            print("Output:\n", output)
        if errors:
            print("Errors:\n", errors)
        
        return output, errors

    finally:
        # Close the connection
        ssh_client.close()
        print("Connection closed.")


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/forward')
def forward():
    output, errors = run_script("/home/Yuval/Desktop/scripts/forward.py")
    data = {"Movement": "forward"}
    doc_ref.set(data)
    return render_template("success.html")

@app.route('/backward')
def backward():
    output, errors = run_script("/home/Yuval/Desktop/scripts/backward.py")
    data = {"Movement": "backward"}
    doc_ref.set(data)
    return render_template("success.html")

@app.route('/left')
def left():
    output, errors = run_script("/home/Yuval/Desktop/scripts/left.py")
    data = {"Movement": "left"}
    doc_ref.set(data)
    return render_template("success.html")

@app.route('/right')
def right():
    output, errors = run_script("/home/Yuval/Desktop/scripts/right.py")
    data = {"Movement": "right"}
    doc_ref.set(data)
    return render_template("success.html")

@app.route('/round')
def round():
    output, errors = run_script("/home/Yuval/Desktop/scripts/round.py")
    data = {"Movement": "round"}
    doc_ref.set(data)
    return render_template("success.html")

@app.route('/speed')
def speed():
    output, errors = run_script("/home/Yuval/Desktop/scripts/speed.py")
    data = {"Movement": "speed"}
    doc_ref.set(data)
    return render_template("success.html")

@app.route('/colors')
def colors():
    output, errors = run_script("/home/Yuval/Desktop/scripts/colors.py")
    data = {"Identification": "Colors"}
    doc_ref.set(data)
    return render_template("success.html")

# Route to handle button press and display documents
@app.route('/show-data', methods=['GET'])
def show_data():
    db = firestore.client()
    docs = db.collection('Logs').stream()  # Adjust the collection name
    data = [doc.to_dict() for doc in docs]
    return render_template('data.html', data=data)


if __name__ == "__main__":
    app.run()
