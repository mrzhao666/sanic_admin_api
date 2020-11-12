class DataPage:
    max_page_size = 100
    page_size = 50
    page = 1

    def set_page(self, request):
        try:
            self.page = int(request.args.get("page", self.page))
            self.page_size = int(request.args.get("page_size", self.page_size))
            self.page_size = self.max_page_size if self.page_size > self.max_page_size else self.page_size
        except ValueError:
            pass
