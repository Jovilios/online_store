from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MessageRespondForm
from online_store.user_messages.models import Message



@login_required
def inbox(request):
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        message = get_object_or_404(Message, pk=message_id)
        if request.user == message.recipient:
            message.delete()
            return redirect('inbox')
        else:
            error_message = 'You do not have permission to delete this message.'
            received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
            return render(request, 'messages/inbox.html', {'received_messages': received_messages, 'error_message': error_message})

    received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'messages/inbox.html', {'received_messages': received_messages})


@login_required
def respond_to_message(request, message_id):

    message = get_object_or_404(Message, pk=message_id)

    if request.user != message.recipient:
        return render(request, "web/error_page.html",
                      {"error_message": "You do not have permission to do that."})

    if request.method == 'POST':
        form = MessageRespondForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.sender = request.user
            response.recipient = message.sender
            response.subject = f"Re: {message.subject}"
            response.save()
            return redirect('inbox')
    else:
        form = MessageRespondForm()

    context = {
        'form': form,
        'original_message': message
    }

    return render(request, 'messages/respond_to_message.html', context)

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    if request.user != message.recipient:
        return render(request, "web/error_page.html", {"error_message": "You do not have permission to do that."})
    if request.method == 'POST':
        message.delete()
    return redirect('inbox')