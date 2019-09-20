import os
from PIL import Image
from flask import Flask, render_template, request, flash, jsonify, url_for
from run import connection
import pymysql


def add_product(name, cat_id, condition, age, descrption, img):
    try:
        with connection.cursor() as cursor:
            sql = """  INSERT INTO Products
            (Product_name, Image, Description, Age, Product_condition, Category_id, Availability)
            VALUES ('{}','{}','{}','{}','{}',{},true );""".format(name.capitalize(), img, descrption, age, condition, cat_id)
            cursor.execute(sql)
            connection.commit()
    finally:
        # connection.close()  
        return "OK"
        
def get_last_product():
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """SELECT Product_id FROM Products ORDER BY Product_id DESC LIMIT 1"""
            cursor.execute(sql)
            for item in cursor:
                product_id = item["Product_id"]
    finally:
        return product_id

def add_user(username, user_email, address, prod_id):
    try:
        with connection.cursor() as cursor:
            sql = """  INSERT INTO Users
            (Username, User_email , address, User_type , Product_id)
            VALUES ('{}' ,'{}' , '{}', "Donor", '{}');""".format(username ,user_email , address, prod_id)
            cursor.execute(sql)
            connection.commit()
    finally:
        return True

def get_last_user():
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """SELECT User_id FROM Users ORDER BY User_id DESC LIMIT 1"""
            cursor.execute(sql)
            for item in cursor:
                user_id = item["User_id"]
    finally:
        return user_id

def add_post(User_id, prod_id):
    try:
        with connection.cursor() as cursor:
            sql = """  INSERT INTO Posts
            (User_id, Product_id)
            VALUES ('{}', '{}');""".format(User_id, prod_id)
            cursor.execute(sql)
            connection.commit()
    finally:
        # connection.close() 
        return "yes"
        

def get_category_data(category_id):
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """SELECT Products.Product_name, 
                    Products.Product_id,
                    Products.Image, 
                    Products.Description, 
                    Products.Age, 
                    Products.Product_condition,
                    Users.Username,
                    Users.Address,
                    Posts.Date
                    FROM Products INNER JOIN Users ON Users.Product_id = Products.Product_id
                    INNER JOIN Posts ON Posts.Product_id = Products.Product_id
                    WHERE Products.Category_id = {} and Availability = 1 and Users.User_type = "Donor";""".format(category_id)
            cursor.execute(sql)
            return cursor
    finally:
        print("yes")

def get_product_data(prod_id):
    product_list = ""
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """SELECT Products.Product_name, 
                    Products.Product_id,
                    Products.Image, 
                    Products.Description, 
                    Products.Age, 
                    Products.Product_condition,
                    Users.Username,
                    Users.User_email,
                    Users.Address
                    FROM Products INNER JOIN Users ON Users.Product_id = Products.Product_id
                    WHERE Products.Product_id = {} and Availability = 1 ;""".format(prod_id)
            cursor.execute(sql)
            
            for items in cursor:
                print(items, "itemsssss")
                product_list = items
            
            return product_list
    finally:
        # connection.close()
        print("Sure")

def save_customer_info(username, user_email, prod_id):
    try:
        with connection.cursor() as cursor:
            sql = """  INSERT INTO Users
            (Username, User_email, User_type , Product_id)
            VALUES ('{}' , '{}', "Customer", '{}');""".format(username, user_email, prod_id)
            cursor.execute(sql)
            connection.commit()
    finally:
        return True

def update_availability(prod_id):
    try:
        with connection.cursor() as cursor:
            sql = """  UPDATE Products SET Availability = 0 
            WHERE Product_id = {} """.format(prod_id)
            cursor.execute(sql)
            connection.commit()
    finally:
        return True

# def resize_image(input_image_path,
#                  output_image_path,
#                  size):
#     print("in here")
#     original_image = Image.open(input_image_path)
#     width, height = original_image.size
#     print('The original image size is {wide} wide x {height} '
#           'high'.format(wide=width, height=height))
 
#     resized_image = original_image.resize(size)
#     width, height = resized_image.size
#     print('The resized image size is {wide} wide x {height} '
#           'high'.format(wide=width, height=height))
#     # resized_image.show()
#     print(os.path.abspath("") + "/static/img/uploads" + "test.jpg", "output_image_path")
#     resized_image.save(output_image_path)

def scale_image(input_image_path,
                output_image_path,
                width=None,
                height=None
                ):
    original_image = Image.open(input_image_path)
    w, h = original_image.size
    print('The original image size is {wide} wide x {height} '
          'high'.format(wide=w, height=h))
 
    if width and height:
        max_size = (width, height)
    elif width:
        max_size = (width, h)
    elif height:
        max_size = (w, height)
    else:
        # No width or height specified
        raise RuntimeError('Width or height required!')
 
    original_image.thumbnail(max_size, Image.ANTIALIAS)
    original_image.save(output_image_path)
 
    scaled_image = Image.open(output_image_path)
    width, height = scaled_image.size
    print('The scaled image size is {wide} wide x {height} '
          'high'.format(wide=width, height=height))

def get_recent_product():
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """SELECT Products.Product_name, 
                    Products.Product_id,
                    Products.Image, 
                    Products.Description, 
                    Products.Age, 
                    Products.Product_condition,
                    Products.Category_id, 
                    Users.Username,
                    Users.Address,
                    Posts.Date
                    FROM Products INNER JOIN Users ON Users.Product_id = Products.Product_id
                    INNER JOIN Posts ON Posts.Product_id = Products.Product_id
                    WHERE Availability = 1 and Users.User_type = "Donor" LIMIT 6;"""
            cursor.execute(sql)
            return cursor
    finally:
        print("yes")