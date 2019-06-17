from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from app.models import *
from app.spellcheck import *
from django.http import HttpResponse

def home(request):
	return render(request, 'index.html',{})
def register(request):
	request.session.flush()
	return render(request, 'Login.html',{})
def login(request):
	return render(request, 'Reg.html',{})
def checkscorepage(request):
	obj=EssayData.objects.all()
	email=request.session['email']
	d=0
	context={}
	b1=''
	b2=''
	b3=''
	b4=''
	b5=''
	b6=''
	ob=HtmlData.objects.all()
	for elt in ob:
		if elt.filename=='t1':
			b1=elt.code
			break
	for elt in ob:
		if elt.filename=='t2':
			b2=elt.code
			break
	for elt in ob:
		if elt.filename=='t3':
			b3=elt.code
			break
	for elt in ob:
		if elt.filename=='t4':
			b4=elt.code
			break
	for elt in ob:
		if elt.filename=='t5':
			b5=elt.code
			break
	for elt in ob:
		if elt.filename=='t6':
			b6=elt.code
			break		
	table=''
	for elt in obj:
		if elt.userid==email:
			d=1
			data=b1+elt.topic+b2+elt.wordcount+b3+elt.spellcheck+b4+elt.grammercheck+b5+elt.error+b6
			table=table+data
	if d==1:
		return render(request, "CheckScore.html" , {'data':table})
	else:
		return render(request, "CheckScore.html" , {})
@csrf_exempt
def checkscore(request):
	if request.method=="POST":
		topic = request.POST.get('Topic')
		data = request.POST.get('text')
		obj=EssayData.objects.all()
		count = str(data).split()
		length = len(count)
		spell = spellcheck(str(data))
		obj=EssayData(userid=request.session['email'],topic=topic,essay=data,wordcount=length,spellcheck=spell['errorcount'],grammercheck='-',error='-')
		obj.save()
		b1=''
		b2=''
		b3=''
		b4=''
		b5=''
		b6=''
		ob=HtmlData.objects.all()
		for elt in ob:
			if elt.filename=='t1':
				b1=elt.code
				break
		for elt in ob:
			if elt.filename=='t2':
				b2=elt.code
				break
		for elt in ob:
			if elt.filename=='t3':
				b3=elt.code
				break
		for elt in ob:
			if elt.filename=='t4':
				b4=elt.code
				break
		for elt in ob:
			if elt.filename=='t5':
				b5=elt.code
				break
		for elt in ob:
			if elt.filename=='t6':
				b6=elt.code
				break		
		table=''
		obj=EssayData.objects.all()
		for elt in obj:
			if elt.userid==request.session['email']:
				d=1
				data=b1+elt.topic+b2+elt.wordcount+b3+elt.spellcheck+b4+elt.grammercheck+b5+elt.error+b6
				table=table+data
		return render(request, "CheckScore.html" , {'data':table})
def analyticspage(request):
	return render(request, 'Analytics.html',{})
def rulespage(request):
	return render(request, 'Rules.html',{})
def contactpage(request):
	return render(request, 'Contact.html',{})
@csrf_exempt
def saveuser(request):
	if request.method=="POST":
		text=' '
		n=request.POST.get('name')
		g=request.POST.get('gender')
		ph=request.POST.get('phone')
		p=request.POST.get('password')
		e=request.POST.get('email')
		ob=UserData.objects.all()
		d=0
		for elt in ob:
			if e==elt.email:
				text='User already Signed In'
				d=1
				break
		if d==0:
			obj=UserData(name=n,password=p,email=e,gender=g,phone=ph)
			obj.save()
			text='Account Created Successfully'
		context={'text':text}
		return render(request,'regresult.html',context)
@csrf_exempt
def checklogin(request):
	text=" "
	d=0
	e=request.POST.get('email')
	p=request.POST.get('password')
	obj=UserData.objects.all()
	name=''
	for elt in obj:
		if e==elt.email and p==elt.password:
			d=1
			name=elt.name
			request.session['email'] = e
			request.session['name'] = elt.name
			break
	if d==0:
		con={'text':"No User Found"}
		return render(request,"regresult.html",con)
	else:
		return render(request,'index.html',{'name':name})