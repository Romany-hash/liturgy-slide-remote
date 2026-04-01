"""
Flask Web Server
Serves phone remote UI and handles slide control commands.
"""

import sys
import os

# Fix path so Python finds our modules and templates
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

import socket
from flask import Flask, render_template, jsonify, request
import ppt_controller


app = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_DIR, "templates")
)

# Track last action for status display
last_action = {"text": "Ready"}


def get_local_ip():
    """Get this PC's local WiFi IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


# ─── Routes ───────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the phone remote control page."""
    return render_template("index.html")


@app.route("/api/next", methods=["POST"])
def api_next():
    """Advance to next slide."""
    ppt_controller.next_slide()
    last_action["text"] = "Next"
    return jsonify({"ok": True, "action": "next"})


@app.route("/api/prev", methods=["POST"])
def api_prev():
    """Go back to previous slide."""
    ppt_controller.prev_slide()
    last_action["text"] = "Previous"
    return jsonify({"ok": True, "action": "prev"})


@app.route("/api/goto", methods=["POST"])
def api_goto():
    """Jump to a specific slide number."""
    data = request.get_json()
    if not data or "slide" not in data:
        return jsonify({"ok": False, "error": "Missing slide number"}), 400

    try:
        slide_num = int(data["slide"])
        if slide_num < 1:
            return jsonify({"ok": False, "error": "Slide must be >= 1"}), 400
    except (ValueError, TypeError):
        return jsonify({"ok": False, "error": "Invalid number"}), 400

    ppt_controller.goto_slide(slide_num)
    last_action["text"] = "Jump to " + str(slide_num)
    return jsonify({"ok": True, "action": "goto", "slide": slide_num})


@app.route("/api/status", methods=["GET"])
def api_status():
    """Return current status for phone display."""
    return jsonify({
        "ok": True,
        "last_action": last_action["text"]
    })


@app.route("/api/slideshow/start", methods=["POST"])
def api_start_slideshow():
    """Start PowerPoint slideshow (F5)."""
    ppt_controller.start_slideshow()
    last_action["text"] = "Slideshow Started"
    return jsonify({"ok": True, "action": "start"})


@app.route("/api/slideshow/end", methods=["POST"])
def api_end_slideshow():
    """End PowerPoint slideshow (Escape)."""
    ppt_controller.end_slideshow()
    last_action["text"] = "Slideshow Ended"
    return jsonify({"ok": True, "action": "end"})


# ─── Startup ──────────────────────────────────────────────

def main():
    ip = get_local_ip()
    port = 5000

    print("")
    print("=" * 50)
    print("  SERVER RUNNING")
    print("=" * 50)
    print("")
    print("  On your phone browser go to:")
    print("")
    print("     http://{}:{}".format(ip, port))
    print("")
    print("=" * 50)
    print("  Press Ctrl+C to stop")
    print("=" * 50)
    print("")

    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()