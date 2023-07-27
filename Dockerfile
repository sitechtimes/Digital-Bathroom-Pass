FROM beevelop/ionic:latest
COPY . /app
WORKDIR /app/bathroomPass
RUN npm install -g ionic
RUN npm install
RUN ionic build
WORKDIR /app/backend
RUN pip install -r requirements.txt
EXPOSE 6666
CMD ["uvicorn", "main:app"]
