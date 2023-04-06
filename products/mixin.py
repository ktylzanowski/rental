class HomeMixin(object):
    template_name = 'products/home.html'
    ordering = ['popularity']

    def get_queryset(self):
        qs = super().get_queryset()
        genre = self.request.GET.get('genre')
        if genre == 'alphabetical':
            qs = qs.order_by('title')
        elif genre == 'popularity':
            qs = qs.order_by('-popularity')
        elif genre:
            qs = qs.filter(genre=genre)
        return qs

