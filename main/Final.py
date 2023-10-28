#!/usr/bin/env python3
# Import needed Libraries 
import pandas as pd
import requests
import time
from datetime import datetime
from datetime import date
from hijri_converter import convert
from hijri_converter import Hijri


# Date for Caption 

today = date.today()
d1 = today.strftime("%d/%m/%Y")

d2 = datetime.strptime(d1, '%d/%m/%Y')
d3 = convert.Gregorian.fromdate(d2).to_hijri()

hijri = d3

Month=hijri.month_name('ar')
Date=hijri.day_name('ar')

# Inializations

base_url_audio = "https://api.telegram.org/bot5644514978:AAH-H2_VuQQ9Xtg9hV0MIarzcFcoJarbzoE/sendAudio"
base_url_photo = "https://api.telegram.org/bot5644514978:AAH-H2_VuQQ9Xtg9hV0MIarzcFcoJarbzoE/sendPhoto"
base_url_message = "https://api.telegram.org/bot5644514978:AAH-H2_VuQQ9Xtg9hV0MIarzcFcoJarbzoE/sendMessage"

audio_base = "https://archive.org/download/Quran--alhozyfi---604-part---mp3---full/"
photo_base = "https://ia800105.us.archive.org/BookReader/BookReaderImages.php?zip=/27/items/Quran-Kareem-Khawagah-The-Blue-Page-Quran/Quran-Kareem-Khawagah-The-Blue-Page-Quran_jp2.zip&file=Quran-Kareem-Khawagah-The-Blue-Page-Quran_jp2/Quran-Kareem-Khawagah-The-Blue-Page-Quran_0"
photo_base2 = ".jp2&id=Quran-Kareem-Khawagah-The-Blue-Page-Quran&scale=4&rotate=0"

# Surat dictionary and conversion to Dataframes

data = {'name': ['الفاتحة', 'البقرة', 'ال عمران', 'النساء' , 'المائدة' , 'الأنعام' , 'الأعراف' , 'الأنفال' , 'التوبة' , 'يونس' , 'هود' , 'يوسف' , 'الرعد' , 'إبراهيم' , 'الحجر' , 'النحل' , 'الإسراء' , 'الكهف' , 'مريم' , 'طه' , ' الأنبياء' , 'الحج' , 'المؤمنون' , ' النور' , 'الفرقان'],
        'id': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25],
        'start': [1 , 2 , 50 , 77 , 106 ,128,151 ,177 ,187 ,208 ,221 ,235 ,249 ,255 ,262 ,276,282 ,293 ,305 ,312 ,322 ,332 ,342 ,350,359],
        'end':[1 , 49 , 76 , 106 , 127,150,176,186,207,221,235,248,255,261,276,281,293,304,312,321,331,341,349,359,366]} 
new_surat = pd.DataFrame.from_dict(data)
new_surat['number_of_pages'] = new_surat['end']-new_surat['start']+1


def main():
    # Read the Users CSV file into dataframes 
    users = pd.read_csv("./Users.csv")

    # Itrate over the file

    for i in range(0, len(users)):
        if users.iloc[i]['Current_Page']<10:
            Current_Page,Current_mp3 = "00"+str(users.iloc[i]['Current_Page']),"00"+str(users.iloc[i]['Current_mp3'])
        elif users.iloc[i]['Current_Page']>99:
            Current_Page,Current_mp3 = str(users.iloc[i]['Current_Page']),str(users.iloc[i]['Current_mp3'])
        else:
            Current_Page,Current_mp3 = "0"+str(users.iloc[i]['Current_Page']),"0"+str(users.iloc[i]['Current_mp3'])
        chat_id = str(users.iloc[i]['chat_id'])
        user_surat = new_surat[(new_surat["start"]<= int(Current_mp3)) & (new_surat["end"]>= int(Current_mp3))].reset_index() 
        user_surat0 = str(user_surat['name'][0])
        print (Current_Page,Current_mp3,chat_id)
        caption = user_surat0+" "+ Current_mp3+"/"+str(new_surat[new_surat['name'] == user_surat0].reset_index().end[0])
        audio_id = audio_base+Current_mp3+".mp3"
        photo_id = photo_base+Current_Page+photo_base2
    
        parameters_audio = {    "chat_id" : chat_id ,    "audio" : audio_id,    "caption" : caption    }
        parameters_photo = {    "chat_id" : chat_id ,    "photo" : photo_id ,    "caption" : caption   }
    

        #
        # Send the Salam Message
        #my_file = open("./Salam.gif", "rb")
        #caption_Salam = "هنيئا لكم مداومة حفظ كتاب الله .... استعينوا بالله و اصبروا"
        #parameters = {    "chat_id" : chat_id,    "caption" : caption_Salam     }
        #files = { "photo" : my_file}
        #requests.get(base_url_photo, data = parameters, files=files)
        
        # Send the Daily Intro Surat Name 
        my_file = open("./Daily.JPG", "rb")
        caption_Intro = Date+" " +Month+" "+str(d3)
        parameters = {    "chat_id" : chat_id,    "caption" : caption_Intro     }
        files = { "photo" : my_file}
        requests.get(base_url_photo, data = parameters, files=files)
        
        # Send the Surat Name
        #file_base=r"C:\Users\emahoma\Downloads\Quran_Python\Quran\Local_Pics/"
        #file=file_base+str(user_surat.id[0])+"Intro_new.JPG"
        #my_file = open(file, "rb")
        #parameters = {    "chat_id" : chat_id}
        #files = { "photo" : my_file}
        #requests.get(base_url_photo, data = parameters, files=files)
        
        '''
        # Send the Personalized Message 
        message = " السلام عليكم و رحمة الله و بركاته ... هنيئا لكم مداومة حفظ كتاب الله "
        parameters_text = {    "chat_id" : chat_id ,     "text" : message ,"entities":[{"offset":0,"length":4,"type":"bold"}]}
        requests.get(base_url_message, data = parameters_text)
        message = " استعينوا بالله و اصبرٍوا "
        parameters_text = {    "chat_id" : chat_id ,     "text" : message ,"entities":[{"offset":0,"length":4,"type":"bold"}]}
        requests.get(base_url_message, data = parameters_text)  
        '''     
        # Send the MP3    
        requests.get(base_url_audio, data = parameters_audio)
        # Send the Surat Page
        requests.get(base_url_photo, data = parameters_photo)
    
        users.iloc[i]['Current_Page']+=1
        users.iloc[i]['Current_mp3']+=1
        users.to_csv("./Users.csv",index=False)

main()


