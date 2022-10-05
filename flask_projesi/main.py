import pyrebase as pyrebase
from flask import Flask, render_template, request, url_for, redirect, session
from firebase_admin import credentials, firestore, auth
import firebase_admin
import random
import string
import pandas as pd

config = {
    "apiKey": "AIzaSyAguRDRVXagJZdv0J-75GF3fOh0lwAmyVU",
    "authDomain": "sifreyoneticisi.firebaseapp.com",
    "databaseURL": "https://sifreyoneticisi-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "sifreyoneticisi",
    "storageBucket": "sifreyoneticisi.appspot.com",
    "messagingSenderId": "489351401281",
    "appId": "1:489351401281:web:55bfc857df9fe986579bc0",
    "measurementId": "G-GE7CEGHLYS"
}

key = {
    "type": "service_account",
    "project_id": "sifreyoneticisi",
    "private_key_id": "b17abc60805f1f9df7cc8b4ef565b94e0baee30b",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCnYxcGDCpe6f+H\nbmMzQnPrfwZIlNjkeIbz/AP19iICjQCCjmIrg6DsxDM4Uo6sJDF9wDmau1J6ZaiP\nuRGqB3nyVJ3n2AzJrN/aZo7yao3I3qZUdEkv9x9GZqH+4ugyhQM8U1qM6eCRFz9R\nvNVhRo6V0F5BTx1EPYdKiEEuOex6mBx0c00OHiy+zhTrcPRI5vT5yh/7nKYgT/VQ\n/B4AJ+pcOr/vaLXYWNv1vc1/TPYCG3kNCbsl+S1TN5zC9r4cNtuRrn8IJDflLTUx\nIRQY6K1Sn0mt2y41/tkt16xvqBdC0++A7esiGghks98pvenwGwWnbMpDbfM0p0hu\nyPBv1TbdAgMBAAECggEAIS0hK5gur7hGZtPowoipzCPVnX4vDP2clfA94rrBm+rR\njo7lA0XoF/V9R20JjTHxQ0Ddyf7Vxp+ujKn8R8yKjY7a61BlnHVwuut36rFW39jN\nc9DGjsS2xK/j7M6Rgi3d6c+Fk4dpdKh8atl4G3suGKB/hgdFwDhHv+yIqr5dUiDQ\nviBWs7mpCdbQDOfPNGxL7o3hbvm96KdoXrUWQB/83sPNhPZ3zedte5LFODMZlzb6\nxEh/W0G0TCV+6Gtpq378LUAaW7xMuRDLHI+1qDq4IhDTOrhYTmDDYNBUEspxyJVB\nTpKYO0GnqgpxkOY+xQt4qKLJLQ7COvAHt/Y8ixuIoQKBgQDe9HhqICgKTxk1vUXq\n1R2osQxFa1RPS0wXU0/teQgFBUT+trKOJfA4B7rKT4qtzKGfu0k01SHD1QWK6JHs\n/HpAGa623iQN9QLtsFZTcOMpaEgwTVwNOMBnU8TJRuglOaZnn4EQsc2Oys32fY2I\nLwUV6zETStcRJRyWt2FP3nV0UQKBgQDAMjg4yYOJLOODdDbC2lQEZr3BZicdB6i0\nzuzxF70l3ARDp7ptLke9XPlUdsBiZRl53gKiFurzpAUOGbC4qvjpO5aCHUafHbXm\nFA4uEVhAzaLSecfhmmpoowFCs8p85kOTnEBTjvoRDhX3HKrlC3MukqZmKRo7klSN\neSCv9otyzQKBgBA9sr/YU9JcbLOzc/JlT+HH8+LirKOSEproYLwlwuXKunnriRo9\nvT/3oC24mZuLeoKOPAjzNaB0VhEGXArtYWJl/IopqGqz3GDAJamyYXnUtN1/5SK5\nbZqZSY538dU0W+DUh6xVp2mtcE9yWer/sdkk5tBG9V+0Wl7IQPh2dgvhAoGBAIhz\nHvcyGfCJrfzlxPsRhhSZ3J4xqBM0HNJBFncUI3V9fomJyxE4ijYmi90rceppXGzo\n8XWiT6wqBmy8UHrK52yuoWw+3KSas0llc6vBJKbdV3uWehHxTxp6n6p7eoax88gY\nZpLsLx1soquN7sYuGtg1xW1CQR2KBf1qwYorv1UBAoGAXzIcWdo+fzxSv9vGMRAa\n5qjpWEKwlGmdWHXn1R5nxxFv9ur55Rqiut1Xw2pn344u8AnDq+4f5mbEIVOxArT+\nAZAPqNBMO9NYYouF3oDW+hvLU5JWrjfGR1KEOJcSM1e/PCNBmMNMoKauLCHXRhSh\n2LTzTUSOeIryGOTK6MoOl+Y=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-goigg@sifreyoneticisi.iam.gserviceaccount.com",
    "client_id": "107230987416345296976",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-goigg%40sifreyoneticisi.iam.gserviceaccount.com"
}

# firebase pyrebase kullanılarak bağlantısı
cred = credentials.Certificate(key)
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(config)
db = firestore.client()
users_ref = db.collection(u'users')
app = Flask(__name__)
app.secret_key = b"Batuhan    "


@app.route("/")
def anasayfa():
    return render_template("index.html")


# login ekranı
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('mail')
        password = request.form.get('pass')

        user = pb.auth().sign_in_with_email_and_password(email, password)
        jwt = user['localId']
        session['userid'] = jwt
        session['mail'] = email
        return redirect(url_for("user_page"))
    else:
        return render_template('login.html')


# kayıt ekranı aynı anda auth ve firestore arayüzüne kayıt ediyor
@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('mail')
        password = request.form.get('pass')
        if email is None or password is None:
            return "mail veya şifre eksik"
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            data = {
                "id": user.uid,
                "mail": email
            }
            users_ref.document(user.uid).set(data)
            kayitBasarili = "Kayıt Başarılı"
            return render_template("signup.html", kayitBasarili=kayitBasarili)
        except:
            kayitHatali = "Kayıt Hatası"
            return render_template("signup.html", kayitHatali=kayitHatali)
    else:
        return render_template("signup.html")


# kullanıcı ekranı yeni şifre hesaplar eklemesine yarıyor
@app.route('/user_page', methods=['POST', 'GET'])
def user_page():
    mail = session.get('mail')
    userid = session.get('userid')
    if request.method == 'POST':
        if request.form['kayit'] == 'Şifre Oluştur':
            site = request.form.get("site")
            kadi = request.form.get("kadi")
            return render_template('user_page.html', mail=mail, data=tables(), password=sifreOlustur(), site=site,
                                   kadi=kadi)
        elif request.form['kayit'] == 'Ekle':
            try:
                site = request.form.get("site")
                kadi = request.form.get("kadi")
                password = request.form.get("pass")
                data = {
                    "site": site,
                    "kadi": kadi,
                    "pass": password
                }
                users_ref.document(userid).collection("hesaplar").document(site).set(data)
                kayit = "Kayıt Başarılı"
                return render_template('user_page.html', kayit=kayit, mail=mail, data=tables())
            except:
                hata = "Hata Meydana Geldi"
                return render_template('user_page.html', hata=hata)
        elif request.form['kayit'] == 'Sil':
            return sifre_sil()
    else:
        return render_template('user_page.html', mail=mail, data=tables())


# çıkış için lazım olan kod blogu
@app.route('/logout')
def sign_out():
    session.clear()
    return redirect(url_for('login'))


@app.route('/forgetpass', methods=['POST', 'GET'])
def forget():
    if request.method == 'POST':

        email = request.form.get('mail')
        pb.auth().send_password_reset_email(email)
        gonderildi = "Şifre Değiştirme Maili Gönderildi."
        return render_template('forgetpass.html', gonderildi=gonderildi)
    else:
        return render_template('forgetpass.html')


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    userid = session.get('userid')
    auth.delete_user(userid)
    session.clear()
    return redirect(url_for('login'))


def sifre_sil():
    try:
        site = request.form.get('site')
        userid = session.get('userid')
        users_ref.document(userid).collection('hesaplar').document(site).delete()
        return redirect(url_for('user_page'))
    except:
        return redirect(url_for('user_page'))


def sifreOlustur():
    length = random.randint(8, 16)
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation
    all = lower + upper + num + symbols
    temp = random.sample(all, length)
    password = "".join(temp)
    return password


def tables():
    userid = session.get('userid')
    users = list(users_ref.document(userid).collection(u"hesaplar").stream())
    users_dict = list(map(lambda x: x.to_dict(), users))
    df = pd.DataFrame(users_dict)
    df = df.sort_index(axis=1)
    return df.values
