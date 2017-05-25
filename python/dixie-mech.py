import sys
import mechanicalsoup

browser = mechanicalsoup.StatefulBrowser()
mainpage = 'http://www.richmond.com/news/local/city-of-richmond/poll-should-richmond-remove-its-confederate-monuments/poll_70452265-9c50-587f-886e-10bcb46dd990.html'

pollid='poll-70452265-9c50-587f-886e-10bcb46dd990'
formid='#' + pollid + '-form'
voteid=pollid + '-your-vote'
nocode='C789C5A1-8370-0001-62F65000AC3718EB'

#page = browser.get(mainpage)
#form = page.soup.form

browser.open(mainpage)
browser.select_form(formid)
form = browser.get_current_form()
#form.form.find('input', {'title':'NO'})['checked'] = ''
form.check( {'answer':nocode} )
resp=browser.submit_selected()
print(resp)
res=browser.get_current_page()
print(res.find('div',id=voteid).text)

