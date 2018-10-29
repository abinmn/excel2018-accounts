from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from register.validators import redundantmail
from register.validators import number
from register.validators import redundantmailforpaid
from register.validators import redundantnum
from register.validators import redundantnumforpaid
from register.validators import validatemail
from register.models import userinfo
from controlroom.models import event


class RegistrationForm(forms.Form):

    TRUE_FALSE_CHOICES = (
        ('', "Stay"),
        (1, "Yes"),
        (0, "No"),)
    COLLEGES = (
        ('','College'),
        ("Model engineering College","Model engineering College"),
        ("XMEC","XMEC"),
        ("A.W.H. polytechnic College, Pattyilkunnu",	"A.W.H. polytechnic College, Pattyilkunnu"),
        ("ACE college of engineering",	"ACE college of engineering"),
        ("Acquinas College, EdaCochin",	"Acquinas College, EdaCochin"),
        ("Adi shankara institute of engineering and technology",	"Adi shankara institute of engineering and technology"),
        ("Ahalya school of engineering and technology",	"Ahalya school of engineering and technology"),
        ("Al ameen college of engineering",	"Al ameen college of engineering"),
        ("Al Azhar Engineering College",	"Al Azhar Engineering College"),
        ("Al-amee  college Edathala",	"Al-amee  college Edathala"),
        ("Albertian Institute of Science and Technology, kalamassery",	"Albertian Institute of Science and Technology, kalamassery"),
        ("Alphonsa College Pala, Pala, Kerala",	"Alphonsa College Pala, Pala, Kerala"),
        ("Amal Jyothi College of Engineering, Kanjirapally - Erumely Road, Koovappally, Kerala",	"Amal Jyothi College of Engineering, Kanjirapally - Erumely Road, Koovappally, Kerala"),
        ("Ammini college of engineering and technology",	"Ammini college of engineering and technology"),
        ("Amrita School of Arts and Science , Cochin",	"Amrita School of Arts and Science , Cochin"),
        ("Amritha College , Thalassery",	"Amritha College , Thalassery"),
        ("Amritha college of engineering,Kollam",	"Amritha college of engineering,Kollam"),
        ("Archana College of Engineering, Alappuzha",	"Archana College of Engineering, Alappuzha"),
        ("Aryanet institute of technology",	"Aryanet institute of technology"),
        ("Assumption College, Changanassery, Kerala",	"Assumption College, Changanassery, Kerala"),
        ("Axis College of Engineering & Technology",	"Axis College of Engineering & Technology"),
        ("B.C.M College For Women, Kottayam, Kerala",	"B.C.M College For Women, Kottayam, Kerala"),
        ("Baselius College, Kottayam, Kerala",	"Baselius College, Kottayam, Kerala"),
        ("Baselius Poulose II Catholicate College , Ernakulam",	"Baselius Poulose II Catholicate College , Ernakulam"),
        ("Basellious Mathews College of Engineering",	"Basellious Mathews College of Engineering"),
        ("Bharathamatha College , Ernakulam",	"Bharathamatha College , Ernakulam"),
        ("Bishop Jerome Institute of Science and Technology, Kollam",	"Bishop Jerome Institute of Science and Technology, Kollam"),
        ("Caarmel Engineering College, Ranni",	"Caarmel Engineering College, Ranni"),
        ("Calicut University Institute of Engineering & Technology, Malappuram ",	"Calicut University Institute of Engineering & Technology, Malappuram "),
        ("Christ College of Engineering, Irinjalakuda",	"Christ College of Engineering, Irinjalakuda"),
        ("CMS College, Kottayam, Kerala",	"CMS College, Kottayam, Kerala"),
        ("Co-Operative Institute of Technology, Vadakara",	"Co-Operative Institute of Technology, Vadakara"),
        ("Cochin College , Cochin ",	"Cochin College , Cochin "),
        ("College of Engineering , Munnar",	"College of Engineering , Munnar"),
        ("College of Engineering & Management, Punnapra",	"College of Engineering & Management, Punnapra"),
        ("College of Engineering and technology,payyanur",	"College of Engineering and technology,payyanur"),
        ("College of Engineering Karunagapally, Kollam",	"College of Engineering Karunagapally, Kollam"),
        ("College of Engineering Poonjar, Poonjar, Kerala",	"College of Engineering Poonjar, Poonjar, Kerala"),
        ("College OF Engineering, Adoor",	"College OF Engineering, Adoor"),
        ("College of engineering, Attingal",	"College of engineering, Attingal"),
        ("College of Engineering, Chengannur",	"College of Engineering, Chengannur"),
        ("College of Engineering, Cherthala",	"College of Engineering, Cherthala"),
        ("College Of Engineering, Kalloopara",	"College Of Engineering, Kalloopara"),
        ("College of Engineering, Kidangoor, Kidangoor, Kerala",	"College of Engineering, Kidangoor, Kidangoor, Kerala"),
        ("College of Engineering, Kottarakkara",	"College of Engineering, Kottarakkara"),
        ("College of engineering, Trikaripur ",	"College of engineering, Trikaripur "),
        ("College of Engineering,Thalassery",	"College of Engineering,Thalassery"),
        ("College of Engineerning, Trivandrum",	"College of Engineerning, Trivandrum"),
        ("CUCEK, puliincunnu",	"CUCEK, puliincunnu"),
    ("CUSAT","CUSAT"),
    ("Devaki Amma's Guruvayurappan College of Architecture, Malappuram",	"Devaki Amma's Guruvayurappan College of Architecture, Malappuram"),
    ("DOEACC Centre(NIELIT) , Calicut",	"DOEACC Centre(NIELIT) , Calicut"),
    ("ER and DCI institute of technology",	"ER and DCI institute of technology"),
    ("Eranad College City Technical Campus",	"Eranad College City Technical Campus"),
    ("Federal institute of science and technology ",	"Federal institute of science and technology "),
    ("Focus Institute of Science and Technology, Poomala, Thrissur",	"Focus Institute of Science and Technology, Poomala, Thrissur"),
    ("Government College of Engineering, Calicut",	"Government College of Engineering, Calicut"),
    ("Government college of engineering,sreekrishnapuram",	"Government college of engineering,sreekrishnapuram"),
    ("Government Engineering College, Idukki",	"Government Engineering College, Idukki"),
    ("Government Engineering College, Thrissur",	"Government Engineering College, Thrissur"),
    ("Government Engineering College, Wayanad",	"Government Engineering College, Wayanad"),
    ("Govt college of engineering, Barton Hill",	"Govt college of engineering, Barton Hill"),
    ("Govt Poly technic Calicut",	"Govt Poly technic Calicut"),
    ("Govt. College Manimalakunnu",	"Govt. College Manimalakunnu"),
    ("Govt. College of Engineering, Parassinikadavu",	"Govt. College of Engineering, Parassinikadavu"),
    ("Govt. College Thripunithara ",	"Govt. College Thripunithara "),
    ("Govt. Polytechnic College , Mattanur",	"Govt. Polytechnic College , Mattanur"),
    ("Govt. Polytechnic College, Perinthalmanna",	"Govt. Polytechnic College, Perinthalmanna"),
    ("Govt. Sanskrit College Thripunithara",	"Govt. Sanskrit College Thripunithara"),
    ("Hindusthan College of Engineering",	"Hindusthan College of Engineering"),
    ("Holy Grace Academy of Engineering for Women",	"Holy Grace Academy of Engineering for Women"),
    ("IES College of Engineering",	"IES College of Engineering"),
    ("IIT Palakkad",	"IIT Palakkad"),
    ("Ilahia College of Arts and Science , Muvattupuzha",	"Ilahia College of Arts and Science , Muvattupuzha"),
    ("Ilahia Engineering College",	"Ilahia Engineering College"),
    ("Indhira Gandhi Polytechnic College , Mahe",	"Indhira Gandhi Polytechnic College , Mahe"),
    ("Indian institute of space science and technology",	"Indian institute of space science and technology"),
    ("Indira Gandhi Institute of Engineering & Technology for Women,Nellikuzhi, Kothamangalam, Ernakulam",	"Indira Gandhi Institute of Engineering & Technology for Women,Nellikuzhi, Kothamangalam, Ernakulam"),
    ("International School Of Photonics Cochin",	"International School Of Photonics Cochin"),
    ("Jai Bharath College of Management & Engineering Technology, Ernakulam, Arackappady, Vengola, Perumbavoor",	"Jai Bharath College of Management & Engineering Technology, Ernakulam, Arackappady, Vengola, Perumbavoor"),
    ("Jawaharlal college of engineering and technology",	"Jawaharlal college of engineering and technology"),
    ("John Cox memorial CSI institute of technology",	"John Cox memorial CSI institute of technology"),
    ("Jyothi Engineering College, Cheruthuruthy",	"Jyothi Engineering College, Cheruthuruthy"),
    ("K.M.C.T College of Engineering for Women, Calicut",	"K.M.C.T College of Engineering for Women, Calicut"),
    ("K.M.C.T. College of Engineering, Mukkam",	"K.M.C.T. College of Engineering, Mukkam"),
    ("K.M.E.A. Engineering College, Edathala",	"K.M.E.A. Engineering College, Edathala"),
    ("K.R. Gouri Amma College of Engineering for Women, Alappuzha",	"K.R. Gouri Amma College of Engineering for Women, Alappuzha"),
    ("Kannur University Thavakkara ",	"Kannur University Thavakkara "),
    ("Kelappaji College of Agricultural Engneering & Technology ,Malappuram",	"Kelappaji College of Agricultural Engneering & Technology ,Malappuram"),
    ("Kesari Arts and Science College, N.paravur",	"Kesari Arts and Science College, N.paravur"),
    ("Kits college,chengalam East, Kottayam, Pallickathode",	"Kits college,chengalam East, Kottayam, Pallickathode"),
    ("Kuriakose Elias College, Mannanam, Kerala",	"Kuriakose Elias College, Mannanam, Kerala"),
    ("kvm college of engineering and information technology, kokkothamangalam",	"kvm college of engineering and information technology, kokkothamangalam"),
    ("LBS College Of engineering,  Kasaragod ",	"LBS College Of engineering,  Kasaragod "),
    ("LBS institute of technology",	"LBS institute of technology"),
    ("Little Flower College of Engineering, Kalamassery",	"Little Flower College of Engineering, Kalamassery"),
    ("Lourdes matha college of science and technology",	"Lourdes matha college of science and technology"),
    ("M.E.S College of Advanced Studies, Aluva, Marampilly",	"M.E.S College of Advanced Studies, Aluva, Marampilly"),
    ("M.E.S. Institute of Technology & Management, Kollam",	"M.E.S. Institute of Technology & Management, Kollam"),
    ("Maharajas College, Pallimukku",	"Maharajas College, Pallimukku"),
    ("Malabar College of Engineering and Technology",	"Malabar College of Engineering and Technology"),
    ("Malabar Institute of Technology, Anjarakandi",	"Malabar Institute of Technology, Anjarakandi"),
    ("Mangalam College of Engineering, Ettumanoor, Kerala",	"Mangalam College of Engineering, Ettumanoor, Kerala"),
    ("Mar Athanasias College Kothamangalam",	"Mar Athanasias College Kothamangalam"),
    ("Mar Baselios Christian College of Engineering and Technology, Idukki",	"Mar Baselios Christian College of Engineering and Technology, Idukki"),
    ("Mar baselios college of engineering and technology",	"Mar baselios college of engineering and technology"),
    ("Mar Baselios Institute of Technology & Science, Ernakulam, kothamangalam",	"Mar Baselios Institute of Technology & Science, Ernakulam, kothamangalam"),
    ("Mar Baselios Thomas Catholicose college of engneering, koothattukulam ,Ernakulam",	"Mar Baselios Thomas Catholicose college of engneering, koothattukulam ,Ernakulam"),
    ("Mar Thoma Institute of Information Technology",	"Mar Thoma Institute of Information Technology"),
    ("Marian engineering college, Kazhakuttam",	"Marian engineering college, Kazhakuttam"),
    ("Marthoma College for Women, Perumbavoor, Cochin",	"Marthoma College for Women, Perumbavoor, Cochin"),
    ("MEA College of Engineering ,Perinthalmanna",	"MEA College of Engineering ,Perinthalmanna"),
    ("MES College of Engineering,Kuttippuram",	"MES College of Engineering,Kuttippuram"),
    ("Model Polytechnic College, Painavu",	"Model Polytechnic College, Painavu"),
    ("Model Polytechnic College, Vadakara",	"Model Polytechnic College, Vadakara"),
    ("Mohandas college of engineering and technology",	"Mohandas college of engineering and technology"),
    ("Morning Star Home Science College, Angamaly",	"Morning Star Home Science College, Angamaly"),
    ("Mount Zion College of Engineering for Women, Chengannur",	"Mount Zion College of Engineering for Women, Chengannur"),
    ("Mount Zion College Of Engineering, Kadammanitta",	"Mount Zion College Of Engineering, Kadammanitta"),
    ("Musaliar College Of Engineering, Pathanamthitta",	"Musaliar College Of Engineering, Pathanamthitta"),
    ("Muthoot Institute of Science and Technology , kolenchery",	"Muthoot Institute of Science and Technology , kolenchery"),
    ("National Institute of Technology, Calicut",	"National Institute of Technology, Calicut"),
    ("Nehru College of Engineering & Research Centre, Thrissur",	"Nehru College of Engineering & Research Centre, Thrissur"),
    ("Nirmala College of Engineering",	"Nirmala College of Engineering"),
    ("Nirmala College, Muvattupuzha, Ernakulam",	"Nirmala College, Muvattupuzha, Ernakulam"),
    ("North Malabar Institute of Technology ",	"North Malabar Institute of Technology "),
    ("NSS College of engineering",	"NSS College of engineering"),
    ("Presentation College of Applied Sciences, Puthenvelikara, Ernakulam",	"Presentation College of Applied Sciences, Puthenvelikara, Ernakulam"),
    ("Prime college of engineering",	"Prime college of engineering"),
    ("Providence college of engineering,chengannur",	"Providence college of engineering,chengannur"),
    ("R.L.V College of Music and Institute of Fine Arts , Ernakulam",	"R.L.V College of Music and Institute of Fine Arts , Ernakulam"),
    ("Rajadhani Institute of engineering and technology",	"Rajadhani Institute of engineering and technology"),
    ("Rajagiri College of Social Science, Ernakulam",	"Rajagiri College of Social Science, Ernakulam"),
    ("Rajagiri School of Engineering and Technology, Ernakulam",	"Rajagiri School of Engineering and Technology, Ernakulam"),
    ("Rajiv Gandhi Institute of Technology, Kerala",	"Rajiv Gandhi Institute of Technology, Kerala"),
    ("Royal College of Engineering & Technology",	"Royal College of Engineering & Technology"),
    ("S.C.M.S. School of Engineering and Technology, Cochin, karukutty",	"S.C.M.S. School of Engineering and Technology, Cochin, karukutty"),
    ("S.S.V. College, Cochin",	"S.S.V. College, Cochin"),
    ("Sacred Heart College, Ernakulam",	"Sacred Heart College, Ernakulam"),
    ("Sahrdaya College of Engineering and Technology",	"Sahrdaya College of Engineering and Technology"),
    ("saint dominic's college",	"saint dominic's college"),
    ("Saintgits College of Engineering, Pathamuttam, Kerala",	"Saintgits College of Engineering, Pathamuttam, Kerala"),
    ("Sankar Institute of Science and Technology",	"Sankar Institute of Science and Technology"),
    ("Sarabhai Institute of science and technology",	"Sarabhai Institute of science and technology"),
    ("SHM Engineering College",	"SHM Engineering College"),
    ("SJCET, Choondacherry, Kerala",	"SJCET, Choondacherry, Kerala"),
    ("Southern College of Engineering & Technology",	"Southern College of Engineering & Technology"),
    ("Sree Buddha College Of Engineering for Women, Muttathukonam",	"Sree Buddha College Of Engineering for Women, Muttathukonam"),
    ("Sree Buddha College of Engineering, Alappuzha",	"Sree Buddha College of Engineering, Alappuzha"),
    ("Sree Eranakulathappan College of Engineering and Management",	"Sree Eranakulathappan College of Engineering and Management"),
    ("Sree Narayana Guru College of Engineering & Technology, Chalakode",	"Sree Narayana Guru College of Engineering & Technology, Chalakode"),
    ("Sree Narayana Gurukulam College of Engineeing, Kolenchery",	"Sree Narayana Gurukulam College of Engineeing, Kolenchery"),
    ("Sree Narayana Mangalam Institute of Management and Technology, Moothakunnam, maliyankara",	"Sree Narayana Mangalam Institute of Management and Technology, Moothakunnam, maliyankara"),
    ("Sree Sankaracharya University of Sanskrit, Kalady",	"Sree Sankaracharya University of Sanskrit, Kalady"),
    ("Sree Vellappally Natesan College of Engineering,	Alappuzha",	"Sree Vellappally Natesan College of Engineering,  Alappuzha"),
    ("Sreepathy institute of science and technology",	"Sreepathy institute of science and technology"),
    ("Sri chithra thrirunal college of engineering",	"Sri chithra thrirunal college of engineering"),
    ("St thomas college of engineering, chengannur",	"St thomas college of engineering, chengannur"),
    ("St Thomas institute of science and technology",	"St Thomas institute of science and technology"),
    ("St. Alberts College, Cochin",	"St. Alberts College, Cochin"),
    ("St. Berchmans College, Changanassery, Kerala",	"St. Berchmans College, Changanassery, Kerala"),
    ("St. Pauls College, Ernakulam",	"St. Pauls College, Ernakulam"),
    ("St. Peters College, Kolenchery, Ernakulam",	"St. Peters College, Kolenchery, Ernakulam"),
    ("St. Teresa's College, Cochin",	"St. Teresa's College, Cochin"),
    ("St. Thomas College of Engineering & Technology, Sivapuram",	"St. Thomas College of Engineering & Technology, Sivapuram"),
    ("St. Xaviers College for Women, Aluva",	"St. Xaviers College for Women, Aluva"),
    ("St.George's College, Saint George College Road, Aruvithura, Erattupetta, Kerala",	"St.George's College, Saint George College Road, Aruvithura, Erattupetta, Kerala"),
    ("St.Thomas College Pala, Arunapuram, Pala, Kerala",	"St.Thomas College Pala, Arunapuram, Pala, Kerala"),
    ("T.K.M. College of Engineering, Kollam",	"T.K.M. College of Engineering, Kollam"),
    ("T.O.C.H. Institute of Science and Technology, Mookannur, angamaly",	"T.O.C.H. Institute of Science and Technology, Mookannur, angamaly"),
    ("Thejus Engineering College",	"Thejus Engineering College"),
    ("Travancore Engineering College, Kollam",	"Travancore Engineering College, Kollam"),
    ("U.K.F. College of Engineering & Technology, Kollam",	"U.K.F. College of Engineering & Technology, Kollam"),
    ("Universal Engineering College",	"Universal Engineering College"),
    ("University college of engineering",	"University college of engineering"),
    ("University College of Engineering, muttom",	"University College of Engineering, muttom"),
    ("Veda Vyasa Institute of Technology , Karadparamba",	"Veda Vyasa Institute of Technology , Karadparamba"),
    ("Vidya Academy of Science and Technology",	"Vidya Academy of Science and Technology"),
    ("Vimal Jyothi Engineering College, Chemperi",	"Vimal Jyothi Engineering College, Chemperi"),
    ("Viswa Jyothi College of Engineering and Technology, Muvattupuzha",	"Viswa Jyothi College of Engineering and Technology, Muvattupuzha"),
    ("VJCET, Vazhakullam",	"VJCET, Vazhakullam"),
    ("VKCET Chavarcode",	"VKCET Chavarcode"),
    ("Younus College of Engineering for Women, Kollam",	"Younus College of Engineering for Women, Kollam"),
    ("Others","Others")
    )

    name=forms.CharField(max_length=50,required=True,label='',widget=forms.TextInput(attrs={
        "placeholder":"Full Name",
        "class":"form-control",
        "style":"height:50px;margin-bottom:10px;"
    }))
    college=forms.ChoiceField(choices = COLLEGES,label='',widget=forms.Select(attrs={
        "placeholder":"College",
        "class":"form-control",
        "style":"height:50px;margin-bottom:10px;"
    }))
    email=forms.EmailField(required=False,label='',validators=[redundantmail,],widget=forms.TextInput(attrs={
        "placeholder":"Email Address",
        "class":"form-control",
        "style":"height:50px;margin-bottom:10px;"
    }))
    phone=forms.CharField(max_length=10,min_length=10,label='',validators=[number,redundantnum],widget=forms.TextInput(attrs={
        "placeholder":"Phone Number",
        "class":"form-control",
        "style":"height:50px;margin-bottom:10px;"
    }))
    # stay=forms.TypedChoiceField(coerce=lambda x: bool(int(x)),choices = TRUE_FALSE_CHOICES,label='',widget=forms.Select(attrs={
    #     "placeholder":"Stay Required",
    #     "class":"form-control",
    #     "style":"height:50px;margin-bottom:20px;"
    # }))
    def clean(self):
        super(RegistrationForm,self).clean()

class PaidRegistrationForm(forms.Form):

    TRUE_FALSE_CHOICES = (
        ('',"Stay"),
        (1, "Yes"),
        (0, "No"))
    COLLEGES = (
        ('','College'),
        ("Model engineering College","Model engineering College"),
        ("XMEC","XMEC"),
        ("A.W.H. polytechnic College, Pattyilkunnu",	"A.W.H. polytechnic College, Pattyilkunnu"),
        ("ACE college of engineering",	"ACE college of engineering"),
        ("Acquinas College, EdaCochin",	"Acquinas College, EdaCochin"),
        ("Adi shankara institute of engineering and technology",	"Adi shankara institute of engineering and technology"),
        ("Ahalya school of engineering and technology",	"Ahalya school of engineering and technology"),
        ("Al ameen college of engineering",	"Al ameen college of engineering"),
        ("Al Azhar Engineering College",	"Al Azhar Engineering College"),
        ("Al-amee  college Edathala",	"Al-amee  college Edathala"),
        ("Albertian Institute of Science and Technology, kalamassery",	"Albertian Institute of Science and Technology, kalamassery"),
        ("Alphonsa College Pala, Pala, Kerala",	"Alphonsa College Pala, Pala, Kerala"),
        ("Amal Jyothi College of Engineering, Kanjirapally - Erumely Road, Koovappally, Kerala",	"Amal Jyothi College of Engineering, Kanjirapally - Erumely Road, Koovappally, Kerala"),
        ("Ammini college of engineering and technology",	"Ammini college of engineering and technology"),
        ("Amrita School of Arts and Science , Cochin",	"Amrita School of Arts and Science , Cochin"),
        ("Amritha College , Thalassery",	"Amritha College , Thalassery"),
        ("Amritha college of engineering,Kollam",	"Amritha college of engineering,Kollam"),
        ("Archana College of Engineering, Alappuzha",	"Archana College of Engineering, Alappuzha"),
        ("Aryanet institute of technology",	"Aryanet institute of technology"),
        ("Assumption College, Changanassery, Kerala",	"Assumption College, Changanassery, Kerala"),
        ("Axis College of Engineering & Technology",	"Axis College of Engineering & Technology"),
        ("B.C.M College For Women, Kottayam, Kerala",	"B.C.M College For Women, Kottayam, Kerala"),
        ("Baselius College, Kottayam, Kerala",	"Baselius College, Kottayam, Kerala"),
        ("Baselius Poulose II Catholicate College , Ernakulam",	"Baselius Poulose II Catholicate College , Ernakulam"),
        ("Basellious Mathews College of Engineering",	"Basellious Mathews College of Engineering"),
        ("Bharathamatha College , Ernakulam",	"Bharathamatha College , Ernakulam"),
        ("Bishop Jerome Institute of Science and Technology, Kollam",	"Bishop Jerome Institute of Science and Technology, Kollam"),
        ("Caarmel Engineering College, Ranni",	"Caarmel Engineering College, Ranni"),
        ("Calicut University Institute of Engineering & Technology, Malappuram ",	"Calicut University Institute of Engineering & Technology, Malappuram "),
        ("Christ College of Engineering, Irinjalakuda",	"Christ College of Engineering, Irinjalakuda"),
        ("CMS College, Kottayam, Kerala",	"CMS College, Kottayam, Kerala"),
        ("Co-Operative Institute of Technology, Vadakara",	"Co-Operative Institute of Technology, Vadakara"),
        ("Cochin College , Cochin ",	"Cochin College , Cochin "),
        ("College of Engineering , Munnar",	"College of Engineering , Munnar"),
        ("College of Engineering & Management, Punnapra",	"College of Engineering & Management, Punnapra"),
        ("College of Engineering and technology,payyanur",	"College of Engineering and technology,payyanur"),
        ("College of Engineering Karunagapally, Kollam",	"College of Engineering Karunagapally, Kollam"),
        ("College of Engineering Poonjar, Poonjar, Kerala",	"College of Engineering Poonjar, Poonjar, Kerala"),
        ("College OF Engineering, Adoor",	"College OF Engineering, Adoor"),
        ("College of engineering, Attingal",	"College of engineering, Attingal"),
        ("College of Engineering, Chengannur",	"College of Engineering, Chengannur"),
        ("College of Engineering, Cherthala",	"College of Engineering, Cherthala"),
        ("College Of Engineering, Kalloopara",	"College Of Engineering, Kalloopara"),
        ("College of Engineering, Kidangoor, Kidangoor, Kerala",	"College of Engineering, Kidangoor, Kidangoor, Kerala"),
        ("College of Engineering, Kottarakkara",	"College of Engineering, Kottarakkara"),
        ("College of engineering, Trikaripur ",	"College of engineering, Trikaripur "),
        ("College of Engineering,Thalassery",	"College of Engineering,Thalassery"),
        ("College of Engineerning, Trivandrum",	"College of Engineerning, Trivandrum"),
        ("CUCEK, puliincunnu",	"CUCEK, puliincunnu"),
    ("CUSAT","CUSAT"),
    ("Devaki Amma's Guruvayurappan College of Architecture, Malappuram",	"Devaki Amma's Guruvayurappan College of Architecture, Malappuram"),
    ("DOEACC Centre(NIELIT) , Calicut",	"DOEACC Centre(NIELIT) , Calicut"),
    ("ER and DCI institute of technology",	"ER and DCI institute of technology"),
    ("Eranad College City Technical Campus",	"Eranad College City Technical Campus"),
    ("Federal institute of science and technology ",	"Federal institute of science and technology "),
    ("Focus Institute of Science and Technology, Poomala, Thrissur",	"Focus Institute of Science and Technology, Poomala, Thrissur"),
    ("Government College of Engineering, Calicut",	"Government College of Engineering, Calicut"),
    ("Government college of engineering,sreekrishnapuram",	"Government college of engineering,sreekrishnapuram"),
    ("Government Engineering College, Idukki",	"Government Engineering College, Idukki"),
    ("Government Engineering College, Thrissur",	"Government Engineering College, Thrissur"),
    ("Government Engineering College, Wayanad",	"Government Engineering College, Wayanad"),
    ("Govt college of engineering, Barton Hill",	"Govt college of engineering, Barton Hill"),
    ("Govt Poly technic Calicut",	"Govt Poly technic Calicut"),
    ("Govt. College Manimalakunnu",	"Govt. College Manimalakunnu"),
    ("Govt. College of Engineering, Parassinikadavu",	"Govt. College of Engineering, Parassinikadavu"),
    ("Govt. College Thripunithara ",	"Govt. College Thripunithara "),
    ("Govt. Polytechnic College , Mattanur",	"Govt. Polytechnic College , Mattanur"),
    ("Govt. Polytechnic College, Perinthalmanna",	"Govt. Polytechnic College, Perinthalmanna"),
    ("Govt. Sanskrit College Thripunithara",	"Govt. Sanskrit College Thripunithara"),
    ("Hindusthan College of Engineering",	"Hindusthan College of Engineering"),
    ("Holy Grace Academy of Engineering for Women",	"Holy Grace Academy of Engineering for Women"),
    ("IES College of Engineering",	"IES College of Engineering"),
    ("IIT Palakkad",	"IIT Palakkad"),
    ("Ilahia College of Arts and Science , Muvattupuzha",	"Ilahia College of Arts and Science , Muvattupuzha"),
    ("Ilahia Engineering College",	"Ilahia Engineering College"),
    ("Indhira Gandhi Polytechnic College , Mahe",	"Indhira Gandhi Polytechnic College , Mahe"),
    ("Indian institute of space science and technology",	"Indian institute of space science and technology"),
    ("Indira Gandhi Institute of Engineering & Technology for Women,Nellikuzhi, Kothamangalam, Ernakulam",	"Indira Gandhi Institute of Engineering & Technology for Women,Nellikuzhi, Kothamangalam, Ernakulam"),
    ("International School Of Photonics Cochin",	"International School Of Photonics Cochin"),
    ("Jai Bharath College of Management & Engineering Technology, Ernakulam, Arackappady, Vengola, Perumbavoor",	"Jai Bharath College of Management & Engineering Technology, Ernakulam, Arackappady, Vengola, Perumbavoor"),
    ("Jawaharlal college of engineering and technology",	"Jawaharlal college of engineering and technology"),
    ("John Cox memorial CSI institute of technology",	"John Cox memorial CSI institute of technology"),
    ("Jyothi Engineering College, Cheruthuruthy",	"Jyothi Engineering College, Cheruthuruthy"),
    ("K.M.C.T College of Engineering for Women, Calicut",	"K.M.C.T College of Engineering for Women, Calicut"),
    ("K.M.C.T. College of Engineering, Mukkam",	"K.M.C.T. College of Engineering, Mukkam"),
    ("K.M.E.A. Engineering College, Edathala",	"K.M.E.A. Engineering College, Edathala"),
    ("K.R. Gouri Amma College of Engineering for Women, Alappuzha",	"K.R. Gouri Amma College of Engineering for Women, Alappuzha"),
    ("Kannur University Thavakkara ",	"Kannur University Thavakkara "),
    ("Kelappaji College of Agricultural Engneering & Technology ,Malappuram",	"Kelappaji College of Agricultural Engneering & Technology ,Malappuram"),
    ("Kesari Arts and Science College, N.paravur",	"Kesari Arts and Science College, N.paravur"),
    ("Kits college,chengalam East, Kottayam, Pallickathode",	"Kits college,chengalam East, Kottayam, Pallickathode"),
    ("Kuriakose Elias College, Mannanam, Kerala",	"Kuriakose Elias College, Mannanam, Kerala"),
    ("kvm college of engineering and information technology, kokkothamangalam",	"kvm college of engineering and information technology, kokkothamangalam"),
    ("LBS College Of engineering,  Kasaragod ",	"LBS College Of engineering,  Kasaragod "),
    ("LBS institute of technology",	"LBS institute of technology"),
    ("Little Flower College of Engineering, Kalamassery",	"Little Flower College of Engineering, Kalamassery"),
    ("Lourdes matha college of science and technology",	"Lourdes matha college of science and technology"),
    ("M.E.S College of Advanced Studies, Aluva, Marampilly",	"M.E.S College of Advanced Studies, Aluva, Marampilly"),
    ("M.E.S. Institute of Technology & Management, Kollam",	"M.E.S. Institute of Technology & Management, Kollam"),
    ("Maharajas College, Pallimukku",	"Maharajas College, Pallimukku"),
    ("Malabar College of Engineering and Technology",	"Malabar College of Engineering and Technology"),
    ("Malabar Institute of Technology, Anjarakandi",	"Malabar Institute of Technology, Anjarakandi"),
    ("Mangalam College of Engineering, Ettumanoor, Kerala",	"Mangalam College of Engineering, Ettumanoor, Kerala"),
    ("Mar Athanasias College Kothamangalam",	"Mar Athanasias College Kothamangalam"),
    ("Mar Baselios Christian College of Engineering and Technology, Idukki",	"Mar Baselios Christian College of Engineering and Technology, Idukki"),
    ("Mar baselios college of engineering and technology",	"Mar baselios college of engineering and technology"),
    ("Mar Baselios Institute of Technology & Science, Ernakulam, kothamangalam",	"Mar Baselios Institute of Technology & Science, Ernakulam, kothamangalam"),
    ("Mar Baselios Thomas Catholicose college of engneering, koothattukulam ,Ernakulam",	"Mar Baselios Thomas Catholicose college of engneering, koothattukulam ,Ernakulam"),
    ("Mar Thoma Institute of Information Technology",	"Mar Thoma Institute of Information Technology"),
    ("Marian engineering college, Kazhakuttam",	"Marian engineering college, Kazhakuttam"),
    ("Marthoma College for Women, Perumbavoor, Cochin",	"Marthoma College for Women, Perumbavoor, Cochin"),
    ("MEA College of Engineering ,Perinthalmanna",	"MEA College of Engineering ,Perinthalmanna"),
    ("MES College of Engineering,Kuttippuram",	"MES College of Engineering,Kuttippuram"),
    ("Model Polytechnic College, Painavu",	"Model Polytechnic College, Painavu"),
    ("Model Polytechnic College, Vadakara",	"Model Polytechnic College, Vadakara"),
    ("Mohandas college of engineering and technology",	"Mohandas college of engineering and technology"),
    ("Morning Star Home Science College, Angamaly",	"Morning Star Home Science College, Angamaly"),
    ("Mount Zion College of Engineering for Women, Chengannur",	"Mount Zion College of Engineering for Women, Chengannur"),
    ("Mount Zion College Of Engineering, Kadammanitta",	"Mount Zion College Of Engineering, Kadammanitta"),
    ("Musaliar College Of Engineering, Pathanamthitta",	"Musaliar College Of Engineering, Pathanamthitta"),
    ("Muthoot Institute of Science and Technology , kolenchery",	"Muthoot Institute of Science and Technology , kolenchery"),
    ("National Institute of Technology, Calicut",	"National Institute of Technology, Calicut"),
    ("Nehru College of Engineering & Research Centre, Thrissur",	"Nehru College of Engineering & Research Centre, Thrissur"),
    ("Nirmala College of Engineering",	"Nirmala College of Engineering"),
    ("Nirmala College, Muvattupuzha, Ernakulam",	"Nirmala College, Muvattupuzha, Ernakulam"),
    ("North Malabar Institute of Technology ",	"North Malabar Institute of Technology "),
    ("NSS College of engineering",	"NSS College of engineering"),
    ("Presentation College of Applied Sciences, Puthenvelikara, Ernakulam",	"Presentation College of Applied Sciences, Puthenvelikara, Ernakulam"),
    ("Prime college of engineering",	"Prime college of engineering"),
    ("Providence college of engineering,chengannur",	"Providence college of engineering,chengannur"),
    ("R.L.V College of Music and Institute of Fine Arts , Ernakulam",	"R.L.V College of Music and Institute of Fine Arts , Ernakulam"),
    ("Rajadhani Institute of engineering and technology",	"Rajadhani Institute of engineering and technology"),
    ("Rajagiri College of Social Science, Ernakulam",	"Rajagiri College of Social Science, Ernakulam"),
    ("Rajagiri School of Engineering and Technology, Ernakulam",	"Rajagiri School of Engineering and Technology, Ernakulam"),
    ("Rajiv Gandhi Institute of Technology, Kerala",	"Rajiv Gandhi Institute of Technology, Kerala"),
    ("Royal College of Engineering & Technology",	"Royal College of Engineering & Technology"),
    ("S.C.M.S. School of Engineering and Technology, Cochin, karukutty",	"S.C.M.S. School of Engineering and Technology, Cochin, karukutty"),
    ("S.S.V. College, Cochin",	"S.S.V. College, Cochin"),
    ("Sacred Heart College, Ernakulam",	"Sacred Heart College, Ernakulam"),
    ("Sahrdaya College of Engineering and Technology",	"Sahrdaya College of Engineering and Technology"),
    ("saint dominic's college",	"saint dominic's college"),
    ("Saintgits College of Engineering, Pathamuttam, Kerala",	"Saintgits College of Engineering, Pathamuttam, Kerala"),
    ("Sankar Institute of Science and Technology",	"Sankar Institute of Science and Technology"),
    ("Sarabhai Institute of science and technology",	"Sarabhai Institute of science and technology"),
    ("SHM Engineering College",	"SHM Engineering College"),
    ("SJCET, Choondacherry, Kerala",	"SJCET, Choondacherry, Kerala"),
    ("Southern College of Engineering & Technology",	"Southern College of Engineering & Technology"),
    ("Sree Buddha College Of Engineering for Women, Muttathukonam",	"Sree Buddha College Of Engineering for Women, Muttathukonam"),
    ("Sree Buddha College of Engineering, Alappuzha",	"Sree Buddha College of Engineering, Alappuzha"),
    ("Sree Eranakulathappan College of Engineering and Management",	"Sree Eranakulathappan College of Engineering and Management"),
    ("Sree Narayana Guru College of Engineering & Technology, Chalakode",	"Sree Narayana Guru College of Engineering & Technology, Chalakode"),
    ("Sree Narayana Gurukulam College of Engineeing, Kolenchery",	"Sree Narayana Gurukulam College of Engineeing, Kolenchery"),
    ("Sree Narayana Mangalam Institute of Management and Technology, Moothakunnam, maliyankara",	"Sree Narayana Mangalam Institute of Management and Technology, Moothakunnam, maliyankara"),
    ("Sree Sankaracharya University of Sanskrit, Kalady",	"Sree Sankaracharya University of Sanskrit, Kalady"),
    ("Sree Vellappally Natesan College of Engineering,	Alappuzha",	"Sree Vellappally Natesan College of Engineering,  Alappuzha"),
    ("Sreepathy institute of science and technology",	"Sreepathy institute of science and technology"),
    ("Sri chithra thrirunal college of engineering",	"Sri chithra thrirunal college of engineering"),
    ("St thomas college of engineering, chengannur",	"St thomas college of engineering, chengannur"),
    ("St Thomas institute of science and technology",	"St Thomas institute of science and technology"),
    ("St. Alberts College, Cochin",	"St. Alberts College, Cochin"),
    ("St. Berchmans College, Changanassery, Kerala",	"St. Berchmans College, Changanassery, Kerala"),
    ("St. Pauls College, Ernakulam",	"St. Pauls College, Ernakulam"),
    ("St. Peters College, Kolenchery, Ernakulam",	"St. Peters College, Kolenchery, Ernakulam"),
    ("St. Teresa's College, Cochin",	"St. Teresa's College, Cochin"),
    ("St. Thomas College of Engineering & Technology, Sivapuram",	"St. Thomas College of Engineering & Technology, Sivapuram"),
    ("St. Xaviers College for Women, Aluva",	"St. Xaviers College for Women, Aluva"),
    ("St.George's College, Saint George College Road, Aruvithura, Erattupetta, Kerala",	"St.George's College, Saint George College Road, Aruvithura, Erattupetta, Kerala"),
    ("St.Thomas College Pala, Arunapuram, Pala, Kerala",	"St.Thomas College Pala, Arunapuram, Pala, Kerala"),
    ("T.K.M. College of Engineering, Kollam",	"T.K.M. College of Engineering, Kollam"),
    ("T.O.C.H. Institute of Science and Technology",	"T.O.C.H. Institute of Science and Technology"),
    ("Thejus Engineering College",	"Thejus Engineering College"),
    ("Travancore Engineering College, Kollam",	"Travancore Engineering College, Kollam"),
    ("U.K.F. College of Engineering & Technology, Kollam",	"U.K.F. College of Engineering & Technology, Kollam"),
    ("Universal Engineering College",	"Universal Engineering College"),
    ("University college of engineering",	"University college of engineering"),
    ("University College of Engineering, muttom",	"University College of Engineering, muttom"),
    ("Veda Vyasa Institute of Technology , Karadparamba",	"Veda Vyasa Institute of Technology , Karadparamba"),
    ("Vidya Academy of Science and Technology",	"Vidya Academy of Science and Technology"),
    ("Vimal Jyothi Engineering College, Chemperi",	"Vimal Jyothi Engineering College, Chemperi"),
    ("Viswa Jyothi College of Engineering and Technology, Muvattupuzha",	"Viswa Jyothi College of Engineering and Technology, Muvattupuzha"),
    ("VJCET, Vazhakullam",	"VJCET, Vazhakullam"),
    ("VKCET Chavarcode",	"VKCET Chavarcode"),
    ("Younus College of Engineering for Women, Kollam",	"Younus College of Engineering for Women, Kollam"),
    ("Others","Others")
    )

    # EVENT = (
    #     ('','Event'),
    #     ("ROBW","Robowar"),
    #     ("GOD","Game Of Drones"),
    #     ("ROBS","Robosoccer"),
    #     ("GPLAN","Game Plan"),
    #     ("GZON","Game Zone"),
    # )

    EVENT = ((x.event_id,x.event_name) for x in event.objects.filter(paid=True))

    name=forms.CharField(max_length=50,required=True,label='',widget=forms.TextInput(attrs={
        "placeholder":"Full Name",
        "class":"form-control",
        "style":"height:50px;margin-bottom:10px;"
    }))
    college=forms.ChoiceField(choices=COLLEGES,label='',widget=forms.Select(attrs={
        "placeholder":"College Name",
        "class":"input form-control",
        "style":"height:50px;margin-bottom:10px;",
        "id":"college"
    }))
    email=forms.EmailField(required=False,label='',validators=[redundantmailforpaid,],widget=forms.TextInput(attrs={
        "placeholder":"Email Address",
        "class":"form-control",
        "style":"height:50px;margin-bottom:10px;"
    }))
    phone=forms.CharField(max_length=10,min_length=10,label='',validators=[number,redundantnumforpaid],widget=forms.TextInput(attrs={
        "placeholder":"Phone Number",
        "class":"form-control",
        "style":"height:50px;margin-bottom:10px;"
    }))


    event=forms.ChoiceField(choices = EVENT,label='',widget=forms.Select(attrs={
        "placeholder":"Event Name",
        "class":"form-control",
        "style":"height:50px;margin-bottom:20px;"
    }))
    def clean(self):
        super(PaidRegistrationForm,self).clean()

class StudentForm(forms.Form):

    name = forms.CharField(max_length=50, required=True, label='', widget=forms.TextInput(attrs={
        "placeholder": "Full Name",
        "class": "form-control",
        "style": "height:50px;margin-bottom:10px;"
    }))
    college = forms.CharField(max_length=100, required=True, label='', widget=forms.TextInput(attrs={
        "placeholder": "School",
        "class": "form-control",
        "style": "height:50px;margin-bottom:20px;"
    }))

    def clean(self):
        cleaned_data = super(StudentForm, self).clean()

class OfflineRegistrationForm(forms.Form):

    TRUE_FALSE_CHOICES = (
        ('', "Stay"),
        (1, "Yes"),
        (0, "No"),)

    name=forms.CharField(max_length=50,required=True,label='',widget=forms.TextInput(attrs={
        "placeholder":"Full Name",
        "class":"form-control",
        "style":"height:50px;margin-bottom:10px;"
    }))
    email=forms.EmailField(required=False,label='',validators=[redundantmail,],widget=forms.TextInput(attrs={
        "placeholder":"Email Address",
        "class":"form-control",
        "style":"height:50px;margin-bottom:10px;"
    }))
    phone=forms.CharField(max_length=10,min_length=10,label='',validators=[number,redundantnum],widget=forms.TextInput(attrs={
        "placeholder":"Phone Number",
        "class":"form-control",
        "style":"height:50px;margin-bottom:10px;"
    }))
    # stay=forms.TypedChoiceField(coerce=lambda x: bool(int(x)),choices = TRUE_FALSE_CHOICES,label='',widget=forms.Select(attrs={
    #     "placeholder":"Stay Required",
    #     "class":"form-control",
    #     "style":"height:50px;margin-bottom:20px;"
    # }))
    def clean(self):
        super(OfflineRegistrationForm,self).clean()
