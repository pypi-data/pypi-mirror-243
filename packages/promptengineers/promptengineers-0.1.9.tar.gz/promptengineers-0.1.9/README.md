# Prompt Engineers AI Open Source Package

#### Build and Publish

```bash
## Build Package
bash scripts/build.sh

## Publish Package to PyPi
bash scripts/publish.sh
```


#### Development

```bash
## In the application directory start your virtual env (this would be the workspace
## where your API server that you would like to install the model)
source .venv/bin/activate

## Then change directory to where your package is, make changes and run the following.
pip install .

## Switch back to the directory of your where your workspace is for you app server.
cd <path>/<app>/<server>
pip install -r requirements.txt

## Make sure your app server has the packages shown in setup.py and run your server...
```