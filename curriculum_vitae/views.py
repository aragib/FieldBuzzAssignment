from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, FormView
from django.core.files.storage import FileSystemStorage
import requests
import uuid
from curriculum_vitae.forms import LoginForm, CVForm


LOGIN_URL = "https://recruitment.fisdev.com/api/login/"
TEST_VERSION_URL = "https://recruitment.fisdev.com/api/v0/recruiting-entities/"
FINAL_VERSION_URL = "https://recruitment.fisdev.com/api/v1/recruiting-entities/"
CV_FILE_URL = "https://recruitment.fisdev.com/api/file-object/"

class IndexView(FormView):
    form_class = LoginForm
    template_name = 'curriculum_vitae/login.html'
    success_url ="/login/"


class LoginView(View):
    
    def post(self, request, *args, **kwargs):
        self.username = self.request.POST.get("username") 
        self.password = self.request.POST.get("password")
        
        token = self.get_token()
        if token:
            request.session['token'] = token
            return redirect('curriculum_vitae:curriculum_vitae_info')
        else:
            return redirect('curriculum_vitae:index')


    def get_token(self):
        token = None
        headers = {'Content-type': 'application/json'}
        payload = {
            "username" : self.username,
            "password": self.password
        }
        response = requests.post(url=LOGIN_URL, json=payload, headers=headers)
        if response.status_code == 200:
            token = response.json()['token']
        return token



class CurriculumVitaeInformation(FormView):
    form_class = CVForm
    template_name = 'curriculum_vitae/cv_data.html'
    success_url ="/curriculum_vitae_submit/"



class CVSubmission(View):

    def post(self, request, *args, **kwargs):
        
       
        token = self.get_token_from_session(request)
        
        form_fields_list = ['name', 'email', 'phone', 'full_address', 'name_of_university', 'graduation_year', 'cgpa',
        'experience_in_months','current_work_place_name','applying_in','expected_salary','field_buzz_reference',
        'github_project_url']

        
        tsync_id = '2f2c94d9-423a-11eb-9004-7c2a318ac2d5'

       

        cv_info = {}
        for field in form_fields_list:
            cv_info[field] = self.request.POST.get(field)
        
        curriculum_vitae_file = self.request.FILES.get('cv_file')
        cv_info['tsync_id'] = tsync_id
        cv_info['cv_file']= {
            "tsync_id" : str(uuid.uuid1())
        }

       
        headers = {'Authorization': 'Token ' + token,'Content-type': 'application/json'}
        response = requests.post(url=FINAL_VERSION_URL, json=cv_info, headers=headers)
        test_response = response.json()
        
    
        if response.status_code == 200 or 201:
            
            file_token_id = response.json()['cv_file']['id']
            file_update_url = f"{CV_FILE_URL}{str(file_token_id)}/"
            
            file_payload = {
                'file': curriculum_vitae_file.read()
            }

            headers = {'Authorization': 'Token ' + token,}
            response = requests.put(url=file_update_url, files=file_payload, headers=headers)
           

            if response.status_code < 300:
               
                return redirect('curriculum_vitae:success')

            else:
               
                return redirect('curriculum_vitae:fail')

        else:
        
            return redirect('curriculum_vitae:fail')
    
    
    def get_token_from_session(self, request):
        token = None
        if 'token' in request.session:
            token = request.session.get('token')
        return token

