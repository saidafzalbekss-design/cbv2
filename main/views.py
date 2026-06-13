import requests
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django import forms
from .models import Talaba

TELEGRAM_TOKEN = '8845788723:AAFfGFGe7qh8_rSNbI5un6ERJ85oSdn11Bk'
TELEGRAM_CHAT_ID = '6539174454'

def telegram_yuborish(matn):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': matn,
        'parse_mode': 'HTML'
    }
    try:
        requests.post(url, data=data)
    except Exception:
        pass


class TalabaList(ListView):
    model = Talaba
    template_name = 'main/talaba_list.html'
    context_object_name = 'talabalar'


class TalabaCreate(LoginRequiredMixin, CreateView):
    model = Talaba
    fields = ['ism', 'familiya', 'guruh', 'yosh', 'faol']
    template_name = 'main/talaba_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        t = self.object
        messages.success(self.request, f"✅ Talaba qo'shildi: {t}")
        telegram_yuborish(
            f"➕ <b>Yangi talaba qo'shildi!</b>\n\n"
            f"👤 Ism: {t.ism} {t.familiya}\n"
            f"🎓 Guruh: {t.guruh}\n"
            f"🎂 Yosh: {t.yosh}\n"
            f"✅ Faol: {'Ha' if t.faol else 'Yoq'}"
        )
        return response


class TalabaUpdate(LoginRequiredMixin, UpdateView):
    model = Talaba
    fields = ['ism', 'familiya', 'guruh', 'yosh', 'faol']
    template_name = 'main/talaba_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        t = self.object
        messages.success(self.request, f"✏️ Talaba tahrirlandi: {t}")
        telegram_yuborish(
            f"✏️ <b>Talaba tahrirlandi!</b>\n\n"
            f"👤 Ism: {t.ism} {t.familiya}\n"
            f"🎓 Guruh: {t.guruh}\n"
            f"🎂 Yosh: {t.yosh}\n"
            f"✅ Faol: {'Ha' if t.faol else 'Yoq'}"
        )
        return response


class TalabaDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Talaba
    template_name = 'main/talaba_confirm_delete.html'
    success_url = reverse_lazy('royxat')
    permission_required = 'main.delete_talaba'

    def handle_no_permission(self):
        messages.error(self.request, "⛔ Sizda o'chirish huquqi yo'q!")
        return super().handle_no_permission()

    def form_valid(self, form):
        t = self.object
        telegram_yuborish(
            f"🗑 <b>Talaba o'chirildi!</b>\n\n"
            f"👤 Ism: {t.ism} {t.familiya}\n"
            f"🎓 Guruh: {t.guruh}"
        )
        messages.success(self.request, f"🗑 Talaba o'chirildi: {t}")
        return super().form_valid(form)


class AloqaForm(forms.Form):
    ism = forms.CharField(max_length=100, label="Ismingiz")
    email = forms.EmailField(label="Email")
    xabar = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), label="Xabar")


class AloqaView(FormView):
    template_name = 'main/aloqa.html'
    form_class = AloqaForm
    success_url = reverse_lazy('aloqa')

    def form_valid(self, form):
        d = form.cleaned_data
        messages.success(self.request, "✅ Xabaringiz yuborildi!")
        telegram_yuborish(
            f"📩 <b>Yangi aloqa xabari!</b>\n\n"
            f"👤 Ism: {d['ism']}\n"
            f"📧 Email: {d['email']}\n"
            f"💬 Xabar: {d['xabar']}"
        )
        return super().form_valid(form)
