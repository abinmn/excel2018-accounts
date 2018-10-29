from django.shortcuts import render
from django.views.generic import TemplateView
from controlroom.models import event
from register.models import userinfo, paid_userinfo
from django.http import JsonResponse
import datetime
from django.shortcuts import get_object_or_404
from register.models import winners, userinfo, paid_winners
from .forms import eventform
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.generics import RetrieveAPIView
from .serializers import api, winnerapi
from rest_framework.generics import ListAPIView
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle as PS
from controlroom.export_data import generatepaidcsv, generateusercsv

def generatepdf(win,event):
    s="static/pdf/"+event
    filename=s+"-shortlisted.pdf"
    data=[['EXCELID','NAME','PHONE']]
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    centered = PS(name = 'centered',
                  fontSize = 25,
                  leading = 16,
                  alignment = 1,
                  spaceAfter = 30,
                  )
    for obj in win:
        data.append([obj.excelid,obj.name,obj.phone])

    t = Table(data)#,2*[2*inch], len(data)*[0.3*inch])
    t.setStyle(TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ('TEXTCOLOR',(0,0),(-1,0),colors.green),
    ]))
    k="<b>"
    k=k+event+"-SHORTLIST"
    k=k+"</b>"
    elements.append(Paragraph(k,centered))
    elements.append(t)
    doc.build(elements)

def generatepdfwinners(win,event):
    s="static/pdf/winners"+event
    filename=s+"-winners.pdf"

    data=[['POSITION','EXCELID','NAME','COLLEGE',]]
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    centered = PS(name = 'centered',
                  fontSize = 25,
                  leading = 16,
                  alignment = 1,
                  spaceAfter = 30,
                  )
    for obj in win:
        data.append([obj.position, obj.excelid,obj.name,obj.college])
    t=Table(data)#,2*[2*inch], len(data)*[0.3*inch])
    t.setStyle(TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ('TEXTCOLOR',(0,0),(-1,0),colors.green),
    ]))
    k="<b>"
    k=k+event+"-WINNERS"
    k=k+"</b>"
    elements.append(Paragraph(k,centered))
    elements.append(t)
    doc.build(elements)


def PostCreate(request, pk=None):
    instance = get_object_or_404(event, pk=pk)
    form = eventform(request.POST or None, instance=instance)

    if form.is_valid():
        link="/eventpage/"
        link=link+form.cleaned_data.get('event_id')+"/"
        if form.cleaned_data.get('winner1')!="nil" or form.cleaned_data.get('winner2')!="nil" and form.cleaned_data.get('winner3')!="nil" or form.cleaned_data.get('short_list')!="nil":
            event_name=form.cleaned_data.get('event_name')
            eventid=form.cleaned_data.get('event_id')
            winners.objects.filter(event=event_name).delete()

            eventlist=event.objects.filter(event_id=eventid)
            winner1=form.cleaned_data.get('winner1')
            winner2=form.cleaned_data.get('winner2')
            winner3=form.cleaned_data.get('winner3')
            participants=form.cleaned_data.get('participants')
            participants.split(',')
            winner_list=[winner1.split(','),winner2.split(','),winner3.split(',') ]
            if len(winner_list)!=0:
                for lists in winner_list:
                    for Exid in lists:
                        if eventlist[0].paid == False :
                            queryset=userinfo.objects.filter(excelid=Exid)
                            for obj in queryset:
                                name=obj.name
                                college= obj.college
                                if not winners.objects.filter(event=event_name,excelid=Exid):
                                    obj1_winner=winners(event=event_name,name=name,college=college,position=winner_list.index(lists)+1,excelid=Exid)
                                    obj1_winner.save()
                        else :
                            queryset=paid_userinfo.objects.filter(excelid=Exid)
                            for obj in queryset:
                                        name=obj.name
                                        college= obj.college
                                        if not paid_winners.objects.filter(event=event_name,excelid=Exid):
                                            obj1_winner=paid_winners(event=event_name,name=name,college=college,position=winner_list.index(lists)+1,excelid=Exid)
                                            obj1_winner.save()

        if form.cleaned_data.get('participants')!="nil" and form.cleaned_data.get('participants')!="":
            event_name=form.cleaned_data.get('event_name')
            event_id=form.cleaned_data.get('event_id')
            eventlist=event.objects.filter(event_id=event_id)
            participants=form.cleaned_data.get('participants').split(",")
            if len(participants)!=0:
                stri=event_id
                for Exid in participants:
                    if Exid !="nil" and Exid !="":
                        if eventlist[0].paid == False :
                            queryset=userinfo.objects.get(excelid=Exid)
                            if queryset.participated_events=="nil":
                                queryset.participated_events=""
                            pp=queryset.participated_events.split(",")
                            if stri not in pp:
                                queryset.participated_events = queryset.participated_events+stri + ","
                                queryset.save()
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(link)

    context = {
        "form": form,
    }
    return render(request, "test.html", context)

class ControlRoomView(TemplateView):
    def get(self,request,*args,**kwargs):
        today = datetime.datetime.today()
        result=event.objects.filter(status__in=[0,1])
        sb=1
        context={
            "title":"testing",
            "searchby":"events of the day",
            "searchby_num":sb,
            "obj":result,
            "len":len(result)
        }
        return render(request,"controlroom.html",context)

    def post(self,request,*args,**kwargs):
        error1=False
        error2=False
        result=[]
        sb=-1
        searchby=request.POST.get('searchby')
        value=request.POST.get('value')


        if request.POST.get('ajax'):
            ajax=request.POST.get('ajax')
            if(ajax=="eventname"):
                list1=event.objects.values_list('event_name',flat=True)
            elif(ajax=="excelid"):
                list1=[]
            d=[]
            for li in list1:
                li.replace("u","")
                d.append(li)
            data = {
                'dataset': d
            }
            return JsonResponse(data)

        if request.POST.get('update'):
            list=request.POST.get('update')
            list1=list.split(',')
            obj = event.objects.get(event_id=list1[0])

            obj.save()

            d=[]
            data={
                'dataset':d
            }
            return JsonResponse(data)

        if((searchby=="" or searchby==None) and (value=="Not Applicable" or value=="")):
            error1=True
        elif(searchby=="eventname"):
            value="_".join(value.split(" "))
            result=event.objects.filter(event_name__icontains=value)
            sb=3
        elif(searchby=="excelid"):
            result=userinfo.objects.filter(excelid=value)
            if(len(result)==0):
                result=paid_userinfo.objects.filter(excelid=value)
            sb=2

        context={
            "title":"testing",
            "searchby":searchby,
            "value":value,
            "error1":error1,
            "error2":error2,
            "searchby_num":sb,
            "obj":result,
            "len":len(result)
        }
        return render(request,"controlroom.html",context)


class EventView(TemplateView):
    def get(self,request,*args,**kwargs):
        list1=get_object_or_404(event,event_id=kwargs['event'])
        list2=list1.short_list.split(",")
        list5=list1.participants.split(",")
        context={
            "title":"testing",
            "obj":list1,
            "id":list1.event_id,
            "evname":list1.event_name,
            "shortlist":list2,
            "participants":list5
        }
        return render(request,"eventview.html",context)

class Android(ListAPIView):
    serializer_class = api

    def get_queryset(self):
        event_id=self.kwargs['pk']
        short=get_object_or_404(event,event_id=event_id)
        shortlisted=short.short_list
        shortlistedcan=shortlisted.split(',')
        if not short.paid:
            return userinfo.objects.filter(excelid__in=shortlistedcan)
        else:
            return paid_userinfo.objects.filter(excelid__in=shortlistedcan)


class Winnerapi(ListAPIView):
    serializer_class = winnerapi

    def get_queryset(self):
        event_name=self.kwargs['pk']
        winnerobj =get_object_or_404(event,event_name__iexact=event_name)
        if not winnerobj.paid:
            winn = winners.objects.filter(event__iexact=event_name)
        else:
            winn = paid_winners.objects.filter(event__iexact=event_name)
        return winn

class Download(TemplateView):
    def get(self,request,*args,**kwargs):
        event1=self.kwargs['eve']
        print(event1)
        obj = event.objects.get(event_id=event1)
        event1=obj.event_name
        print(type(obj))
        if obj.short_list!="nil":
            shortlisted = obj.short_list.split(',')
            print(shortlisted)
            if not obj.paid:
                short = []
                for eid in shortlisted:
                    if eid != "nil" and eid != "":
                        short.append(userinfo.objects.get(excelid=eid))
            else:
                short=[]
                for eid in shortlisted:
                    if eid != "nil" and eid !="":
                        short.append(paid_userinfo.objects.get(excelid=eid))
            generatepdf(short,event1)
        else:
            short=[]
            generatepdf(short,event1)
        filename = "static/pdf/"+event1
        filename = filename+"-shortlisted.pdf"
        fname = event1+"-shortlisted.pdf"
        with open(filename, 'rb') as pdf:
            response = HttpResponse(pdf.read())
            response['content_type'] = 'application/pdf'
            response['Content-Disposition'] = 'attachment;filename=%s'%fname
            return response

class EventNav(TemplateView):
    def get(self,request,*args,**kwargs):
        obj = event.objects.all().order_by('status')
        context={
            "events":obj,
        }
        return render(request,"eventnavigation.html",context)


class WinnerDownload(TemplateView):
    def get(self,request,*args,**kwargs):
        event1=self.kwargs['eve']
        obj = event.objects.get(event_id=event1)
        event1=obj.event_name
        if not obj.paid:
            win = winners.objects.filter(event = obj.event_name).order_by('position')
        else:
            win = paid_winners.objects.filter(event = obj.event_name).order_by('position')
        generatepdfwinners(win,event1)
        filename = "static/pdf/winners"+event1
        filename = filename+"-winners.pdf"
        fname = event1+"-winners.pdf"
        with open(filename, 'rb') as pdf:
            response = HttpResponse(pdf.read())
            response['content_type'] = 'application/pdf'
            response['Content-Disposition'] = 'attachment;filename=%s' % fname
            return response


def paiduserdata(request):
    file = open("static/csv/paidEventsData.csv", "w+")
    generatepaidcsv(file)
    readfile=open("static/csv/paidEventsData.csv", "r")
    response = HttpResponse(readfile.read())
    response['content_type'] = 'application/csv'
    response['Content-Disposition'] = 'attachment;filename=paidEventsData.csv'
    return response

def userdata(request):
    file = open("static/csv/spotRegData.csv", "w+")
    generateusercsv(file)
    readfile=open("static/csv/spotRegData.csv", "r")
    response = HttpResponse(readfile.read())
    response['content_type'] = 'application/csv'
    response['Content-Disposition'] = 'attachment;filename=paidEventsData.csv'
    return response
