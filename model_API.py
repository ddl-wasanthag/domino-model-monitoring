import pickle
import uuid
import datetime

from sklearn.tree import DecisionTreeRegressor

from domino_data_capture.data_capture_client import DataCaptureClient

features = ["bedrooms", "bathrooms","sqft_living","sqft_lot","floors",
            "waterfront","view","condition","grade", "sqft_above",
            "sqft_basement","yr_built","yr_renovated","zipcode","lat","long",
            "sqft_living15","sqft_lot15"]

target = ["price"]

data_capture_client = DataCaptureClient(features, target)

model_file_name = "price_dt_py.sav"
model = pickle.load(open(model_file_name, 'rb'))


def predict_price(bedrooms, bathrooms,sqft_living,sqft_lot,floors,
                    waterfront,view,condition,grade,sqft_above,sqft_basement,
                    yr_built,yr_renovated,zipcode,lat,long, sqft_living15,
                    sqft_lot15):
    
    feature_values = [bedrooms, bathrooms,sqft_living,sqft_lot,floors,
                    waterfront,view,condition,grade,sqft_above,sqft_basement,
                    yr_built,yr_renovated,zipcode,lat,long,
                    sqft_living15,sqft_lot15]
    
    price_prediction = model.predict([feature_values])
    
    # Record eventID and current time
    event_id = uuid.uuid4()
    event_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Capture this prediction event so Domino can track and monitor them
    data_capture_client.capturePrediction(
        feature_values,
        price_prediction,
        event_id=event_id,
        timestamp=event_time,
    )
    
    return(dict(prediction = price_prediction[0]))
