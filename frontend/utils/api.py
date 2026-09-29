import requests


API_URL = "http://127.0.0.1:8000"


# =========================================================
# BACKEND HEALTH CHECK
# =========================================================

def check_backend():

    try:

        response = requests.get(

            f"{API_URL}/health",

            timeout=10

        )


        response.raise_for_status()


        return response.json()


    except requests.exceptions.RequestException as error:

        return {

            "error": str(error)

        }


# =========================================================
# ANALYZE PAPER
# =========================================================

def analyze_paper(uploaded_file):

    try:

        files = {

            "file": (

                uploaded_file.name,

                uploaded_file.getvalue(),

                "application/pdf"

            )

        }


        response = requests.post(

            f"{API_URL}/api/analyze/paper",

            files=files,

            timeout=300

        )


        if response.status_code == 409:

            return {

                "error":

                    response.json().get(
                        "detail",
                        "This paper has already been analyzed."
                    )

            }


        response.raise_for_status()


        return response.json()


    except requests.exceptions.RequestException as error:

        return {

            "error": str(error)

        }


# =========================================================
# GET HISTORY
# =========================================================

def get_history():

    try:

        response = requests.get(

            f"{API_URL}/api/history/",

            timeout=30

        )


        response.raise_for_status()


        return response.json()


    except requests.exceptions.RequestException as error:

        return {

            "error": str(error)

        }


# =========================================================
# ALIAS FOR DASHBOARD
# =========================================================

def get_analysis_history():

    return get_history()


# =========================================================
# GET SINGLE PAPER ANALYSIS
# =========================================================

def get_paper_analysis(paper_id):

    try:

        response = requests.get(

            f"{API_URL}/api/history/{paper_id}",

            timeout=30

        )


        response.raise_for_status()


        return response.json()


    except requests.exceptions.RequestException as error:

        return {

            "error": str(error)

        }


# =========================================================
# DELETE PAPER
# =========================================================

def delete_paper(paper_id):

    try:

        response = requests.delete(

            f"{API_URL}/api/history/{paper_id}",

            timeout=30

        )


        response.raise_for_status()


        return response.json()


    except requests.exceptions.RequestException as error:

        return {

            "error": str(error)

        }