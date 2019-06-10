#### The whole project was made together with [Agnieszka Kowalik] (https://github.com/agnkow)

I decided to upload this notebook after I did quite a lot of changes after an event, since
I do not like to leave anything unfinished and the results were worth it.

##### The goal
We had to create machine learning model to predict power demand for next week after
avaidable data.

##### Features picked
- weather from four cites located within area the data was pulled from
- dummy dates
- holidays
- day length
- time change
- lag values

##### Stack used
- scikit-learn for features selection (based on p value)
- tensorflow (sequential nn with RMSprop optimizer)

##### Results

141 RMSE for whole period
[chart](results.png)
