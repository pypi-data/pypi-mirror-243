# CaGeo: CAnonical Geospatial features

In this repository we want to collect and implement methods to extract 
from a set of raw GPS coordinates features that enrich the dataset, 
but which, simultaneously also allow dimensionality reduction.

## Features:

### Point Features
- Speed: AVG, STD, MIN, MAX
- Acceleration: AVG, STD, MIN, MAX
- angle/direction: atan2 == Bearing: angle between the magnetic north and an object ??

### Aggregate features
- Turning Angle: AVG, STD, MIN, MAX. 𝐻𝐶𝑅 = |𝑃𝑐|/𝐷𝑖𝑠𝑡𝑎𝑛𝑐𝑒 Pc is the collection of gps points at which a user changes 
   his/her heading direction exceeding a certain threshold (Hc), and |𝑃𝑐 | represents the number of elements in Pc
- Traveled Distance: SUM
- Stop Rate: 𝑆𝑅 = |𝑃𝑠|/𝐷𝑖𝑠𝑡𝑎𝑛𝑐𝑒 Ps is the collection of point with velocity smaller than a certain threshold
- Velocity Change Rate: foreach point 𝑝1. 𝑉𝑅𝑎𝑡𝑒 = |𝑉2 − 𝑉1|/𝑉1; then 𝑉𝐶𝑅 = |𝑃𝑣|/𝐷𝑖𝑠𝑡𝑎𝑛𝑐𝑒 where 𝑃𝑣 ={𝑝𝑖|𝑝𝑖 ∈ 𝑃, 𝑝𝑖 . 𝑉𝑅𝑎𝑡𝑒 > 𝑉𝑟 }
- FFT?
- duration of movement?
- traveled path?
- displacement?
- Bearing rate: B_rate(i+1) = (Bi+1 − Bi)/∆t
- Rate of bearing rate: Br_rate(i+1) = (Brate(i+1) − Brate(i))/∆t

### Derivate features
- sinuosity ?
- distance from POI

## References:
- A survey and comparison of trajectory classification methods
- Understanding mobility based on GPS data
- Revealing the physics of movement: comparing the similarity of movement characteristics of different types of moving objects
- Predicting Transportation Modes of GPS Trajectories using Feature Engineering and Noise Removal
- Determination transportation mode on mobile phones 



## Note
Per le distanze vedere Intelligent Trajectory Classification for Improved Movement Prediction

In "Identifying Different Transportation Modes from Trajectory Data Using Tree-Based Ensamble Classifier": ci sono varie misure globali