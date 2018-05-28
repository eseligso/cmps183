# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

import re

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    checklists = db((db.checklist.is_public==True) | (db.checklist.is_public==False)).select()
    return dict(checklists=checklists)

def empty(form):
    r = r"\S"
    t = re.search(r, form.vars.title)
    d = re.search(r, form.vars.description)
    if t is None:
        form.errors.title = T("Your checklist needs a title!")
    if d is None:
        form.errors.description = T("Your checklist needs a description!")

def add():
    """Adds a checklist"""
    
    form = SQLFORM(db.checklist)
    if form.process(onvalidation=empty).accepted:
        session.flash = T("Checklist added.")
        redirect(URL('default', 'index'))
    elif form.errors:
        session.flash = T("Please correct the information.")
    return dict(form=form)

@auth.requires_login()
def edit():
    """Offers a form to edit a checklist"""

    if request.args(0) is None:
        return redirect(URL('default', 'index'))
    else:
        q = ((db.checklist.user_email == auth.user.email) &
             (db.checklist.id == request.args(0)))
        cl = db(q).select().first()
        if cl is None:
            session.flash = T("You are not authorized to view that checklist.")
            redirect(URL('default', 'index'))
        form = SQLFORM(db.checklist, record=cl, deletable=False)
        if form.process(onvalidation=empty).accepted:
            session.flash = T("Checklist saved.")
            redirect(URL('default', 'index'))
        elif form.errors:
            session.flash = T("Please correct the information")
    return dict(form=form)

@auth.requires_login()
@auth.requires_signature()
def delete():
    """Deletes a checklist"""

    if request.args(0) is not None:
        q = ((db.checklist.user_email == auth.user.email) &
             (db.checklist.id == request.args(0)))
        db(q).delete()
    redirect(URL('default', 'index'))

@auth.requires_login()
def toggle_private():
	"""Toggles checklist between private and public"""

	if request.args(0) is not None:
		q = ((db.checklist.user_email == auth.user.email) &
			 (db.checklist.id == request.args(0)))
		cl = db(q).select().first()
		if cl is None:
			session.flash = T("You are not authorized to change the permissions of that checklist.")
			redirect(URL('default', 'index'))
		else:
			if cl.is_public == True:
				cl.is_public = False
			else:
				cl.is_public = True
			cl.update_record()
	redirect(URL('default', 'index'))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
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
