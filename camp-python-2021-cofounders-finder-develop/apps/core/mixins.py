from django.views.generic.edit import FormMixin


class PostFormMixin(FormMixin):
    """FormMixin with handling POST requests and saving form.

    If you need to add a form to a view without having to customize
    handling POST requests and saving form, you can use this mixin.
    It allows you not to define the post and form_valid methods
    in the child class.

    """
    def __init__(self, **kwargs):
        """Initialize object."""
        super().__init__(**kwargs)
        self.object = None

    def post(self, request, *args, **kwargs):
        """Handle POST requests

        Instantiate a form instance with the passed
        POST variables and then check if it's valid.

        """
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        """If the form is valid, save form."""
        form.save()
        return super().form_valid(form)
