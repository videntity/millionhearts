from django.forms import HiddenInput
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

class ClientSignatureWidget(HiddenInput):
    def render(self, name, value, attrs=None, choices=()):    
        output="""
                <div class="sigPad">
                    <div class="sig sigWrapper">
                        <div class="typed"></div>
                        <canvas class="pad" width="198" height="55"></canvas>
                        <input type="hidden" name="patient_signature" class="output">
                    </div>
                    <a href="#clear" class="sigpad-clear">Clear</a>
                </div>
        """
        return mark_safe(force_unicode(output))
        
class WorkerSignatureWidget(HiddenInput):
    def render(self, name, value, attrs=None, choices=()):    
        output="""
                <div class="sigPad">
                    <div class="sig sigWrapper">
                        <div class="typed"></div>
                        <canvas class="pad" width="198" height="55"></canvas>
                        <input type="hidden" name="worker_signature" class="output">
                    </div>
                    <a href="#clear" class="sigpad-clear">Clear</a>
                </div>
        """
        return mark_safe(force_unicode(output))