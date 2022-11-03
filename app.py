from flask import Flask,request,render_template,url_for,jsonify
import os
import sqlite3
import dialogflow
from google.api_core.exceptions import InvalidArgument

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'sample-key.json'

DIALOGFLOW_PROJECT_ID = 'sample-glae'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'

app=Flask(__name__)

@app.route('/')
def home():
    
    return render_template('home.html')



@app.route('/predict',methods=['POST'])
def predict():

    if request.method=='POST':
        text_to_be_analyzed=request.form['message']

        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        try:
            response = session_client.detect_intent(session=session, query_input=query_input)
        except InvalidArgument:
            raise
        
        connection=sqlite3.connect("engagedemo.db")
        cursor=connection.cursor()
        '''
        query="select status from engagedemo where awb=101"
        r=cursor.execute(query)
        r=r.fetchall()[0][0]
        '''
        '''
        print("Query text:", response.query_result.query_text)
        print("Detected intent:", response.query_result.intent.display_name)
        print("Detected intent confidence:", response.query_result.intent_detection_confidence)
        print("Fulfillment text:", response.query_result.fulfillment_text)
        '''
        #print("Fulfillment text:", response.query_result.parameters.awb_number)
        #if response.query_result.fulfillment_text !="":
        ''' 
        q="insert into intents values('{n}','{m}')".format(n=text_to_be_analyzed,m=response.query_result.intent.display_name)
        cursor.execute(q)
        connection.commit()
        if response.query_result.intent.display_name=='wismo':
            if response.query_result.fulfillment_text !="":
                
                return render_template('home.html',pre=response.query_result.fulfillment_text)
            else:
                a=str(response.query_result.parameters.fields)
                p=a.split()[-2]
                print(p)
                no=int(float(p))
                try:
                    query="select status from engagedemo where awb={}".format(no)
                    r=cursor.execute(query)
                    r=r.fetchall()[0][0]
                except:
                    r="awb_not_assigned"
                    
                return render_template('home.html',pre="The status of your order is "+r)
                '''
        return render_template('home.html',pre=response.query_result.intent.display_name)
if __name__=='__main__':
    app.run(debug=True)
