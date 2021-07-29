import streamlit as st
import time
import requests
import psycopg2
import uuid
import datetime

conn = psycopg2.connect(database="d7pibsdo79jogi",host="ec2-52-86-25-51.compute-1.amazonaws.com",port=5432,user="cccbiffnldwfkf",password="605444bcd83d702da6e7f56cb2fba0ebb74fb3db14dc5a0c1555bbfa75a357a1")
cur = conn.cursor()


SIDEBAR_OPTION_PROJECT_INFO = "Show Project Info"
SIDEBAR_OPTION_DEMO_IMAGE = "Select a Demo Image"
SIDEBAR_OPTION_UPLOAD_IMAGE = "Upload an Image"
SIDEBAR_OPTION_MEET_TEAM = "Meet the Team"

SIDEBAR_OPTIONS = [SIDEBAR_OPTION_PROJECT_INFO, SIDEBAR_OPTION_DEMO_IMAGE, SIDEBAR_OPTION_UPLOAD_IMAGE, SIDEBAR_OPTION_MEET_TEAM]





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



def cost(elapsed):
    #if elapsed is between 0 to 30 then return the cost of the plate
    if elapsed > 0 and elapsed <= 30:
        return 200
    if elapsed > 30 and elapsed <= 60:
        return 300
    if elapsed > 60 and elapsed <= 90:
        return 500
    if elapsed > 90 and elapsed <= 120:
        return 500
    

def parking_log(Plate):
    #Check if the Plate is already in the database & Parked
    cur.execute(f""" select * from public."Auth_parkinglog" where "CustomerId" = 'EGPCI-AAA01-0001' and "PlateNum" = '{Plate}' and "Status" = 'Parked';""")
    query = cur.fetchall()
    if query:
        elapsed = (time.time()- query[0][5]) /60
        if elapsed <= 30:
            cash = 300
        elif elapsed <= 60:
            cash  = 500
        elif elapsed <= 90:
            cash = 700
        else:
            cash = 1000
        
        #update Checkoutimte, status, cost  and duration
        cur.execute(f""" UPDATE public."Auth_parkinglog" SET "CheckoutTime"= {time.time()}, "ExitGateId"='Main', "Status"='Exited', "Duration"={elapsed}, Cash={cash} WHERE "TicketId"=uuid'{query[0][0]}'; """)
        conn.commit()
    else:
        cur.execute(f"""INSERT INTO public."Auth_parkinglog" ("TicketId", "CustomerId", "Date", "PlateNum", "EntryGateId", "CheckinTime", "CheckoutTime", "ExitGateId", "Status", "Duration", "Cash") VALUES(uuid'{uuid.uuid4()}', 'EGPCI-AAA01-0001', date'{str(datetime.datetime.now().date())}', '{Plate}','Main', {time.time()}, Null, Null, 'Parked', Null, Null);""")
        conn.commit()
    #If it is then update the time stamp, Exit Gate, Status & duration
    #else add the Plate to the database

def alpr(img):
    regions = ['in']
    response = requests.post('https://api.platerecognizer.com/v1/plate-reader/',
                                data=dict(regions=regions),  # Optional
                                files=dict(upload=img),
                                headers={'Authorization': 'Token ec549d56a1930e6da1cbe3dccda9910bcb54072a'})
    resp_json = response.json()
    Plate = str(resp_json['results'][0]['plate']).upper()
    parking_log(Plate)
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
    elif AppMode == SIDEBAR_OPTION_DEMO_IMAGE:
        startup_load()
        st.title("Ewawe Parking Managment System")
        st.title("Please Load Image")
    elif AppMode == SIDEBAR_OPTION_UPLOAD_IMAGE:
        st.info('PRIVACY POLICY: uploaded images are never saved or stored. They are held entirely within memory for prediction \
            and discarded after the final results are displayed. ')
        f = st.file_uploader("Please Select to Upload an Image", type=['png', 'jpg', 'jpeg', 'tiff', 'gif'])
        if f is not None:
            img = f.read()
            st.image(img)
            #tfile = tempfile.NamedTemporaryFile(delete=True)
            #tfile.write(f.read())
            st.write('Please wait for the magic to happen! This may take up to a minute.')
            alpr(img)
    elif AppMode == SIDEBAR_OPTION_MEET_TEAM:
        st.title("Meet the team behind the system")
        first_column, second_column, third_column= st.beta_columns(3)
        st.success('Hope you had a great time :)')
        st.write('Please feel free to connect with us on Linkedin!')
        expandar_linkedin = st.beta_expander('Contact Information')
        expandar_linkedin.write('Patrick: https://www.linkedin.com/in/irasubiza-patrick-591b11a4/?originalSubdomain=rw')
        expandar_linkedin.write('Nicole: To be Posted')
        expandar_linkedin.write('Arnaud: https://www.linkedin.com/in/arnaud-kayonga-5910a813a/')




main()