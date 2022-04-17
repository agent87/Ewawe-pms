from requests.api import request
import streamlit as st
import time
import requests
import psycopg2
import datetime

conn = psycopg2.connect(database="d7pibsdo79jogi",host="ec2-52-86-25-51.compute-1.amazonaws.com",port=5432,user="cccbiffnldwfkf",password="605444bcd83d702da6e7f56cb2fba0ebb74fb3db14dc5a0c1555bbfa75a357a1")
cur = conn.cursor()


SIDEBAR_OPTION_PROJECT_INFO = "Show Project Info"
SIDEBAR_OPTION_UPLOAD_IMAGE = "Upload Image"
SIDEBAR_OPTION_MEET_TEAM = "Meet the Team"

SIDEBAR_OPTIONS = [SIDEBAR_OPTION_PROJECT_INFO, SIDEBAR_OPTION_UPLOAD_IMAGE, SIDEBAR_OPTION_MEET_TEAM]





#st.cache()
def startup_load():
    one = st.title('Ewawe Parking Managment System V.2.1')
    progress_bar = st.progress(0)
    status_text = st.empty()
    for i in range(100):
        # Update progress bar.
        progress_bar.progress(i + 1)
        # Update status text.
        status_text.text(
        'Starting up the system :{}%'.format(i) )
        # Pretend we're doing some computation that takes time.
        time.sleep(0.1)
    one.empty()
    progress_bar.empty() 
    status_text.empty()


def upload_progress():
    progress_bar = st.progress(0)
    status_text = st.empty()
    for i in range(100):
        # Update progress bar.
        progress_bar.progress(i + 1)
        # Update status text.
        status_text.text(
        'Uploading Files to the System Progress :{}%'.format(i) )
        # Pretend we're doing some computation that takes time.
        time.sleep(0.03)
    progress_bar.empty() 
    status_text.empty()



def alpr(img):
    regions = ['in']
    response = requests.post('https://api.platerecognizer.com/v1/plate-reader/',
                                data=dict(regions=regions),  # Optional
                                files=dict(upload=img),
                                headers={'Authorization': 'Token ec549d56a1930e6da1cbe3dccda9910bcb54072a'})
    resp_json = response.json()
    Plate = str(resp_json['results'][0]['plate']).upper()
    # cur.execute(
    # """INSERT INTO public."ParkingLog" ("Date", "PlateNum", "CheckInMethod", "CheckinTime", "Parked", customer_id_id, entry_gate_id)
    # VALUES('%s', '%s', 'Automatic', %i, true, 2, 2);""".format(str(datetime.datetime.now().date()), Plate, int(time.time())))

    cur.execute("""INSERT INTO public."ParkingLog" ("Date", "PlateNum", "CheckInMethod", "CheckinTime", "Parked", customer_id_id, entry_gate_id) VALUES(%s, %s, 'Automatic', %s, true, 2, 2)""", (str(datetime.datetime.now().date()), Plate, int(time.time())))
    conn.commit()
    #parking_log(Plate)
    Vehicle = str(resp_json['results'][0]['vehicle']['type'])
    st.subheader("Bellow are the results of the prediction")
    st.text("Plate Number: {}".format(Plate))
    st.text('Vehicle Type: {}'.format(Vehicle))


def main():
    st.sidebar.warning('\
        Please upload SINGLE-car images or Videos.')
    st.sidebar.write(" ------ ")
    st.sidebar.title("Navigation")
    AppMode = st.sidebar.selectbox('Please select from the following',SIDEBAR_OPTIONS)

    if AppMode == SIDEBAR_OPTION_PROJECT_INFO:
        st.title("Ewawe Parking Managment System")
        st.text("Welcome to the Ewawe PMS Project Info Page.")
        st.text("Enjoy")
    elif AppMode == SIDEBAR_OPTION_UPLOAD_IMAGE:
        st.title("Upload a Vehicle Entry Image")
        st.info('PRIVACY POLICY: uploaded images are never saved or stored. They are held entirely within memory for prediction \and discarded after the final results are displayed. ')
        f = st.file_uploader("Please Select to Upload an Image", type=['png', 'jpg', 'jpeg'])
        if f is not None:
            img = f.read()
            st.image(img, 'Here is your image')
            st.write('Please wait for the magic to happen! This may take a few seconds.')
            alpr(img)
    
    elif AppMode == SIDEBAR_OPTION_MEET_TEAM:
        st.title("Meet the typing hands behind the system")
        first_column, second_column, third_column= st.beta_columns(3)
        st.success('Hope you had a great time :)')
        st.write('Please feel free to connect with us on Linkedin!')
        expandar_linkedin = st.beta_expander('Contact Information')
        expandar_linkedin.write('Arnaud: https://www.linkedin.com/in/arnaud-kayonga-5910a813a/')




main()