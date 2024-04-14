from fastapi import Query, Response
from parsing_navigation import get_table_by_request
from fastapi import FastAPI, File, UploadFile
from selenium import webdriver
import tempfile
from resume_extract.classifier import classify_resume

app = FastAPI()


# https://127.0.0.1:8000/get_vacancies/?request=frontend&source=djinni
@app.get("/get_vacancies/")
async def process_string(request: str = Query(...), source: str = Query(...)):
    """
        Endpoint to retrieve job vacancies based on the search request and source website.

        Args:
            request (str): The search request.
            source (str): The source website ('work.ua', 'robota.ua', 'dou', 'djinni').

        Returns:
            Response: Response object containing the CSV data of job vacancies.
    """

    if source != 'work.ua':
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        table = get_table_by_request(request, source, driver)
        driver.quit()
    else:
        table = get_table_by_request(request, source, '')
    csv_string = table.to_csv(index=False)
    return Response(content=csv_string, media_type="text/csv")


@app.post("/analyze_resume/")
async def analyze_resume(file: UploadFile = File(...)):
    """
        Endpoint to analyze the job category based on the uploaded resume file.

        Args:
            file (UploadFile): The uploaded resume file.

        Returns:
            dict: Dictionary containing the predicted job category.
    """

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(await file.read())

        with open(temp_file.name, 'rb') as opened_file:
            class_name = classify_resume(opened_file)
            print(class_name)

        return {"class": class_name}


# uvicorn server:app --reload
# uvicorn server:app --http h11
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)