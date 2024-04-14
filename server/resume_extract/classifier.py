import re
import PyPDF2
import joblib


def cleanResume(resumeText):
    """
        Function to clean the resume text by removing URLs, mentions, hashtags, special characters, and extra whitespaces.

        Args:
            resumeText (str): The raw text extracted from the resume.

        Returns:
            str: Cleaned resume text.
    """

    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText)
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText


def classify_resume(file):
    """
        Function to classify the type of job based on the resume.

        Args:
            file (file): The PDF file containing the resume.

        Returns:
            str: The predicted job category.
    """

    text = ''

    pdf_reader = PyPDF2.PdfReader(file)

    num_pages = len(pdf_reader.pages)

    for page_number in range(num_pages):
        page = pdf_reader.pages[page_number]

        cur_text = page.extract_text()

        text += cur_text

    cleanedText = cleanResume(text)

    word_vectorizer = joblib.load('resume_extract/vectorizer.pkl')

    WordFeatures = word_vectorizer.transform([cleanedText])

    knn = joblib.load('resume_extract/model.pkl')

    decoder = {
        0: 'Advocate',
        1: 'Arts',
        2: 'Automation Testing',
        3: 'Blockchain',
        4: 'Business Analyst',
        5: 'Civil Engineer',
        6: 'Data Science',
        7: 'Database',
        8: 'DevOps Engineer',
        9: 'DotNet Developer',
        10: 'ETL Developer',
        11: 'Electrical Engineering',
        12: 'HR',
        13: 'Hadoop',
        14: 'Health and fitness',
        15: 'Java Developer',
        16: 'Mechanical Engineer',
        17: 'Network Security Engineer',
        18: 'Operations Manager',
        19: 'PMO',
        20: 'Python Developer',
        21: 'SAP Developer',
        22: 'Sales',
        23: 'Testing',
        24: 'Web Designing'
    }

    return decoder[knn.predict(WordFeatures)[0]]


if __name__ == '__main__':
    file = open('Untitled-resume.pdf', 'rb')
    print(classify_resume(file))
