# pyzkfp


[![PyPI version](https://badge.fury.io/py/pyzkfp.svg)](https://badge.fury.io/py/pyzkfp)

## Overview
Because ZKTeco offical SDKs suck and are unstable and full of bugs, I decided to make a simple python wrapper library of their SDKs and save you from the agony of using their products.

## Why?
why not?

## Compatibility
This library can connect to `SLK20R` and ZK series, including `ZK9500`, `ZK6500`, `ZK8500R` devices.
 
## Installation
- You have to first install the ZKFinger SDK from the offical website [here](https://www.zkteco.com/en/Biometrics_Module_SDK/ZKFinger-SDK-for-Windows) or through this direct [link](https://new-website-file.s3.ap-southeast-1.amazonaws.com/files/20220725/9774a946c3f659ddf2ae90bc8dadc3eb.rar) (might stop working) 
- Then install this library via pip:
    ```bash
    pip install pyzkfp
    ```

## Features
- Initialize and interact with ZKFinger Reader devices.
- Capture fingerprint images.
- Perform fingerprint 1:1 comparisons.
- Perform fingerprint 1:N comparisons.
- Register and identify users.
- Light & Beep control functions.

## Usage
Here's a simple example of how to use this library:

#### Initialize the ZKFP2 class and open the device
```python
from pyzkfp import ZKFP2

# Initialize the ZKFP2 class
zkfp2 = ZKFP2()
zkfp2.Init()

# Get device count and open first device
device_count = zkfp2.GetDeviceCount()
logger.info(f"{device_count} Devices found, Connecting to the first device.")
zkfp2.OpenDevice(0)
```

### Capture a fingerprint
```python
while True:
    capture = zkfp2.AcquireFingerprint()
    if capture:
        # Implement your logic here
        break
```

### Perform a 1:N comparison
```python
tmp, img = capture
finger_id, score = zkfp2.DBIdentify(tmp)
```

### Perform a 1:1 comparison
```python
res = zkfp2.DBMatch(template1, template2) # returns 1 if match, 0 if not
```

### Register a fingerprint
In order to register a fingerprint, we must collect 3 templates from the same finger. And then we can merge them into one template and store it in the device's database.
```python
templates = []
for i in range(3):
    while True:
        capture = zkfp2.AcquireFingerprint()
        if capture:
            print('fingerprint captured')
            tmp, img = capture
            templates.append(tmp)
            break
regTemp, regTempLen = zkfp2.DBMerge(*templates)

# Store the template in the device's database
finger_id = 1 # The id of the finger to be registered
zkfp2.DBAdd(finger_id, regTemp)
```

### Storing and Loading Templates from an External Database for Future Use

Given that the device's memory clears upon shutdown, this step is crucial for preserving data. You have the option to store `regTemp` (the final result of the the three merged templates) in your preferred database to retrieve them for later use. The segment of code responsible for loading the registered templates from the database to the device's memory should be run after the device's initialization. Here is a simple way to do it.

```python

members = ... # load members' `regTemp` and their corresponding fingerPrintId from your database.

for member in members:
    fid, temp = member
    zkfp2.DBAdd(fid, temp)
    ...  
```


### To turn on/off the light
```python
zkfp2.Light('green') # green/red/white
```

### Terminate the device and release resources
```python
zkfp2.Terminate()
```

For more detailed usage instructions, please refer to the example folder (WIP).

## Support My Work
If you found this project useful, please hire a private investigator to legally blackmail ZKTeco's dev team, as this would really help spread the good word of this repository.
