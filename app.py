from flask import Flask, request, send_file, render_template
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def transform_file(input_path, output_path):
    # Detectar si es CSV o Excel
    if input_path.endswith('.csv'):
        df = pd.read_csv(input_path)
    else:
        df = pd.read_excel(input_path)

    df_melted = df.melt(id_vars=['_time'], var_name='metric', value_name='value')
    df_melted.to_csv(output_path, index=False)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"

        file_ext = file.filename.split('.')[-1]
        if file_ext not in ["csv", "xlsx"]:
            return "Formato no soportado"

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(OUTPUT_FOLDER, "transformed_" + file.filename)

        file.save(file_path)
        transform_file(file_path, output_path)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
