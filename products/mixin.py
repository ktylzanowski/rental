class HomeMixin(object):
    template_name = 'products/home.html'
    ordering = ['popularity']

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.GET and self.request.GET['genre'] == 'alphabetical':
            qs = qs.order_by('title')
        elif self.request.GET and self.request.GET['genre'] == 'popularity':
            qs = qs.order_by('popularity')
        elif self.request.GET:
            qs = qs.filter(genre=self.request.GET['genre'])
        return qs

