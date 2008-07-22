import time
from django import newforms as forms

class CalendarWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    return super(CalendarWidget, self).render(name, value, attrs) + """
      <script type="text/javascript">
         InputCalendar.createOnLoaded('%s', {format:'yyyy-mm-dd'});
      </script>
    """ % attrs['id']

  def value_from_datadict(self, data, name):
    #return time.strptime(data.get(name, time.strftime('%Y/%m/%d')), '%Y/%m/%d')
    #return time.strptime(data.get(name, None), '%Y/%m/%d')
    return data.get(name, None)
