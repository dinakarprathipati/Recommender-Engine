# -*- coding: utf-8 -*-
import knn
import svd
from flask import Flask,render_template,request,url_for,redirect

app = Flask(__name__,static_url_path='/static')

bookname = ""

@app.route('/send', methods=['GET' , 'POST'])
def send():
    if request.method == 'POST':
        global bookname
        bookname = request.form.get("bookname")
    return render_template('main.html')

@app.route('/main_page', methods=['GET','POST'])
def main_page():
    if request.method == "POST":
        return redirect(url_for('main'))
    return render_template('main.html')


@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    selected_option = request.args.get('type')
    if selected_option == '1':
        k=["This option is yet to come..!"]
    if selected_option == '2':
        k=knn.knn(bookname)
    if selected_option == '3':
        k=svd.svd(bookname)  
    if selected_option == '4':
        k=["The Lovely Bones: A Novel","The Da Vinci Code","The Red Tent (Bestselling Backlist)","Harry Potter and the Sorcerer's Stone (Harry Potter (Paperback))","The Secret Life of Bees","Wild Animus","Divine Secrets of the Ya-Ya Sisterhood: A Novel","Where the Heart Is (Oprah's Book Club (Paperback))","Girl with a Pearl Earring","Angels &amp; Demons"]
    return render_template('recommendations.html', k=k)



if __name__ == "__main__":
    app.run()
    
