import autocomplete_light
import views

class PersonAutocomplete(autocomplete_light.AutocompleteListBase):
    search_fields = ['username']

    def choices_for_request(self):
        search = self.request.GET['q']
        return [i for i in views.list_users() if search in i['username']]

    def choice_html(self, choice):
        return u'<span class="div" data-value="%s" data-role="%s">%s</span>' % (choice['username'], choice['role'], choice['username'])

autocomplete_light.register(PersonAutocomplete)

