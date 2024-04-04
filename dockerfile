FROM python:3.12-alpine

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 8080

# Copy the rest of the application code
COPY . .

# Run migrations
RUN python main.py

# Set the entrypoint
ENTRYPOINT ["python", "manage.py"]

# Set the default command to run
CMD ["runserver", "0.0.0.0:8000"]