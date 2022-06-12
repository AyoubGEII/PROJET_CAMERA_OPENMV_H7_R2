                        ######### CODE OUENZERFI AYOUB V2.0  - 26/03/22 #########
                        
from email.mime.multipart import MIMEMultipart #Module 
from email.mime.text import MIMEText #Module pour la partie texte
import smtplib #Connexion du smtp de google ==> un serveur spéciale pour mails

print("##### RECUPERATION DES PARAMETRES CODE CAMERA #####")

msg = MIMEMultipart() # Initialisation du message
msg['From'] = "MOI@gmail.com" # Expéditeur "ici moi"
msg['To'] = "MAIL_DESTINATAIRE@gmail.com"# Destinataire du mail
password = "MOTDEPASSE A ENTRER" # Stockage du mot de passe dans une variable "en chaine de caractère"
msg['Subject'] = "Test Réception - ENS V2.0 " #Sujet du mail   
body = "Bonjour Madame, Monsieur," #Contenu du mail
body += "Voici un test de récéption assez simple pour la candidature au magistère de mécatronique. En vous remerciant."

### Début de connexion au serveur SMTP de google 

msg.attach(MIMEText(body, 'html'))
server = smtplib.SMTP("smtp.gmail.com",587) #Port 587 correspond à gmail
server.starttls()
server.login(msg['From'], password) # Connexion au compte / Récupération via l'adresse et le mdp
server.sendmail(msg['From'], msg['To'], msg.as_string()) #Envoie du mail et le message en chaine de caractère "String"

print("##### Fin du code #####")

server.quit() #FIN