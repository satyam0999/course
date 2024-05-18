from flask import Flask, render_template, request, jsonify
from main import generate_output  
from flask_cors import CORS
from gpt_output import related_courses_gpt
from gpt_jobs import jobSearch


app = Flask(__name__)
CORS(app)




@app.route('/', methods=['GET', 'POST'])
def form():
    print(request,11)
    if request.method == 'POST':

        # form_data = request.form
        form_data= request.get_json()

   
        domain = form_data['domain']
        studylevel = form_data['studyLevel']
        course = form_data.get('course')  
        test_score = form_data.get('test_score') 
        test_type = form_data.get('test_type') 
        

        fixed_question =f"course: {domain} (the user might enter wrongs spelling of courses, so correct it and use it), studylevel: {studylevel},course: {'ALL' if not course else course}. {test_type}: {test_score } display college, course, study level, fees, duration, toefl score, ielts score, college website, scolarship for {test_type} <= {test_score}, use ILIKE in SQL query and dont put any limit , arrange them in descending order of toefl score.  Only generate sql query and nothing else in output."

 
        results_from_main = generate_output(fixed_question)
        print(results_from_main)
        return jsonify(results_from_main)
        
    return render_template('index.html')



@app.route('/related-courses', methods=['GET', 'POST'])
def related_courses():
    print(request,54)
    if request.method == 'POST':
        
        form_data = request.get_json()
        print(form_data,50)

        domain = form_data['domain']
        studylevel = form_data['studyLevel']
        course = form_data.get('degree')  
        toefl_score = form_data.get('toefl_score')  
        ielts_score = form_data.get('ielts_score')  

            
        data = related_courses_gpt(domain)
        print(data,60)

            
        question = f"course: {data}, studylevel: {studylevel}, toefl_score: {toefl_score if toefl_score else '120'}, ielts_score: {ielts_score if ielts_score else '9'} display college, course, study level, fees, duration, toefl score, ielts score, college website, scholarship for TOEFL score <= {toefl_score} and IELTS score <= {ielts_score}, use ILIKE in SQL query and dont put any limit , arrange them in descending order of toefl score. Use OR in query while searching for courses. Only generate sql query and nothing else in output."

           
        results_from_related = generate_output(question)
        print(results_from_related)
        return jsonify(results_from_related)
      
    return jsonify({"error": "Method not allowed"}), 405  


@app.route('/jobs', methods=['GET', 'POST'])
def jobsAndPay():
    print(request,94)
    if request.method == 'POST':
       
        job_data = request.get_json()
        print(job_data,50)


        university= job_data['university']
        course= job_data['course']
        

            
        data = jobSearch(course, university)
        print(data,60)

        return jsonify(data)

    return jsonify({"error": "Method not allowed"}), 405  



if __name__ == '__main__':
    app.run(debug=True) 
