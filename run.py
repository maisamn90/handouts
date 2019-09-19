import os
from flask import Flask, render_template, request, flash, jsonify, url_for
import json
from main import *
import pymysql
from flask_mail import Mail, Message

connection = pymysql.connect(host='my-database-class.ctr3xxx4mow6.ca-central-1.rds.amazonaws.com',
                            user='***',
                            password='***',
                            db='Handouts'
                            )    
app = Flask(__name__)
app.config['IMAGE_UPLOADS'] = "static/img/uploads"
app.secret_key = "its_secret"

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '***'
app.config['MAIL_PASSWORD'] = '***'
app.config['MAIL_USE_TSL'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = '***'
mail = Mail(app)

# initial index page
@app.route('/')
def index():
    recent_products = get_recent_product()
    if recent_products.rowcount == 0:
        recent_products = {"nodata":""}
    return render_template("index.html", data = recent_products)

@app.route('/category')
def category():
    return render_template("category.html")
    
@app.route('/category/<cat_id>')
def category_name(cat_id):
    category_data = get_category_data(cat_id)
    if category_data.rowcount == 0:
        # print("Empty")
        category_data = {"message":"We can't seems to find any products that match your selected category"}
    

    return render_template("category.html", data = category_data)


@app.route('/product_info', methods=["GET","POST"])
def product_info():
    my_arg = request.args
    product_id = my_arg['selected_product']
    customer_fullname = my_arg['customer_fullname']
    customer_email = my_arg['customer_email']
    pickup_date_time = my_arg['pickup_date_time']
    product_info = get_product_data(product_id)
    print(product_info, "product_info")
    
    save_customer_info(customer_fullname, customer_email, product_id)
    update_availability(product_id)
    
    img_src = (request.host_url).replace("/product_info","") + "/static/img/uploads/" +product_info["Image"]
    print(img_src)
    customer_msg= Message('Handouts Customer Take Request for ({})'.format(product_info["Product_name"]), recipients=['{}'.format(customer_email)])
    customer_msg.html = """<p>Dear {}</p> 
            <p>you have been sent a take request for the product bellow: </p> 
            <ul>
            
            <li><img src='{}'></li>
            <li>Product Name: {}</li>
            <li>Product Description: {}</li>
            <li>Product Age: {}</li>
            <li>Product Condition: {}</li>
            </ul>
            <br>
            <p><b>Donor information: </b></p>
             <ul>
            <li>Owner Name: {}</li>
            <li>Owner Email: {}</li>
            <li>Pickup Address: {}</li>
            <li>Pickup Date and Time:{} </li>
        
            """.format(img_src, img_src,product_info["Product_name"], 
                    product_info["Description"], product_info["Age"], 
                    product_info["Product_condition"], product_info["Username"],
                    product_info["User_email"], product_info["Address"], pickup_date_time)
    mail.send(customer_msg)
    
    
    owner_msg= Message('Handouts Take Request for ({})'.format(product_info["Product_name"]), recipients=['{}'.format(product_info["User_email"])])
    owner_msg.html = """<p>Dear {}</p> 
            <p>you have a pickup request for the product bellow: </p> 
            <ul>
            <li>Product Name: {}</li>
            <li>Product Description: {}</li>
            <li>Product Age: {}</li>
            <li>Product Condition: {}</li>
            </ul>
            <br>
            <p><b>Customer information: </b></p>
             <ul>
            <li>Customer Name: {}</li>
            <li>Customer Email: {}</li>
            </ul>
            
            <p><b>Pickup information: </b></p>
            <ul>
            <li>Pickup Address: {}</li>
            <li>Pickup Date and Time:{} </li>
            </ul>
            """.format(product_info["Username"], product_info["Product_name"], 
                    product_info["Description"], product_info["Age"], 
                    product_info["Product_condition"], customer_fullname,
                    customer_email, product_info["Address"], pickup_date_time)
    mail.send(owner_msg)
    return jsonify(True)
    
@app.route('/postAd', methods=["GET","POST"])
def postAd():
    if request.method == "POST":
        
        image  = request.files['upload_img']
        image.save(os.path.join(app.config['IMAGE_UPLOADS'], image.filename))
        print(image, url_for('index') + "static/img/uploads/" + image.filename,"test image")
        print(os.path.abspath('IMAGE_UPLOADS'), "IMAGE_UPLOADS")
        scale_image(os.path.abspath("") + "/static/img/uploads/" + image.filename, os.path.abspath("") + "/static/img/uploads/small/" + image.filename, height=245) 
        
        add_product(request.form['ad_name'], request.form['category'], request.form['condition'],request.form['product_age'], request.form['descrption'] , image.filename)
        product_id = get_last_product()
        add_user(request.form['full_name'], request.form['user_email'], request.form['address'], product_id)
        user_id = get_last_user()
        add_post(user_id, product_id)
        flash("Hey {}, Your for has been successfully added a new post".format(request.form['full_name']))
        
    return render_template("postad.html")

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
  