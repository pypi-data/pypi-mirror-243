# sig_saturate
Second-Order Lag System with Saturation
Highlights: 
1. Set system parameteers for second order lag system
2. Set upper and lower saturation limits
3. slect from different types of input signal
4. Set / change the properties of input signal
5. Visualise the input and output signal

### Chechout the Demo hosted at [Link](https://huggingface.co/spaces/bokey/sig_saturate)

## Installation

#### Pypi
run following command in terminal
```bash
pip install sig-saturate
```

#### From source
Run following command in terminal
1. ```git clone https://github.com/bokey007/sig_saturate```
2. ```cd sig_saturate```
3. ```python setup.py sdist bdist_wheel```
4. ```pip install ./dist/sig_saturate-0.1.0.tar.gz```

## Usage
```bash
sig_saturate.run
```
- Above command will lauch the app on default port 8501. 
- Open the browser and go to http://localhost:8501
- play with the parameters interatively and visualise input and output signals from different sets of parameters.

```bash
sig_saturate.run --port 8080
```
Above command can be used to specify the port on which you want to run the app.

## Demo
![](https://github.com/bokey007/sig_saturate/blob/main/doc_images/Sig_saturate_Screenshot.png)

## Solution is implemnted in following three steps 
1. Generate input siganls as per user inputs
2. Simulates the behavior of a second-order lag system with saturation
3. Visualization the input and output

Development tools:

1. setuptools (https://pypi.org/project/setuptools/): Used to create a python package
2. pipreqs (https://pypi.org/project/pipreqs/): Used to create requirements.txt file
3. twine (https://pypi.org/project/twine/): Used to upload the package to pypi.org
4. wheel (https://pypi.org/project/wheel/): Used to create a wheel file

