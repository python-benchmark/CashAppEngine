
def current_date(request):
  from pycash.services import DateService
  return {'today': DateService.todayDate()}
