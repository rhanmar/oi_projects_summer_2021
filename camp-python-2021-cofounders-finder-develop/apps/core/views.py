from django.shortcuts import render


def base_view(request):
    """Render base html template."""
    return render(request, "index.html")
