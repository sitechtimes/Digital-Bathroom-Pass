FROM node:18.16.0

#Set the timezone environment variable
ENV TZ="America/New_York"

#Set the timezone for the system
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install Python, pip, and virtual environment
RUN apt-get update \
	&& apt-get install -y --no-install-recommends python3.10 python3-pip python3-venv tzdata

COPY . /app
WORKDIR /app/backend
RUN python3 -m venv venv

# Activate the virtual environment and install the required dependencies
SHELL ["/bin/bash", "-c"]
RUN source venv/bin/activate \
	&& pip install --no-cache-dir -r requirements.txt

# Install Node dependencies
WORKDIR /app/bathroomPass
RUN npm install -g @vue/cli-service
RUN npm install -g @ionic/cli@latest
RUN npm install

# Build and run the app
RUN ionic build
WORKDIR /app/backend
EXPOSE 1738
CMD ["venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1738"]
