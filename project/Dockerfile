FROM python:3.8-slim

WORKDIR /app

# Install dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first to leverage Docker caching
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_RUN_PORT=5000

# Set environment variables for MySQL
ENV MYSQL_HOST=same-mysql
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=my-secret-pw
ENV MYSQL_DB=my_database
ENV MYSQL_PORT=3306

# Command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
