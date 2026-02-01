import streamlit as st
import pandas as pd
import random
from sklearn.preprocessing import StandardScaler
import pickle
col = ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup']
st.title("California Housing price prediction")
st.image('https://0701.static.prezi.com/preview/v2/f524s3b7ixvvb7lkkxa2ouskoh6jc3sachvcdoaizecfr3dnitcq_3_0.png')
st.header('Model of housing prices to predict median house values in California',divider=True)

st.sidebar.title('Select House Features 🏠')
st.sidebar.image('https://cdn.pixabay.com/photo/2016/08/16/03/39/home-1597079_1280.jpg')
st.sidebar.image('https://static.vecteezy.com/system/resources/previews/026/586/537/large_2x/beautiful-modern-house-exterior-with-grass-field-modern-residential-district-and-minimalist-building-concept-by-ai-generated-free-photo.jpg')

temp_df = pd.read_csv('california.csv')

temp_df = pd.read_csv('california.csv')
random.seed(52)
all_values= []
for i in temp_df[col]:
    min_value, max_value = temp_df[i].agg(['min','max'])

    var =st.sidebar.slider(f'Select {i} value', int(min_value), int(max_value),
                      random.randint(int(min_value),int(max_value)))
    all_values.append(var)
ss=StandardScaler()
ss.fit(temp_df[col])

final_value= ss.transform([all_values])
with open('house_price_pred_ridge_model.pkl','rb') as f:
   chatgpt= pickle.load(f)
price= chatgpt.predict(final_value)[0]
import time
st.write(pd.DataFrame(dict(zip(col,all_values)),index =[1]))

progress_bar = st.progress(0)
placeholder = st.empty()
placeholder.subheader('Predicting Price')
place = st.empty()
place.image('https://i.gifer.com/origin/a3/a3b1fa69178f24498a5250a9612d9e1f_w200.gif',width =70)
if price>0:

    for i in range(100):
        time.sleep(0.05)
        progress_bar.progress(i + 1)

    body = f'Predicted Median House Price: ${round(price,2)} Thousand Dollars'
    placeholder.empty()
    place.empty()
    # st.subheader(body)

    st.success(body)
else:
    body = 'Invalid House features Values'
    st.warning(body)
    
st.markdown('Designed by:**Ashish Luthra**')


