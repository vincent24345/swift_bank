FROM python:3.10

WORKDIR /app

COPY . .

# Install everything from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "flask_bank_app_mysql.py"]
