# source / create new py env if not exist

#!/bin/bash

iss(){
	# trick: keep container running
	while true; do date; sleep 1; done
}

# as root
ins-gl(){
	chmod 1777 /tmp
	apt update
	apt install -y libgl1 libglib2.0-0
}

ins-libs(){
	apt update
	apt install -y libgl1 libglib2.0-0
	apt install -y libgl1 libglib2.0-0 --fix-missing
	apt --fix-broken install
}

# APP_INIT_TYPE=i3
: '
source setup.sh
i3
'
i3(){
  venv_dir="/app/venv-fa"
  cd /app/
	# ins-libs

  # venv_dir="./venv-fa"
  # cd /app-pidum/
  # sleep 6000
  ins-gl

  # Check if the virtual environment exists
  if [ -d "$venv_dir" ]; then
    echo "Using existing virtual environment."
  else
    echo "Creating a new virtual environment."
    python -m venv $venv_dir
  fi

  # Activate the virtual environment
  #source $venv_dir/bin/activate

  python -m pip install --upgrade pip

  # Install required Python packages
#   pip install -r requirements.txt
  # init poet
  # curl -sSL https://install.python-poetry.org | python3 -
  # Add to shell profile
  # export PATH="$HOME/.local/bin:$PATH"

  # run worker
  # celery -A worker worker --autoreload -P gevent -l info &

  # run main service
  python main.py

	# do infinite sleep 2 prevent docker stop
  iss
}

i2(){
  : '
  # wip
  - logging
  - s
  '
  cd /app

  venv_dir="/app/venv-mc3"
  # venv_dir="./venv-mc3"

  cd /app

  # Activate the virtual environment
  source $venv_dir/bin/activate

  # use existing venv if exist
  # tf/tf env by default:
  # ls /usr/local/lib/python3.11/dist-packages/

  # call if used in parent image such as tensorflow
  pip install pendulum==2.0.5
  pip install pip==18.1 && pip install pendulum
  pip install -r requirements.txt
#   pip install -r req-ml.txt
  pip install -I gunicorn

  # jupyter, temp disabled
  # source /etc/bash.bashrc && jupyter notebook --notebook-dir=/tf --ip 0.0.0.0 --no-browser --allow-root &

  # run masonite
  # /app/craft
  # craft serve
  # python craft serve -p 8000 -b 0.0.0.0 &
  # wip do logging
  gunicorn --reload -b 0.0.0.0:8000 wsgi:application &
  # uvicorn --host 0.0.0.0 --port 8000 wsgi:application &

  # run forever
  while true; do sleep 1; done
}

# Define the path to the virtual environment
# venv_dir="/app/venv_3816"
# venv_dir="/app/venv3114"
# venv_dir="/app/venv3114"
i1(){
  venv_dir="/app/venv-mc3"

  cd /app

  # Check if the virtual environment exists
  if [ -d "$venv_dir" ]; then
    echo "Using existing virtual environment."
  else
    echo "Creating a new virtual environment."
    python -m venv $venv_dir
  fi

  # Activate the virtual environment
  source $venv_dir/bin/activate

  # python -m pip install --upgrade pip
  pip install pendulum==2.0.5

  # Install required Python packages
  pip install -r requirements.txt

  apt update

  echo "ZENML_CONNECT_URL"
  echo $ZENML_CONNECT_URL

  # zenml connect --url $ZENML_CONNECT_URL
  # Run the application
  # python3 app.py | tee -a dmy-api.log

  # trick: keep container running
  while true; do sleep 1; done
}

# wip conditional call
# i2
echo "using APP_INIT_TYPEx $APP_INIT_TYPE ..."

env

$APP_INIT_TYPE