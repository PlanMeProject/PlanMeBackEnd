import logging

import requests


class CoursesService:
    @staticmethod
    def get_classroom_courses(access_token):
        url = "https://classroom.googleapis.com/v1/courses"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Failed to retrieve classroom data: {response.text}")
            raise Exception("Failed to retrieve classroom data")
