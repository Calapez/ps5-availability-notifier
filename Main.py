import pyscreenshot as ImageGrab
import winsound
import smtplib

from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Out of stock colors to detect
WORTEN_YELLOW_COLOR = (255, 174, 0)  # Worten's unavailability yellow color
FNAC_RED_COLOR = (221, 30, 53)  # Fnac's unavailability red color

## Worten ##
# Physical Edition position
WORTEN_PH_SOLDOUT_POS = (499, 585)  # Position of "Esgotado" yellow label
WORTEN_PH_RETAKE_POS = (499, 585)  # Position of "Retoma..." yellow label
# Digital Edition position
WORTEN_DG_SOLDOUT_POS = (499, 585)  # Position of "Esgotado" yellow label
WORTEN_DG_RETAKE_POS = (499, 585)  # Position of "Retoma..." yellow label

## Fnac ##
# Physical Edition position
FNAC_PH_ONLINE_SOLDOUT_POS = (3452, 677)  # Position of "Indisponível online" red label
FNAC_PH_STORE_SOLDOUT_POS = (3452, 707)  # Position of "Indisponível loja" red label
# Digital Edition position
FNAC_DG_ONLINE_SOLDOUT_POS = (3452, 990)  # Position of "Indisponível online" red label
FNAC_DG_STORE_SOLDOUT_POS = (3452, 1020)  # Position of "Indisponível loja" red label

# create message object instance
msg = MIMEMultipart()
# setup the parameters of the message
password = "<INSERT ORIGIN PASSWORD>"
msg['From'] = "<INSERT ORIGIN EMAIL>"
msg['To'] = "<INSERT DESTINATION EMAIL>"
msg['Subject'] = "PS5 Available!"


# Check Worten's PS5 availability
def check_ps5_worten(px):
    if (px[WORTEN_PH_SOLDOUT_POS] != WORTEN_YELLOW_COLOR or px[WORTEN_PH_RETAKE_POS] != WORTEN_YELLOW_COLOR or px[WORTEN_DG_SOLDOUT_POS] != WORTEN_YELLOW_COLOR or px[WORTEN_DG_RETAKE_POS] != WORTEN_YELLOW_COLOR):
        return True  # Available

    return False  # Not Available


# Check Fnac's PS5 availability
def check_ps5_fnac(px):
    if (px[FNAC_PH_ONLINE_SOLDOUT_POS] != FNAC_RED_COLOR or px[FNAC_PH_STORE_SOLDOUT_POS] != FNAC_RED_COLOR or px[FNAC_DG_ONLINE_SOLDOUT_POS] != FNAC_RED_COLOR or px[FNAC_DG_STORE_SOLDOUT_POS] != FNAC_RED_COLOR):
        return True  # Available

    return False  # Not Available


## Warn user that PS5 is available ##
# Print on console
# Sound "beep"
# Send email
def warn_ps5_available(desc):
    warning_text = "\n\n=====\n=====\n=====\n=====\n" + desc + "\n\nPS5 is Available!!\n=====\n=====\n=====\n=====\n\n"

    print(warning_text)

    frequency = 2500  # Set Frequency in hertz
    duration = 500  # Set Duration in milisecs
    winsound.Beep(frequency, duration)
    winsound.Beep(frequency, duration)

    try:
        # create server
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.connect('smtp.gmail.com', '587')
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        # add in the message body
        msg.attach(MIMEText(warning_text, 'plain'))

        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print("Sent email!")
    except Exception as e:
        print("Error sending email")
        print(e)
        pass


# Last availability status
worten_last_available = False
fnac_last_available = False

while(True):
    img = ImageGrab.grab()
    img.save('image.png')  # Saves an image of the screen
    px = img.load()

    worten_now_available = check_ps5_worten(px)
    #fnac_now_available = check_ps5_fnac(px)
    fnac_now_available = False

    # If PS5 is available now and before, warn as available
    if (worten_last_available and worten_now_available):
        warn_ps5_available("Worten")

    # If PS5 is available now and before, warn as available
    if (fnac_last_available and fnac_now_available):
        warn_ps5_available("Fnac")

    # Assign current availability to last availability
    worten_last_available = worten_now_available
    fnac_last_available = fnac_now_available

    # Pages sometimes refresh and fade-out for a while, 
    # only check for PS5 every 5 secs
    sleep(5)