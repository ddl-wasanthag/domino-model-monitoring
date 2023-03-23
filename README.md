# Domino Model Monitoring Demo
This workshop is designed to introduce Domino model monitoring workflows. It is designed to be self-guided and all necessary code and data are included. 

There are two types of model monitoring workflows available in Domino. 

- ## Model API Monitoring
When a model is deployed on Domino as a Model API, 

- Domino Analyzes the training data to extract the model schema (if you register a Domino TrainingSet).

- Captures predictions as Domino datasets for monitoring.

- Generates drift detection and model quality analysis on a schedule (if you share the ground truth dataset with Domino), and alerts you if any thresholds are exceeded.

- Allows you to easily reproduce the environment with access to the captured predictions to diagnose and fix issues with your model.

See Set up monitoring for Model APIs in the Docs, https://docs.dominodatalab.com/en/latest/user_guide/2a7c3b/set-up-monitoring-for-model-apis/


If you do not want Domino to manage the prediction data collection, use the Model Monitor to configure monitoring, even for Model APIs.



- ## Model Monitor
For models deployed as other assets on Domino (App, Launcher, or Job) or external to Domino, you can use Domino to:

- Connect to the data source where the training, prediction, and ground truth data reside.

- Register a model’s entry along with its schema.

- Set up drift detection and model quality monitoring by registering the location of every new batch of prediction or ground truth data.

- Set up a schedule for Domino to run drift and model quality checks periodically and alert you if thresholds are exceeded.

See Set up Model Monitor in the docs, https://docs.dominodatalab.com/en/latest/user_guide/679cc1/set-up-model-monitor/

## Prerequisites
- Access to a Domino deployment with a practitioner role.
- Fork this repository to your own repository or use a zip file to upload the content into a Domino project. You can create a Git based project with a forked project or import it as a git repository.
- Access to AWS S3 bucket to store the training, prediction, and ground truth data.

## Monitoring Model APIs
In this section, we will 
- Create a training set and a sample model
- publish a model API
- Create data capture client to capture prediction data
- Generate Predictions
- Examine Predictions
- Create a DMM data source
- Configure ground truth data


### Create a Training Set and a sample model
In this section, you are going to create a training set that can be compared to later prediction data to monitor data drift. To read more about creating a training set see this, 
https://docs.dominodatalab.com/en/latest/api_guide/440de9/trainingsets-use-cases/We will also create an example model that we can use in the later sections.

**Step1:**

Create a workspace with Jupyter Lab IDE in the project and open the 1-House_Price_Prediction.ipynb. We are going to use the kc_house_data.csv in the sample-data folder to create the training set. Note you can use a dataset from a Domino Data Source if you wish. Just read the data from the data source into the dataset_raw.

**Step2:**

In the cell that contains a call to `Code demonstrating creation of a training set`, update the ‘training_set_name’ to a unique name of your choice and Run all cells. This will create a training set that can be associated with the current model version.

**Step3:**

Execute the cell that contains `Example code to read the training set just created`. This will display the training set.

**Step4:**

Follow the rest of the cells to create a training and test set from the training set created above. The rest of the cells will train the model and create a serialized model `price_dt_py.sav`.
At the end of this section, you have a Domino training set and a trained model.


### Publish Model API
This section set up the Model API use in the future sections that generate and store the prediction data.

**Step1:**

Review the model_api.py file and change the parameters to the `capturePrediction` call, or make changes if desired.

**Step2:**

Publish the Model API with the following:

**File name:** model_API.py 

**Function to invoke:** 
predict_price

Add the following example JSON body into the model description., so it is easy to copy and paste into the model API tester to generate sample predictions.

```
{
  "data":{
    "bedrooms" :1.417779575520277,
    "bathrooms":1.2235334622079015,
    "sqft_living":1376.2808414176138,
    "sqft_lot":-44282.09192720655,
    "floors":1.0663144705090994,
    "waterfront":-0.016425213918793445,
    "view":-0.12412711151320194,
    "condition":3.010860708305122,
    "grade":6.446308650295107,
    "sqft_above":1134.2601420161861,
    "sqft_basement":83.01687506148825,
    "yr_built":1950.9720074899026,
    "yr_renovated":38.33997291730212,
    "zipcode":98187.71575450613,
    "lat":47.512356777412954,
    "long":-122.29738607549102,
    "sqft_living15":1162.588195657737,
    "sqft_lot15":-15814.149590757263
  }
}
```


### Create Data capture client to capture prediction data
Open 2-Prediction_Test.ipynb, and run all cells to test the functionality of the instrumentation

### Generate Predictions
Use a data-generation program to populate predictions so that we can see how the model monitor is performing.

Open 3-model_api_caller.ipynb. 

Update MODEL_API_URL and MODEL_API_KEY (the access token) to match your newly published Model API. (you can find this in the overview tab of model API -> click on Python)

Update iterations if you need to Run all cells (note that nothing will be displayed)

### Configure Data Drift Monitoring
For the Model API, enable monitoring by selecting the training set to track drift against.

Go to your newly published Model API overview page and navigate to the ‘Monitoring’ tab.

Open ‘Configure Monitoring’ > ‘Data’ to select the right training set and version and set the model type to ‘Regression’

Refresh and view drift and MQ metrics, set thresholds, etc.

(NOTE: this may take up to 10 minutes to populate the prediction data in the dataset)

### Examine Predictions
Now we’ll open a workspace directly from the published model and examine the predictions.
From your published model, click ‘Open in Workspace’ to spin up a new workspace
Open the file AnalyzePredictions.ipynb
Update the path variable to point to the model version ID (a directory in the predictions Dataset) and execute the notebook to examine the recorded predictions


### Create a DMM data source
Navigate to the Model Monitor > Monitoring Data Source > Add Data source

Enter the details for AWS S3 bucket containing the data files.

### Configure ground truth data
Add ground truth tracking to the model’s monitoring to determine model quality and accuracy metrics
From the Monitoring tab, open ‘Configure Monitoring’ > ‘Data’ and follow the instructions to register ground truth data
Upon being taken to a new page to register ground truth data, upload the config that points to the data
```
{
    "variables": [
        {
            "valueType": "numerical",
            "variableType": "ground_truth",
            "name": "price_pred",
            "forPredictionOutput": "price"
        }
    ],
    "datasetDetails": {
        "name": "gt_actual_pred.csv",
        "datasetType": "file",
        "datasetConfig": {
            "path": "gt_actual_pred.csv",
            "fileFormat": "csv"
        },
        "datasourceName": "house_data_ziegler",
        "datasourceType": "s3"
    }
}
```



## Monitoring non Model APIs
In this section, we will 
- upload a training set
- upload prediction data set
- upload ground truth data
- Examine Data drift and model quality
