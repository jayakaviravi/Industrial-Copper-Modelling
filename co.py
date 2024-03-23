from datetime import date
import numpy as np
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

def streamlit_configuration():

    # page configuration
    st.set_page_config(page_title='Industrial Copper Modeling')

    # page header transparent color
    page_background_color = """
    <style>

    [data-testid="stHeader"] 
    {
    background: rgba(0,0,0,0);
    }

    </style>
    """
    st.markdown(page_background_color, unsafe_allow_html=True)

    st.markdown(f'<h1 style="text-align: center; color: violet">Industrial Copper Modeling</h1>',
                unsafe_allow_html=True)

def submit_button():

    st.markdown("""
                        <style>
                        div.stButton > button:first-child {
                                                            background-color: #367F80;
                                                            color: white;
                                                            width: 70%}
                        </style>
                    """, unsafe_allow_html=True)

def predict_style():
    
    st.markdown(
            """
            <style>
            .center-text {
                text-align: center;
                color: green
            }
            </style>
            """,
            unsafe_allow_html=True
        )

class user_input:

    status = ['Won', 'Lost', 'Draft', 'To be approved', 'Not lost for AM',
                    'Wonderful', 'Revised', 'Offered', 'Offerable']
    
    status_dict = {'Lost':0, 'Won':1, 'Draft':2, 'To be approved':3, 'Not lost for AM':4,
                'Wonderful':5, 'Revised':6, 'Offered':7, 'Offerable':8}
    
    country_values = [25.0, 26.0, 27.0, 28.0, 30.0, 32.0, 38.0, 39.0, 40.0, 77.0, 
                    78.0, 79.0, 80.0, 84.0, 89.0, 107.0, 113.0]
    
    item_type= ['W', 'WI', 'S', 'PL', 'IPL', 'SLAWR', 'Others']

    item_type_dict = {'W':5.0, 'WI':6.0, 'S':3.0, 'Others':1.0, 'PL':2.0, 'IPL':0.0, 'SLAWR':4.0}

    application_options = [2.0, 3.0, 4.0, 5.0, 10.0, 15.0, 19.0, 20.0, 22.0, 25.0, 26.0, 
                        27.0, 28.0, 29.0, 38.0, 39.0, 40.0, 41.0, 42.0, 56.0, 58.0, 
                        59.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 79.0, 99.0]
    
    product = [611728, 611733, 611993, 628112, 628117, 628377, 640400, 
                640405, 640665, 164141591, 164336407, 164337175, 929423819, 
                1282007633, 1332077137, 1665572032, 1665572374, 1665584320, 
                1665584642, 1665584662, 1668701376, 1668701698, 1668701718, 
                1668701725, 1670798778, 1671863738, 1671876026, 1690738206, 
                1690738219, 1693867550, 1693867563, 1721130331, 1722207579]

# Get input data from users for both regression and classification methods

class data_prediction:

    def regression():

        with st.form('Regression_form'):

            col1, col2, col3 = st.columns([0.5,0.1,0.5])

            with col1:

                item_date = st.date_input(label='Item date', min_value=date(2020,7,1), 
                                        max_value=date(2021,5,31), value=date(2020,7,1))
                
                country = st.selectbox(label='Country', options=user_input.country_values)
                
                quantity_log = st.text_input(label='Quantity tons (Min: 0.00001 & Max: 1000000000)')

                item_type = st.selectbox(label='Item type', options=user_input.item_type)

                thickness_log = st.number_input(label='Thickness', min_value=0.1, max_value=2500000.0, value=1.0) 

                product_ref = st.selectbox(label='Product ref', options=user_input.product)

            with col3:

                delivery_date = st.date_input(label='Delivery Date', min_value=date(2020,8,1), 
                                              max_value=date(2022,2,28), value=date(2020,8,1))
                
                customer = st.text_input(label='Customer ID (Min:12458, Max:30408185)')

                status = st.selectbox(label='Status', options=user_input.status)

                application = st.selectbox(label='Application', options=user_input.application_options)

                width = st.number_input(label='Width', min_value=1.0, max_value=2990.0, value=1.0) 

                reg_button = st.form_submit_button(label='SUBMIT')
                
                submit_button()

        # give information to users
        col1,col2 = st.columns([0.65,0.35])
        
        with col2:
            
            st.caption(body='*Min and Max values are reference only')

        if reg_button:
            
            # load the regression pickle model
            with open('C:/Users/JAYAKAVI/New folder/Regression_Model.pkl', 'rb') as file_r:
                reg_model = pickle.load(file_r)
            
            # make array for all user input values in required order for model prediction
            user_data = np.array([[customer, country,user_input.status_dict[status], user_input.item_type_dict[item_type], application, 
                                   width,product_ref,np.log(float(quantity_log)), np.log(float(thickness_log)),
                                   item_date.day, item_date.month, item_date.year,
                                   delivery_date.day, delivery_date.month, delivery_date.year]])
            
            # model predict the selling price based on user input
            y_pred = reg_model.predict(user_data)

            # inverse transformation for log transformation data
            selling_price = np.exp(y_pred[0])

            # round of the value with 2 decimal point (Eg: 1.35678 to 1.36)
            selling_price = round(selling_price, 2)

            return selling_price
        
    def classification():

        with st.form('classification_form'):

            col1, col2, col3 = st.columns([0.5,0.1,0.5])

            with col1:

                item_date = st.date_input(label='Item Date', min_value=date(2020,7,1), 
                                        max_value=date(2021,5,31), value=date(2020,7,1))
                
                quantity_log = st.text_input(label='Quantity Tons (Min: 0.00001 & Max: 1000000000)')

                country = st.selectbox(label='Country', options=user_input.country_values)

                item_type = st.selectbox(label='Item Type', options=user_input.item_type)

                thickness_log = st.number_input(label='Thickness', min_value=0.0, max_value=400.0, value=1.0)

                product_ref = st.selectbox(label='Product Ref', options=user_input.product)


            with col3:

                delivery_date = st.date_input(label='Delivery Date', min_value=date(2020,8,1), 
                                            max_value=date(2022,2,28), value=date(2020,8,1))
                
                customer = st.text_input(label='Customer ID (Min:12458, Max:30408185)')

                selling_price_log = st.text_input(label='Selling Price (Min:1 & Max:100001015 )') 

                application = st.selectbox(label='Application', options=user_input.application_options)

                width = st.number_input(label='Width', min_value=1.0, max_value=2990.0, value=1.0)

                cls_button = st.form_submit_button(label='SUBMIT')
                
                submit_button()

        col1,col2 = st.columns([0.65,0.35])
        
        with col2:
            st.caption(body='*Min and Max values are reference only')

        if cls_button:
            
            # load the classification pickle model
            with open('C:/Users/JAYAKAVI/New folder/Classification_model.pkl', 'rb') as file_c:
                model = pickle.load(file_c)
            
            # make array for all user input values in required order for model prediction
            user_data = np.array([[customer, country, user_input.item_type_dict[item_type], application, width, 
                                product_ref, np.log(float(quantity_log)), np.log(float(thickness_log)),np.log(float(selling_price_log)),
                                item_date.day, item_date.month, item_date.year,
                                delivery_date.day, delivery_date.month, delivery_date.year]])
            
            # model predict the status based on user input
            y_pred = model.predict(user_data)

            # we get the single output in list, so we access the output using index method
            status = y_pred[0]

            return status
        

streamlit_configuration()

with st.sidebar:

    selected = option_menu(None,  ["Home", "Prediction", "Overview"],
                        default_index=0,
                        orientation="horizontal",
                        styles={"nav-link": {"font-size": "20px", "text-align": "centre", "margin": "-3px",
                                                "--hover-color": "#545454"},
                                "icon": {"font-size": "20px"},
                                "container": {"max-width": "3000px"},
                                "nav-link-selected": {"background-color": "violet"}})

if selected=='Home':

    st.subheader(":red[Introduction:]")
    st.markdown(""" #### Like many other industries, the copper sector struggles to deal with less complicated but distorted and noisy sales and pricing data. Manual forecasting takes time and might not be precise. Making use of machine learning techniques can greatly enhance decision-making. We will deal with problems like skewness and noisy data in this solution, and create a regression model to forecast selling rates and a classification algorithm to forecast the lead status (WON or LOST).""")

    st.markdown("#### :red[Domain:] Manufacturing")
    st.markdown('#### :red[Tools used:] Python scripting, Data Preprocessing,EDA, Streamlit')


if selected=='Prediction':

    tab1,tab2=st.tabs([':green[PREDICT SELLING PRICE]', ':green[PREDICT STATUS]'])

    with tab1:

        try:
            
            selling_price=data_prediction.regression()

            if selling_price:

                predict_style()
                st.markdown(f'### <div class="center-text">Predicted Selling Price = {selling_price}</div>', unsafe_allow_html=True)
                st.balloons()
        
        except ValueError:

            st.warning(':red[Quantity Tons / Customer ID is empty]')

    with tab2:

        try:

            status = data_prediction.classification()

            if status == 1:
                predict_style()
                st.markdown(f'### <div class="center-text">Predicted Status = Won</div>', unsafe_allow_html=True)
                st.balloons()
                

            elif status == 0:
                predict_style()
                st.markdown(f'### <div class="center-text">Predicted Status = Lost</div>', unsafe_allow_html=True)
                st.snow()

        except ValueError:
            st.warning(':red[Quantity Tons / Customer ID / Selling Price is empty]')


if selected=='Overview':

    st.subheader("**:red[Key Objectives:]**")
    
    st.markdown("""
        1. :blue[**Data Exploration:**]
            - Identify and address skewness and outliers in the sales dataset.
        2. :blue[**Data Preprocessing:**]
            - Transform data and implement strategies to handle missing values effectively.
        3. :blue[**Regression Model:**]
            - Develop a robust regression model to predict '**Selling_Price.**'
            - Utilize advanced techniques such as data normalization and feature scaling.
        4. :blue[**Classification Model:**]
            - Build a classification model to predict lead status (WON/LOST).
            - Leverage the '**STATUS**' variable, considering WON as Success and LOST as Failure.""")
    st.subheader(":red[Overview:]")
    
    st.markdown("""By incorporating machine learning in data exploration, preprocessing, regression, and classification, this solution provides a comprehensive approach for the copper industry to improve pricing decisions and lead status assessments. 
                The Streamlit web application is a useful tool that guarantees decision-makers' accessibility and usability, with a focus on the special tasks of :green[**Selling Price**]  and  :green[**Stauts Lead**] prediction.""")
    
    button = st.button("EXIT!")
    
    if button:
        st.success("**Thank you for utilizing this platform. I hope you have received the predicted price and status for your copper industry!**")    