import re
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
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))

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
@auth.requires_login()
def instructions():
	go=A('Continue', _href=URL('default', 'start_quiz'))
	auth_count = db(db.auth_user.id >= 0).count()                           # count of total reg users
	user_rec = db(db.auth_user.id  == auth_count).select().first()          # list of all reg users
	user_count = db(db.user_profile.id >= 0).count()                        # (2nd DB i.e user profile) count of user
	if(auth_count > user_count):                                            # this is true if auth users greater than users 
		db.user_profile.insert(name=user_rec.first_name)
	values = db(db.user_profile.id >= 0).select()                           # score of user logged in
	
	session.count=auth_count						# users count
	session.name=auth.user.first_name					# logged in user's first_name

	return dict(go=go)

session.argume=""
@auth.requires_login()
def start_quiz():
	rec = db(db.user_profile.id >= 0).select()
	if not request.args and not request.vars:
		for i in rec:						# grabbing user information
			if (i.name == auth.user.first_name):					# ""
				done=i.done						# ""
				score=i.score						# ""
				fifty=i.fiftyfifty					# ""
				poll=i.poll						# ""

		question_op = db(db.questions.id >= done).select().first()		# question and options
		q=question_op.question							# ""
		oa=question_op.optiona							# ""
		ob=question_op.optionb							# ""
		oc=question_op.optionc							# ""
		od=question_op.optiond							# ""
		ans=question_op.answer							# ""

  		session.ans=ans								# session.ans
		log=A('Logout', _href=URL('default', 'user', args='logout'))		# for logout link

 		m=0
		dic=[]									# for sorted list based on score
		for m in range(session.count):						# ""
			dic.append(rec[m])					# ""
		sorted_list = sorted(dic, key=lambda k: k['score'])			# ""
		
		session.sorted_list=sorted_list						# Session.sorted_list

		return dict(name=auth.user.first_name,logout=log,score=score,q=q,oa=oa,ob=ob,oc=oc,od=od,done=done,rec=rec,poll=poll,fifty=fifty,count=session.count,what=session.argume)

		############# End of if not request.args and not vars ########
	if request.args:
	   	if((request.args[0] == "optiona") or (request.args[0] == "optionb") or (request.args[0] == "optionc") or (request.args[0] == "optiond")):									       # arguments passed wrer related to options

			rows = db(db.user_profile.id  > 0).select()			# Updation of record
			for row in rows:						# ""
		      		if (row.name == session.name):				# ""
			      		x=row.score					# ""
			      		break						# ""
                	if(request.args[0] == session.ans):				# ""
		      		x=x+10							# ""
			elif(request.args[0] != session.ans):				# ""
		      		x=x-5							# ""
			y=row.done+1							# ""
			row.update_record(done=y)					# ""
		      	row.update_record(score=x)					# ""

			redirect(URL('start_quiz'))					# Redirection to next question

		elif(request.args[0] == "5050" or request.args[0] == "poll"):		#arg passed were related to help
			redirect(URL('start_quiz'))
		################ End of if request.args ####################
	if request.vars:								# request.vars
		auth_count = db(db.auth_user.id >= 0).count()
		m=0
		dic=[]
		x=DIV()
		for m in range(auth_count):                      
			dic.append(rec[m])                          
		sorted_list = sorted(dic, key=lambda k: k['score']) 
		session.w=request.vars['search_name']
		p=session.w
		for i in range(auth_count):
			p=session.w
			j=auth_count-i-1
			if(re.match(p,sorted_list[i].name)):
				x=DIV(DIV(j+1,_id="rec1",_style="float:left;width:10%;"),
				DIV(sorted_list[i].name,_id="rec2",_style="float:left;width:25%;padding-left:40px;"),
				DIV(sorted_list[i].score,_id="rec3",_style="float:left;width:25%;padding-left:55px;"),BR(),x)
			
	return x
