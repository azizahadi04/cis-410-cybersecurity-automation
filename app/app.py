from flask import Flask, render_template
import socket
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def dashboard():
    context = {
        "status": "Running",
        "environment": "dev",
        "version": "1.0.0",
        "pipeline_status": "Passing",
        "hostname": socket.gethostname(),
        "vm": "dev-vm",
        "deployed_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "commit": "latest",
        "branch": "main",
        "triggered_by": "deploy-dev.yml"
    }
    return render_template("index.html", **context)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)