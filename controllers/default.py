# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    import random
    if not session.k or request.vars.reset:
        session.i = random.randint(1,5)
        session.k=3
        session.j=random.randint(1,session.k)
        redirect(URL())

    if request.vars.number:
        if int(request.vars.number)==session.j:
            session.k+=1
            oldi=session.i
            while session.i==oldi:
                session.i = random.randint(1,5)
                oldj=session.j
            while session.j==oldj:
                session.j = random.randint(int(session.k/2),session.k)
                message='Excellent, Try another one'
                audio=URL('static','trains/excellent.wav')
        else:
            message='Respuesta Incorrecta, no son %s trenes, pruebe otra vez' % request.vars.number
            audio=URL('static','trains/haha.wav')
    else:
        message=""
        audio=None
    form=DIV(*[TAG[''](' ',A(k,_style="padding:15px; font-size: 2em;",
                             _href=URL(vars=dict(number=k)))) for k in range(1,session.k+1)])
    return dict(message=message, form=form, audio=audio)


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
