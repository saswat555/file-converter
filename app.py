from flask import Flask, render_template, request, send_file, jsonify
import os
import csv
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        emails = request.form.get('emails')
        
        if not emails:
            return render_template('index.html', error='No email addresses provided')
            
        # Create a CSV file from the pasted email addresses
        csv_file = create_csv_from_emails(emails)

        # Process the CSV file and add a dummy name
        output_file = process_csv(csv_file)

        return send_csv(output_file)

    return render_template('index.html')

def create_csv_from_emails(emails):
    csv_file = 'output.csv'
    
    # Split the pasted email addresses into a list
    email_list = [email.strip() for email in emails.split('\n')]
    
    # Write the email addresses to a CSV file
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for email in email_list:
            writer.writerow([email])

    return csv_file

def process_csv(csv_file):
    output_file = 'output.csv'
    dummy_name = 'John Doe'  
    
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        
    # Add a new column 'name' and set the value to the dummy name
    for row in rows:
        if row[0]=='email':
            row.append("name")
        else:
            row.append(dummy_name)

    # Write the modified data to the output file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
    
    return output_file

def send_csv(csv_file):
    # Check if the file exists
    if not os.path.exists(csv_file):
        return jsonify(error="The output CSV file doesn't exist.")
    
    # Send the file for download
    with open(csv_file, 'rb') as f:
        data = io.BytesIO(f.read())
        response = send_file(
            data,
            as_attachment=True,
            download_name='output.csv',
            mimetype='text/csv'
        )
        return response

if __name__ == '__main__':
    app.run(debug=True,port=4000)
