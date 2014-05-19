# Create your views here.
from groups.forms import GroupForm
from groups.models import Group
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from common import getHost
def addGroup(request):
    if request.method == 'POST' :
        form = GroupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            g = Group(name=cd['name'], description=cd['description'], group_type=cd['group_type'])
            g.save()
            return HttpResponseRedirect(getHost(request) + "/groups/")
    else:
        form = GroupForm()
    return  render_to_response('groups/group_form.html', {'form':form})

def listGroup(request):
    l = Group.objects.all()
    return render_to_response('groups/groups.html', {'forms':l});

def deleteGroups(request):
    ids = request.GET["ids"].split(",")
    for idItem in ids:
        if idItem:
            Group.objects.all().filter(id=idItem).delete()
    return HttpResponseRedirect(getHost(request) + "/groups/")
