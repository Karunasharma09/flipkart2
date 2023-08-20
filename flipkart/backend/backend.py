from flask import Flask, request, jsonify
import subprocess
import os
app = Flask(__name__)

@app.route('/api/process_input_data', methods=['POST'])
def execute_script():
    uploaded_file = request.files['file']

    if uploaded_file:
            # Save the uploaded file to a temporary location
            script_directory = os.path.abspath(os.path.dirname(__file__))
            file_path = os.path.join(script_directory, uploaded_file.filename)
            uploaded_file.save(file_path)
            script_directoryy = os.path.abspath(os.path.join(script_directory,'./python'))
            print(script_directoryy)
            # Execute the Python script with the uploaded file as an argument
            try:
                completed_process = subprocess.run(
                    ["python", os.path.join(script_directoryy,"inp_to_json.py")]
                )
                print("Script output:", completed_process.stdout)
                print("Script errors:", completed_process.stderr)
                return jsonify({'message': 'Script executed successfully.'})
            except Exception as e:
                return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
