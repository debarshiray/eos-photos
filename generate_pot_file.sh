find . -type f \( -name "*.py" -o -name "*.glade" \) | xargs xgettext --sort-output --keyword=N_ --keyword=C_:1c,2 -o po/endless_photos.pot --from-code=utf-8 --copyright-holder='Endless Mobile' --package-name='Endless Photos' --package-version=0