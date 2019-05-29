# ---- Base python ----
FROM python:3.7 AS base

# --- Information about image ---

LABEL MAINTAINER="dominic.motuka@gmail.com"
LABEL application="eats-backend"

# Create app directory
WORKDIR /usr/src/app 

# ---- Dependencies ----
FROM base AS dependencies  
COPY requirements.txt   ./

# install app dependencies
RUN pip install -r requirements.txt

# ---- Copy Files/Build ----
FROM dependencies AS build  
WORKDIR /usr/src/app 
COPY . /usr/src/app

# ----- EXPOSE port 4070 to allow communication to/from server -----
EXPOSE 4070

# Build / Compile if required

# --- Release with Alpine ----
FROM python:3.7 AS release 

# Create app directory
WORKDIR /usr/src/app

COPY --from=dependencies /usr/src/app/requirements.txt ./
COPY --from=dependencies /root/.cache /root/.cache

# Install app dependencies
RUN pip install -r requirements.txt
COPY --from=build /usr/src/app/ ./

CMD ["gunicorn","run:app", "-b", "0.0.0.0:4070", "--timeout", "360"]
