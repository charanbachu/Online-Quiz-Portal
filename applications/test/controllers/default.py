# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to THE QUIZ!")
    return dict()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

@auth.requires_membership('manage users')
def manage_users():
    grid = SQLFORM.grid(db.auth_user)
    return locals()

import re

@auth.requires_login()
def mainpage():
    secret = db(db.secret.name == auth.user.first_name).select()
    auth_count = db(db.auth_user.id >= 0).count()
    sorted_list = sorted(db(db.secret.id >= 0).select(), key=lambda k: k['score']) 
    if(secret[0].Test == 1):
	if request.vars:
	    p=request.vars['search_name']
	    x=DIV()
	    #if( p == ""):
		#i = 4
	    for i in range(auth_count):
		#i= i -1
	 	j=auth_count-i-1
		if(p == ""):
		    if(i == 5):
			break
		    #j = i 
		    #i = auth_count-i-1
   	        if(re.match(p,sorted_list[auth_count - i-1].name)):
		    x=DIV(x,DIV(CENTER(i+1),_id="rec1",_style="float:left;width:20%;"),
		    DIV(CENTER(sorted_list[auth_count - i-1].name),_id="rec2",_style="float: left; width: 110px; padding-left: 5px; padding-right: 5px; margin-left: 0px;"),
		    DIV(CENTER(sorted_list[auth_count - i-1].score),_id="rec3",_style="float: left; width: 50px; padding-left: 0px;"),BR())
	        #i = i -2
	    if(p == ""):
		x=DIV(DIV(CENTER("TOP FIVE :"),BR(),x))
	    
	    return x	
	if(secret[0].quesstatus - 1 == db(db.Questions.id > 0).count()):
	    db(db.secret.name == auth.user.first_name).update(Test = 0)
            redirect(URL('congrats'))
	quesnum = secret[0].quesstatus
	score = secret[0].score
    	question = db(db.Questions.quesno == quesnum).select()                 
	ans=question[0].answer
        if request.args:                						
	    if(request.args[0]== "None"):
                secret[0].update_record(quesstatus= quesnum + 1)
		secret[0].update_record(unanswered= secret[0].unanswered + 1)
		redirect(URL('default','mainpage'))
       	    elif(request.args[0]== ans):
                score=score+10
		secret[0].update_record(correct= secret[0].correct + 1)
                secret[0].update_record(score=score)
	        secret[0].update_record(quesstatus= quesnum + 1)
                redirect(URL('mainpage'))

	    elif(request.args[0] != ans and request.args[0] != "hint"):
                score=score-10
		secret[0].update_record(wrong= secret[0].wrong + 1)
                secret[0].update_record(score=score)
	        secret[0].update_record(quesstatus= quesnum + 1)
                redirect(URL('mainpage'))             
        return dict(name=auth.user.first_name,secret=secret[0],question=question[0],count = auth_count,sorted_list = sorted_list,time =0)
    else:
	redirect(URL('congrats'))


@auth.requires_login()
def congrats():
    secret = db(db.secret.name == auth.user.first_name).select()
    return dict(name = auth.user.first_name, secret = secret[0])

@auth.requires_login()
def instructions():
    return dict()

