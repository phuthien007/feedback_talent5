from flask_admin import BaseView, expose
from flask_login import login_required
from settings import *
from models import *
from routes import *
from flask_admin.contrib.sqla import ModelView
@app.route('/admin/rating_courses/')
@login_required
def rating_course():
    data= get_data_rating()
    xs=[];ys=[]
    for x,y in data:
        xs.append(x)
        ys.append(y)

    fig = create_figure(xs ,ys,'rating_coures' ,'courses','number of rating')
    url='static/images/rating_course.png'
    if os.path.exists(url):
        os.remove(url)
    fig.savefig(url)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure(xs,ys,title,ylabel,xlabel):
    fig = Figure(figsize=(16,7),dpi=120)
    axis = fig.add_subplot(1, 1, 1)
    axis.barh(xs, ys,height = 0.3)
    axis.set_title(title)
    axis.set_ylabel(ylabel)
    axis.set_xlabel(xlabel)
    axis.set_xticks(ys)
    return fig
def create_figure_line(xs,ys,title,ylabel,xlabel):
    fig = Figure(figsize=(16,7),dpi=120)
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(xs, ys,'b*--')
    axis.set_title(title)
    axis.set_ylabel(ylabel)
    axis.set_xlabel(xlabel)
    axis.set_xticks(xs)
    axis.grid(axis='y')
    return fig
@app.route('/admin/comments_courses/')
@login_required
def comments_course():
    data= get_data_comments()
    xs=[];ys=[]
    for x,y in data:
        xs.append(x)
        ys.append(y)
    fig = create_figure(xs ,ys,'comments_courses', 'courses','number of comments' )
    url='static/images/comments_course.png'
    if os.path.exists(url):
        os.remove(url)
    fig.savefig(url)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/admin/comments_dates/')
@login_required
def comments_dates():
    data= get_data_comments_by_date()
    xs=[];ys=[]
    for x,y in data:
        xs.append(str(x))
        ys.append(y)
    print(xs,ys)
    fig = create_figure(xs ,ys,'date' ,'courses','number of comments')
    url='static/images/comments_dates.png'
    if os.path.exists(url):
        os.remove(url)
    fig.savefig(url)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/admin/rating/')
@login_required
def rating():
    data = get_each_element_rating()
    xs = np.arange(0,11,1)
    ys = [0]*11
    for  y in data:
        ys[y[0]]+=1
    fig = create_figure_line(xs, ys, 'number of rating', 'rating', 'ratings')
    url = 'static/images/rating_line.png'
    if os.path.exists(url):
        os.remove(url)
    fig.savefig(url)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')



class FeedBackView(ModelView):
    can_view_details = True
    can_export = True
    can_edit = True
    def is_accessible(self):
        return current_user.is_authenticated

    def is_visible(self):
        return current_user.is_authenticated

    def is_action_allowed(self, name):
        return current_user.is_authenticated

class rating(BaseView):
    @expose('/')
    def rating(self):
        rating()
class comments_dates(BaseView):
    @expose('/')
    def comments_dates(self):
        comments_dates()
class comments_courses(BaseView):
    @expose('/')
    def comments_courses(self):
        comments_courses()
class rating_courses(BaseView):
    @expose('/')
    def rating_courses(self):
        rating_courses()

class LogoutView(BaseView):
    @expose('/')
    def logout(self):
        logout_user()
        return self.render('/admin/index.html')

    def is_accessible(self):
        return current_user.is_authenticated

admin= Admin(app=app, name='Admin Page', template_mode='bootstrap3')

admin.add_view(FeedBackView(FeedBack, db.session))
admin.add_view(rating(name='Chart Rating '))
admin.add_view(rating_courses(name='Chart Rating-Courses'))
admin.add_view(comments_dates(name='Chart Comment-Dates'))
admin.add_view(comments_courses(name='Chart Comments-Courses'))
admin.add_view(LogoutView(name='Logout'))

