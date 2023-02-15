import flask
from flask import redirect, request, render_template, url_for, session, Blueprint
import time


users = [
    {'tutor@warwick.ac.uk': {'password': '1111', 'is_admin': True }},
    {'student@warwick.ac.uk': {'password': '2222', 'is_admin': False }},
]

routesBP = Blueprint('routesBP',__name__)

#Page for the user to enter their email and password
@routesBP.route('/login')
def login():
    return render_template('login.html')


#When user logs out, the session gets deleted and they are redirected to
#the home page
def logout():
    session.pop('user', None)
    return render_template('home.html')


#Sign in method which takes in the email and password entered on the form, and
#checks if those details are present in the users list of dictionaries
@routesBP.route('/signIn', methods=['GET', 'POST'])
def signIn():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        for user in users:
            if email in user and user[email]['password'] == password:
                session['user'] = email
                if user[email]['is_admin']:
                    return redirect(url_for('viewsBP.home', session='Tutor'))
                else:
                    return redirect(url_for('viewsBP.home', session='Student'))
        return render_template('login.html', loginError=True)

@routesBP.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('viewsBP.home'))

#This search method allows the user to search for varous parts of the web app
#such as the homepage, menu and the statistical information
@routesBP.route('/search', methods=['GET'])
def search():
    #Create a list which contains the different parts of the website which the user can search for
    pageNames = ['viewsBP.inPersonClasses2019', 'viewsBP.inPersonClasses2020', 'viewsBP.inPersonClasses2021', 'viewsBP.inPersonClasses2022', 'viewsBP.menu', 'viewsBP.home', 'routesBP.login']
    searchQuery = request.args.get('search').lower()
    #Loop through list and check if what user has input matches with any of the elements in it.
    for page in pageNames:
        if searchQuery.replace(" ","") in page.lower() and searchQuery.strip() != "":
            return redirect(url_for(page))
        #If what the user has input doesn't match with any of the page names
        #a pop-up window will appear telling them that the page doesn't exist
        #and redirects them back to the previous page.
    return """
    <script>
        alert("The page you've entered does not exist. Please ensure you use correct spelling.");
        window.history.back();
    </script>
    """ 