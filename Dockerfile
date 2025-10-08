# Use the official Python runtime image
FROM python:3.13  
 
# Create the app directory
RUN mkdir /app    
 
# Set the working directory inside the container
WORKDIR /app
 
# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 
 
# Upgrade pip
RUN pip install --upgrade pip 
 
# Copy the Django project  and install dependencies
COPY requirements.txt  .
 
# run this command to install all dependencies 
RUN pip install -r requirements.txt

# Copy the Django project to the container
COPY . .
 
# Expose the Django port
EXPOSE 8000

#instal odbc shared objects for azure aql to work
RUN apt update -y
RUN apt install unixodbc -y
 
# Run Django’s development server
CMD ["sh", "docker-entrypoint.sh"]
