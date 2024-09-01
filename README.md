# qa-bot
A simple bot that exposes an API at http://127.0.0.1:8000/api/v1/qa which is POST and accepts two files document.pdf and questions (json or pdf both accepted) it reads the document.pdf and answers to the questions file based on the document provided

STEPS TO RUN:-

1- Insert your Anthropic API Key in the .env file
2- run the docker command "docker-compose up --build" to run the app.
3- If you are testing on POSTMAN paste this CURL directly and replace the files from your local

curl --location 'http://127.0.0.1:8000/api/v1/qa' \
--header 'accept: application/json' \
--form 'document=@"/Users/mehro/Downloads/document.pdf"' \
--form 'questions=@"/Users/mehro/Downloads/questions.json"'

where document.pdf is the your document file & questions.json is your questions file

I have uploaded sample document.pdf and questions.json in the root path for sample testing.
