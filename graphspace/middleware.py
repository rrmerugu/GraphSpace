from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
import json
from graphspace.exceptions import *
from graphspace.database import *
from channels.handler import AsgiRequest


class SQLAlchemySessionMiddleware(object):
	def process_request(self, request):
		if type(request) == AsgiRequest:
			request.db_session = Database().session()
		else:
			request.db_session = settings.db.session()

	def process_response(self, request, response):
		try:
			session = request.db_session
		except AttributeError:
			return response

		try:
			session.commit()
			session.close()
			return response
		except:
			session.rollback()
			session.close()
			raise

	def process_exception(self, request, exception):
		try:
			session = request.db_session
		except AttributeError:
			return
		session.rollback()
		session.close()


class GraphSpaceMiddleware(object):
	def process_request(self, request):
		request.session['uid'] = request.session['uid'] if 'uid' in request.session else None

	def process_response(self, request, response):
		return response

	def process_exception(self, request, exception):
		# TODO: Handle different types of error
		if request.META.get('HTTP_ACCEPT', None) == 'application/json':
			if issubclass(type(exception), GraphSpaceError):
				return HttpResponse(str(exception), content_type="application/json", status=exception.status)

			if exception.message == 'Unauthenticated':
				response = HttpResponse(content_type="application/json", status=401)
				response['WWW-Authenticate'] = 'Basic'
				return response
			elif exception.message == 'Unauthorized':
				response = HttpResponse(content_type="application/json", status=403)
				response['WWW-Authenticate'] = 'Basic'
				return response
			else:
				return HttpResponse(str(BadRequest(request, msg=str(exception))), content_type="application/json", status=400)

		context = exception.to_dict() if issubclass(type(exception), GraphSpaceError) else {}

		if exception.message == 'Unauthenticated':
			context['message'] = 'You are not authenticated to view this page.'
		elif exception.message == 'Unauthorized':
			context['message'] = 'You are not authorized to view this page.'

		return render(request, '500.html', context)
