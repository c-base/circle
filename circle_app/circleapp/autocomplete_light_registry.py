import autocomplete_light
import views

class PersonAutocomplete(autocomplete_light.AutocompleteListBase):
    search_fields = ['username']

    def choices_for_request(self):
        search = self.request.GET['q']
        #return views.list_users()
        return [{'username': 'uk', 'role': 'member'}, {'username': 'smile', 'role': 'board'}]

    def choice_html(self, choice):
        return u'<span class="div" data-value="%s" data-role="%s">%s</span>' % (choice['username'], choice['role'], choice['username'])

autocomplete_light.register(PersonAutocomplete)

