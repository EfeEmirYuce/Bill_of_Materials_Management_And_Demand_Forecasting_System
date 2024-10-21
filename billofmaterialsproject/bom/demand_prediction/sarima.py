# import os
# import pandas as pd
# from pmdarima import auto_arima
# from billofmaterialsproject import settings

# def calculate_sarima():
#     csv_file_path = os.path.join(settings.MEDIA_ROOT, 'running_shoes_sales_10_years.csv')
#     data = pd.read_csv(csv_file_path)

#     data["Month"] = pd.to_datetime(data["Month"])
#     data.set_index("Month", inplace=True)
#     data = data.drop(columns=["Category"])

#     forecast_model = auto_arima(data, trace=True,seasonal=True,m=12)
#     prediction = forecast_model.predict(1)

#     predicted_value = prediction[0]
#     return(predicted_value)