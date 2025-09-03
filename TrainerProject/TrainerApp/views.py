import json
import time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
import logging
from django.db import transaction

from .mpesa_utils import lipa_na_mpesa

from .forms import AddCourseForm, AddDocumentForm, AddUnitForm, LoginForm, MpesaForm, RegisterForm, SelectionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Course, Department, Document, TrainingSession, Transactions, Unit, CustomUser

# Create your views here.

def home(request):
    return render(request, "front-end/index.html")

def department(request):
    title = "Departments"
    departments = Department.objects.all()
    return render(request, 'front-end/departments.html', {'departments': departments, 'title': title})

def course(request, id):
    department = Department.objects.get(id=id)
    courses = Course.objects.filter(department=id)
    return render(request, 'front-end/courses.html', {'courses': courses, 'department': department})

def unit(request, id):
    course = Course.objects.get(id=id)
    units = Unit.objects.filter(course=course)
    return render(request, 'front-end/units.html', {'units': units, 'course': course})

def document(request, id):
    unit = Unit.objects.get(id=id)
    documents = Document.objects.filter(unit=unit)
    return render(request, 'front-end/documents.html', {'documents': documents, 'unit': unit})

def contact(request):
    return render(request, 'front-end/contact.html')

def user_login(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # Here you would typically authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or Password')
        else:
            login_form = LoginForm()
    return render(request, 'back-end/login.html', {'login_form': login_form})

def user_register(request):
    register_form = RegisterForm()
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.set_password(register_form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration Successful")
            return redirect('user-login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        register_form = RegisterForm()
    return render(request, 'back-end/register.html', {'register_form': register_form})


def dashboard(request):
    user = request.user
    return render(request, 'back-end/dashboard.html', {'user': user})

def user_courses(request, id):
    user_department = request.user.department_id
    courses = Course.objects.filter(department_id=user_department)
    return render(request, 'back-end/user-courses.html', {'courses': courses})

def user_units(request, id):
    user_course = Course.objects.get(id=id)
    units = Unit.objects.filter(course=user_course)
    return render(request, 'back-end/user-units.html', {'units': units, 'course': user_course})

def user_resources(request, id):
    user_unit = Unit.objects.get(id=id)
    documents = Document.objects.filter(unit=user_unit)
    return render(request, 'back-end/user-resources.html', {'documents': documents, 'unit': user_unit})

def add_course(request):
    form = AddCourseForm()
    if request.method == 'POST':
        form = AddCourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.department = request.user.department
            course.save()
            messages.success(request, "Course added successfully")
            return redirect('user-courses', id=request.user.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AddCourseForm()
    return render(request, 'back-end/add-course.html', {'form': form})

def add_unit(request, id):
    course = Course.objects.get(id=id)
    if request.method == 'POST':
        form = AddUnitForm(request.POST, request.FILES)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.course = course
            unit.save()
            messages.success(request, "Unit added successfully")
            return redirect('user-units', id=course.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AddUnitForm()
    return render(request, 'back-end/add-unit.html', {'form': form, 'course': course})

def add_document(request, id):
    unit = Unit.objects.get(id=id)
    user = request.user
    if request.method == 'POST':
        form = AddDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.unit = unit
            document.uploaded_by = user
            document.save()
            messages.success(request, "Document added successfully")
            return redirect('user-documents', id=unit.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AddDocumentForm()
    return render(request, 'back-end/add-document.html', {'form': form, 'unit': unit})

def selection_view(request):
    form = SelectionForm()
    
    if request.method == 'POST':
        form = SelectionForm(request.POST)
        if form.is_valid():
            try:
                access_token = lipa_na_mpesa.generate_access_token()
                phone_number = form.cleaned_data['phone_number']
                
                # Initiate STK Push
                payment_response = lipa_na_mpesa.stk_push(phone_number, access_token)
                j_response = payment_response.json()

                # Check STK Push response
                if j_response.get("ResponseCode") == "0":
                    messages.info(request, "Payment initiated. Please complete the payment on your phone.")
                    
                    # Store form data in session to use after callback confirmation
                    request.session['selection_data'] = {
                        'trainer_name': form.cleaned_data['trainer_name'],
                        'trainer_number': form.cleaned_data['trainer_number'],
                        'name_of_institution': form.cleaned_data['name_of_institution'],
                        'date_of_preparation': form.cleaned_data['date_of_preparation'].isoformat(),
                        'number_of_learners': form.cleaned_data['number_of_learners'],
                        'course_class': form.cleaned_data['course_class'],
                        'number_weeks': form.cleaned_data['number_weeks'],
                        'number_of_sessions_per_week': form.cleaned_data['number_of_sessions_per_week'],
                        'hours_per_session': form.cleaned_data['hours_per_session'],
                        'department': form.cleaned_data['department'].id,
                        'course': form.cleaned_data['course'].id,
                        'unit': form.cleaned_data['unit'].id,
                    }
                    request.session['checkout_request_id'] = j_response.get("CheckoutRequestID")
                    
                    # Redirect to a waiting page or poll for payment status
                    return redirect('payment-wait')
                else:
                    messages.error(request, j_response.get("ResponseDescription", "Payment initiation failed."))
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                messages.error(request, f"Payment error: {str(e)}")
        else:
            messages.error(request, "Please correct the errors in the form.")
                       
    return render(request, 'front-end/tvet-ai.html', {'form': form})

@csrf_exempt
def payment_wait(request):
    # This view could poll for payment status or wait for callback
    checkout_request_id = request.session.get('checkout_request_id')
    if not checkout_request_id:
        messages.error(request, "No payment in progress.")
        return redirect('selection_view')
    
    # Query payment status
    try:
        access_token = lipa_na_mpesa.generate_access_token()
        query_response = lipa_na_mpesa.query_stk(checkout_request_id, access_token)
        query_data = query_response.json()
        
        if query_data.get("ResultCode") == "0":
            # Update or create transaction if not already saved by callback
            transaction, created = Transactions.objects.get_or_create(
                checkout_request_id=checkout_request_id,
                defaults={
                    'merchant_request_id': query_data.get("MerchantRequestID", ""),
                    'result_code': int(query_data.get("ResultCode", 0)),
                    'result_desc': query_data.get("ResultDesc", ""),
                    'amount': next((item['Value'] for item in query_data.get("CallbackMetadata", {}).get("Item", []) if item['Name'] == 'Amount'), 0),
                    'transaction_id': next((item['Value'] for item in query_data.get("CallbackMetadata", {}).get("Item", []) if item['Name'] == 'MpesaReceiptNumber'), ""),
                    'user_phone_number': next((item['Value'] for item in query_data.get("CallbackMetadata", {}).get("Item", []) if item['Name'] == 'PhoneNumber'), "")
                }
            )
        else:
            # Handle query failure
            messages.error(request, query_data.get("ResultDesc", "Payment status check failed."))
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        messages.error(request, f"Error checking payment status: {str(e)}")
    
    # For simplicity, assume callback updates the Transactions model
    transaction = Transactions.objects.filter(checkout_request_id=checkout_request_id).first()
    if transaction and transaction.result_code == 0:
        # Payment successful, retrieve session data
        selection_data = request.session.get('selection_data', {})
        unit = selection_data.get('unit')
        
        # Query documents
        os_document = Document.objects.filter(id=unit, document_type='OS').first()
        cu_document = Document.objects.filter(id=unit, document_type='CU').first()
        
        if not os_document and not cu_document:
            messages.error(request, "No documents found for the selected unit.")
            return redirect('selection_view')
        
        # Optionally save selection data to a model
        try:
            TrainingSession.objects.create(
                trainer_name=selection_data.get('trainer_name'),
                trainer_number=selection_data.get('trainer_number'),
                name_of_institution=selection_data.get('name_of_institution'),
                date_of_preparation=selection_data.get('date_of_preparation'),
                number_of_learners=selection_data.get('number_of_learners'),
                course_class=selection_data.get('course_class'),
                number_of_weeks=selection_data.get('number_weeks'),
                number_of_sessions_per_week=selection_data.get('number_of_sessions_per_week'),
                hours_per_session=selection_data.get('hours_per_session'),
                department=selection_data.get('department'),
                course=selection_data.get('course'),
                unit=selection_data.get('unit'),
                transaction=transaction
            )
        except ValueError as e:
            messages.error(request, f"Error saving training session: {str(e)}")
            return redirect('selection_view')

        # Clear session data
        request.session.pop('selection_data', None)
        request.session.pop('checkout_request_id', None)
        request.session.pop('response_code', None)

        messages.success(request, "Payment successful. Proceed to download your document.")
        return render(request, 'front-end/download-lp.html', {
            'os_document': os_document,
            'cu_document': cu_document
        })
    
    return render(request, 'front-end/payment-wait.html', {
        'checkout_request_id': checkout_request_id,
    })
logger = logging.getLogger(__name__)
@csrf_exempt
def process_stk_callback(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed", status=405)

    try:
        stk_callback_response = json.loads(request.body)
        logger.info("Received STK callback: %s", stk_callback_response)

        # Log to file (optional, consider using logger in production)
        with open("Mpesastkresponse.json", "a") as log:
            json.dump(stk_callback_response, log)

        body = stk_callback_response['Body']['stkCallback']
        merchant_request_id = body['MerchantRequestID']
        checkout_request_id = body['CheckoutRequestID']
        result_code = body['ResultCode']
        result_desc = body['ResultDesc']

        with transaction.atomic():
            if result_code == 0:
                callback_metadata = body['CallbackMetadata']['Item']
                amount = next(item['Value'] for item in callback_metadata if item['Name'] == 'Amount')
                transaction_id = next(item['Value'] for item in callback_metadata if item['Name'] == 'MpesaReceiptNumber')
                phone_number = next(item['Value'] for item in callback_metadata if item['Name'] == 'PhoneNumber')
                
                Transactions.objects.create(
                    merchant_request_id=merchant_request_id,
                    checkout_request_id=checkout_request_id,
                    result_code=result_code,
                    result_desc=result_desc,
                    amount=amount,
                    transaction_id=transaction_id,
                    user_phone_number=phone_number
                )
            else:
                Transactions.objects.create(
                    merchant_request_id=merchant_request_id,
                    checkout_request_id=checkout_request_id,
                    result_code=result_code,
                    result_desc=result_desc
                )
        return HttpResponse("Callback processed successfully", status=200)
    except (json.JSONDecodeError, KeyError, StopIteration) as e:
        logger.error("Error processing callback: %s", str(e))
        return HttpResponse(f"Invalid callback data: {str(e)}", status=400)
    
@csrf_exempt
@require_GET
def check_transaction_status(request):
    checkout_request_id = request.session.get('checkout_request_id')
    if not checkout_request_id:
        return JsonResponse({'status': 'error', 'message': 'No payment in progress'}, status=400)

    transaction = Transactions.objects.filter(checkout_request_id=checkout_request_id).first()
    if transaction:
        if transaction.result_code == 0:
            return JsonResponse({
                'status': 'success',
                'message': 'Payment successful. Redirecting to download page.',
                'redirect_url': '/download-lp/'  # Adjust URL as needed
            })
        else:
            return JsonResponse({
                'status': 'failed',
                'message': transaction.result_desc,
                'redirect_url': '/tvet-ai/'  # Adjust URL to retry or home page
            })
    return JsonResponse({'status': 'pending', 'message': 'Payment still processing'})
def check_stk_status(request):
    if request.method == 'GET' and 'request_id' in request.GET:
        request_id = request.GET['request_id']
        
        # Call the query function
        confirm = lipa_na_mpesa.query_stk(request_id)
        query_response = confirm.json()
        result_code = query_response.get("ResultCode")
        
        # Return the status in a JSON response
        return JsonResponse({
            'result_code': result_code,
            'message': get_status_message(result_code)
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_status_message(result_code):
    """Helper function to map result codes to messages."""
    if result_code == '0':
        return "Payment Made successfully. Proceed to Download Your document."
    elif result_code == '1037':
        return "Request Timed Out"
    elif result_code == '1032':
        return "You Cancelled The Transaction"
    elif result_code == '1':
        return "You have insufficient balance"
    else:
        return "Unknown status. Please check your transaction details."
def get_courses(request):
    department_id = int(request.GET.get('department'))
    if department_id:
        courses = Course.objects.filter(department=department_id).order_by('course_name')
        return JsonResponse([{'id': c.id, 'name': str(c)} for c in courses], safe=False)
    return JsonResponse([], safe=False)

def get_units(request):
    course_id = int(request.GET.get('course'))
    if course_id:
        units = Unit.objects.filter(course=course_id).order_by('unit_name')
        return JsonResponse([{'id': u.id, 'name': str(u)} for u in units], safe=False)
    return JsonResponse([], safe=False)

def get_documents(request):
    unit_id = int(request.GET.get('unit'))
    if unit_id:
        try:
            # unit = Unit.objects.get(id=unit_id)
            os = Document.objects.filter(unit=unit_id, document_type='OS').first()
            cu = Document.objects.filter(unit=unit_id, document_type='CU').first()
            
            data = {
                'occupational_standards': os.document_file.url if os else '',
                'curriculum': cu.document_file.url if cu else '',  
            }
            return JsonResponse(data)
        except Unit.DoesNotExist:
            pass
    return JsonResponse({'error': 'Invalid unit'}, status=400)

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('user-login')

