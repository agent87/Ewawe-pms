import streamlit as st
import time
import requests



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

def alpr(img):
    regions = ['in']
    response = requests.post('https://api.platerecognizer.com/v1/plate-reader/',
                                data=dict(regions=regions),  # Optional
                                files=dict(upload=img),
                                headers={'Authorization': 'Token ec549d56a1930e6da1cbe3dccda9910bcb54072a'})
    resp_json = response.json()
    Plate = str(resp_json['results'][0]['plate']).upper()
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