from tkinter import *
from tkinter import filedialog
import pandas as pd
import re
from textblob import TextBlob
from yandex.Translater import Translater


def open():
    global my_label

    root.filename=filedialog.askopenfilename(initialdir='/Desktop',title='Select a file',filetypes=(('Excel Files',"*.xlsx"),("All Files","*.*")))
    my_label=Label(root, text=root.filename).grid(row=8)

def show():
    tweet_list=[]
    df=pd.read_excel(root.filename)
    file_path=root.filename
    old_tweets=df[var.get()].head()

    #Genel Düzenleme
    file_name=file_path.split("/")[-1]
    replace_list=['rt','\n','\t']
    for tweet in df[var.get()]:
        #Replace
        tweet=str(tweet).lower()
        
        for rep in replace_list:
            tweet=tweet.replace(rep,'')
        tweet_list.append(tweet)
        
    df[f"{var.get()}"]=tweet_list

    #URL'lerin kaldırılması.
    if var1.get()==1:
        tweet_list=[]
        
        for tweet in df[f"{var.get()}"]:
            tweet=str(tweet).lower()
            tweet = re.sub(r"@\S+", "", tweet)
            tweet = re.sub(r"http\S+", "", tweet)
            stripped_tweet=tweet.strip()
            tweet_list.append(stripped_tweet)
        
        df[f"{var.get()}"]=tweet_list

    #HASTAG    
    if var2.get()==1:
        tweet_list=[]
        for tweet in df[var.get()]:
            tweet = re.sub(r"#\S+", "", tweet)
            stripped_tweet=tweet.strip()
            tweet_list.append(stripped_tweet)
        df[var.get()]=tweet_list


    #STOPWORDS 
    if var3.get()==1:
        stopwords_tr=['acaba', 'ama', 'aslında', 'az', 'bazı', 'belki', 'biri', 'birkaç', 'birşey', 'biz', 'bu', 'çok', 'çünkü', 'da', 'daha', 'de', 'defa', 'diye', 
'eğer', 'en', 'gibi', 'hem', 'hep', 'hepsi', 'her', 'hiç', 'için', 'ile', 'ise', 'kez', 'ki', 'kim', 'mı', 'mu', 'mü', 'nasıl', 'ne', 'neden', 'nerde', 'nerede', 'nereye', 'niçin', 'niye', 'o', 'sanki', 'şey', 'siz', 'şu', 'tüm', 've', 'veya', 'ya', 'yani']
        tweet_list=[]
        for tweet in df[var.get()]:
            
            for word in tweet:
                if word in stopwords_tr:tweet.replace(word,'')
               
            stripped_tweet=tweet.strip()
            tweet_list.append(stripped_tweet)
        df[var.get()]=tweet_list


    #Emojilerin kaldırılması
    if var4.get()==1:
        tweet_list=[]
        emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
        
        
        
        for tweet in df[var.get()]:
            
            tweet=emoji_pattern.sub(r'', tweet)
                
            stripped_tweet=tweet.strip()
            tweet_list.append(stripped_tweet)


        df[var.get()]=tweet_list


    #Noktalama işaretlerinin silinmesi.
    if var6.get()==1:
        df[var.get()] = df[var.get()].str.replace('[^\w\s]','')

    #Sayıların Silinmesi.
    if var7.get()==1:
        df[var.get()] = df[var.get()].str.replace('\d','')

    #Kelime Kökleri
    if var5.get()==1:
        import jpype
        # JVM başlat
        # Aşağıdaki adresleri java sürümünüze ve jar dosyasının bulunduğu klasöre göre değiştirin
        #Windows için:"C:/Program Files/Java/jdk1.8.0_221/jre/bin/server/jvm.dll"
        #Linux için:"/usr/lib/jvm/java-8-oracle/jre/lib/amd64/server/libjvm.so"
        #-Djava.class.path= zemberek-tum-2.0.jar dosyasının konumu
        jpype.startJVM("C:/Program Files/Java/jdk1.8.0_221/jre/bin/server/jvm.dll",
                "-Djava.class.path=zemberek-tum-2.0.jar", "-ea")
        # Türkiye Türkçesine göre çözümlemek için gerekli sınıfı hazırla
        Tr = jpype.JClass("net.zemberek.tr.yapi.TurkiyeTurkcesi")
        # tr nesnesini oluştur
        tr = Tr()
        # Zemberek sınıfını yükle
        Zemberek = jpype.JClass("net.zemberek.erisim.Zemberek")
        # zemberek nesnesini oluştur
        zemberek = Zemberek(tr)
        tweet_kok_list=[]
        for tweet in df[var.get()]:
            word_kok=""
            #Çözümlenecek örnek kelimeleri belirle
            for word in tweet.split():
                word=str(word)
                if word.strip()>'':
                    yanit = zemberek.kelimeCozumle(word)
                    if yanit:
                        word_kok=word_kok+" "+yanit[0].kok().icerik()
                    else:word_kok=word_kok+" "+word

            stripped_tweet=word_kok.strip()
            tweet_kok_list.append(stripped_tweet)
            
        #JVM kapat
        jpype.shutdownJVM()
        df[f"{var.get()}_kok"]=tweet_kok_list

    #Tweets Translated
    if var8.get()==1:
        tweet_translate=[]
        for tweet in df[var.get()]:
            tr = Translater()
            tr.set_key('trnsl.1.1.20200112T103030Z.3cf813734ad4302f.ec889a140c68ede9b088891ee5376f895efbae0a') # Api key found on https://translate.yandex.com/developers/keys

            print(tweet)
            
                
            tr.set_to_lang('en')
            
            try:
                tr.set_text(tweet)
                tweet_translate.append(tr.translate())
            except:
                tweet_translate.append("-")
        
    
            
            
        df['tweets_translated']=tweet_translate
                
    
    #Tweets Sentiment Analyssis
    if var9.get()==1:
        tweet_sent=[]
        for tweet in df['tweets_translated']:
            
            testimonial=TextBlob(f"{tweet}")
            tweet_sent_analyssis=testimonial.sentiment.polarity
            
            if tweet_sent_analyssis==0:
                tweet_sent.append('Notr')
                print('Notr')
            elif tweet_sent_analyssis>0:
                tweet_sent.append('Positive')
                print('Positive')
            else:tweet_sent.append('Negative')
        df['tweets_sent']=tweet_sent
    old_df=pd.read_excel(root.filename)

    #Saving Excel File
    new_file_name=file_name.split('.')[0]+'_cleaned_.'+file_name.split('.')[1]
    df.to_excel(new_file_name)




root= Tk()
root.title('Data Preprocessing')

my_button=Button(root , text='Open File' , command=open,padx=150).grid(row=0,columnspan=2)


#VARİABLE
var,var1,var2,var3,var4,var5,var6,var7,var8,var9=StringVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar()

#COLUMNS NAME
columns_name_label=Label(root,text='Enter the column name.').grid(row=1,column=0)
columns_name=Entry(root,textvariable=var).grid(row=1,column=1)

#CHECK BUTTONS
url_check=Checkbutton(root, text="Removing URL's.",variable=var1).grid(row=3,column=0,sticky=W)
hastag_check=Checkbutton(root, text="Removing Hastag's (#).",variable=var2).grid(row=3,column=1,sticky=W)
stopwords_check=Checkbutton(root, text="Removing StopWords.",variable=var3).grid(row=5,column=1,sticky=W)
emoji_check=Checkbutton(root, text="Removing emoji.",variable=var4).grid(row=4,column=1,sticky=W)
kok_check=Checkbutton(root, text="Lemmaztization.",variable=var5).grid(row=6,column=0,sticky=W)
nokta_check=Checkbutton(root, text="Removing punctuation.",variable=var6).grid(row=5,column=0,sticky=W)
sayi_check=Checkbutton(root, text="Removing digits.",variable=var7).grid(row=4,column=0,sticky=W)
trans_check=Checkbutton(root, text="Translate to English.",variable=var8).grid(row=6,column=1,sticky=W)
sent_check=Checkbutton(root, text="Do Sentiment Analysis.",variable=var9).grid(row=7,column=0,sticky=W)
#Run Button
check_button=Button(root,text='Run!',command=show,padx=50,justify=CENTER).grid(row=7,column=1)



root.mainloop()
