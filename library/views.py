from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.core.mail import send_mail
#from librarymanagement.settings import EMAIL_HOST_USER


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/index.html')

#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/studentclick.html')

#for showing signup/login button for teacher
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/adminclick.html')



def adminsignup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'library/adminsignup.html',{'form':form})






def studentsignup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'library/studentsignup.html',context=mydict)




def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return render(request,'library/adminafterlogin.html')
    else:
        return render(request,'library/studentafterlogin.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    #now it is empty book form for sending to html
    form=forms.BookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.BookForm(request.POST)
        if form.is_valid():
            user=form.save()
            return render(request,'library/bookadded.html')
    return render(request,'library/addbook.html',{'form':form})

from django.db.models import Q

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewbook_view(request):
    search_query = request.GET.get('search', '')  # Get search query from the URL parameters
    
    # Fetch all books, or filter based on search query
    books = models.Book.objects.all()

    # If there's a search query, filter by title or author
    if search_query:
        books = books.filter(
            Q(name__icontains=search_query) | Q(author__icontains=search_query)
        )

    return render(request, 'library/viewbook.html', {'books': books, 'search_query': search_query})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form = forms.IssuedBookForm()

    if request.method == 'POST':
        form = forms.IssuedBookForm(request.POST)
        if form.is_valid():
            # Extract the data from the form
            student = form.cleaned_data['enrollment2']
            book = form.cleaned_data['isbn2']

            # Create and save the IssuedBook instance
            issued_book = models.IssuedBook(student=student, book=book)
            issued_book.save()  # Save the issued book entry

            # Redirect to a page after successfully issuing the book
            return redirect('/afterlogin')  # Change 'viewissuedbook' to the actual name of your page

    return render(request, 'library/issuebook.html', {'form': form})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date
from . import models

from django.shortcuts import render
from datetime import date
from . import models  # Ensure you have the correct model import

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    search_query = request.GET.get('search', '')  # Get the search term from the URL query parameters

    # Filter issued books by student enrollment if a search query is provided
    if search_query:
        issued_books = models.IssuedBook.objects.filter(student__enrollment__icontains=search_query)
    else:
        issued_books = models.IssuedBook.objects.all()

    # Build a list of tuples with issued book and related information
    issued_books_info = []
    today = date.today()
    
    for ib in issued_books:
        issdate = ib.issuedate.strftime("%d-%m-%Y")
        expdate = ib.expirydate.strftime("%d-%m-%Y")

        # Fine calculation based on expiry date
        overdue_days = (today - ib.expirydate).days
        fine = max(0, overdue_days * 8) if overdue_days > 0 else 0  # Fine calculation

        # Tuple with student, book, and issue information, including fine
        issued_books_info.append({
            'student_name': ib.student.get_name,
            'enrollment': ib.student.enrollment,
            'book_name': ib.book.name,
            'author': ib.book.author,
            'issue_date': issdate,
            'expiry_date': expdate,
            'fine': fine
        })

    return render(request, 'library/viewissuedbook.html', {
        'issued_books': issued_books_info, 
        'search_query': search_query, 
        'today': today
    })


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    search_query = request.GET.get('search', '')  # Get the search query (enrollment number)
    
    # Fetch all students
    students = models.StudentExtra.objects.all()

    # If a search query exists, filter the students by enrollment number
    if search_query:
        students = students.filter(enrollment__icontains=search_query)

    return render(request, 'library/viewstudent.html', {'students': students, 'search_query': search_query})



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from . import models

@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    # Fetch the student information based on the logged-in user
    student = models.StudentExtra.objects.get(user_id=request.user.id)

    # Retrieve all issued books for the current student
    issued_books = models.IssuedBook.objects.filter(student=student)

    li1 = []
    li2 = []

    # Loop through each issued book
    for ib in issued_books:
        # Fetch related book information
        book = ib.book

        # Add book details (student name, enrollment, branch, book name, book author) to li1
        t1 = (request.user, student.enrollment, student.branch, book.name, book.author)
        li1.append(t1)

        # Format the issue and expiry dates
        issdate = ib.issuedate.strftime('%d-%m-%Y')
        expdate = ib.expirydate.strftime('%d-%m-%Y')

        # Fine calculation based on overdue days
        overdue_days = (date.today() - ib.expirydate).days
        fine = max(0, overdue_days * 10) if overdue_days > 0 else 0

        # Add issue, expiry dates and fine to li2
        t2 = (issdate, expdate, fine)
        li2.append(t2)

    # Pass data to the template
    return render(request, 'library/viewissuedbookbystudent.html', {'li1': li1, 'li2': li2})

def aboutus_view():
    pass
def contactus_view():
    pass


from datetime import date
from django.shortcuts import redirect
from django.urls import reverse
from .models import IssuedBook, PendingFine
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import date
from .models import IssuedBook, PendingFine
from django.shortcuts import redirect
from django.shortcuts import redirect


@login_required(login_url='studentlogin')
def return_book_view(request):
    student = request.user.studentextra
    issued_books = IssuedBook.objects.filter(student=student)

    if request.method == 'POST':
        book_id = request.POST.get('book_id')

        try:
            book_to_return = IssuedBook.objects.get(student=student, book__id=book_id)
        except IssuedBook.DoesNotExist:
            return render(request, 'library/return_book.html', {
                'issued_books': issued_books,
                'error_message': "The selected book record was not found."
            })

        if date.today() > book_to_return.expirydate:
            overdue_days = (date.today() - book_to_return.expirydate).days
            fine_amount = overdue_days * 8

            pending_fine, created = PendingFine.objects.get_or_create(student=student)
            pending_fine.money += fine_amount
            pending_fine.save()

        book_to_return.delete()
        
        return redirect('/studentclick')

    return render(request, 'library/return_book.html', {'issued_books': issued_books})

from django.shortcuts import render
from .models import PendingFine

@login_required(login_url='studentlogin')
def view_fine_view(request):
    student = request.user.studentextra
    try:
        # Get pending fine for the student
        pending_fine = PendingFine.objects.get(student=student)
        fine_amount = pending_fine.money
    except PendingFine.DoesNotExist:
        # No pending fine found, set fine_amount to 0
        fine_amount = 0

    # Pass fine amount to the template
    return render(request, 'library/view_fine.html', {'fine_amount': fine_amount})

from django.shortcuts import render
from django.db.models import Q
from .models import StudentExtra, PendingFine  # Import the new models

def pending_fines_view(request):
    query = request.GET.get('search', '')  # Get the search query if any
    fines = PendingFine.objects.filter(money__gt=0)  # Only students with pending fines

    # Apply search filter if there's a query
    if query:
        fines = fines.filter(student__enrollment__icontains=query)

    return render(request, 'library/pending_fines.html', {'fines': fines, 'query': query})
